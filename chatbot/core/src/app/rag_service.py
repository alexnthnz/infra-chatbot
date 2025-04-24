import boto3
import json
import requests
from langchain_aws.retrievers import AmazonKnowledgeBasesRetriever
from langchain.prompts import ChatPromptTemplate
from tenacity import retry, stop_after_attempt, wait_exponential
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from src.config.settings import settings


class RAGService:
    def __init__(self):
        if not settings.bedrock_kb:
            raise ValueError(
                "Bedrock Knowledge Base ID not configured. Set BEDROCK_KB environment variable."
            )

        self.knowledge_base_id = settings.bedrock_kb
        self.bedrock_client = boto3.client("bedrock-runtime")
        self.session = boto3.Session()
        self.credentials = self.session.get_credentials()

        # Define the system prompt and RAG template
        self.system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, say that you "
            "don't know. Use three sentences maximum and keep the "
            "answer concise.\n\n{context}"
        )
        self.rag_prompt = ChatPromptTemplate.from_messages(
            [("system", self.system_prompt), ("human", "{input}")]
        )

    def _sign_request(self, method: str, url: str, body: dict) -> dict:
        """Sign an HTTP request with AWS SigV4 for OpenSearch Serverless."""
        headers = {"Content-Type": "application/json"}
        request = AWSRequest(method=method, url=url, data=json.dumps(body), headers=headers)
        SigV4Auth(self.credentials, "aoss", settings.aws_region).add_auth(request)
        return request.headers

    def embed_tool_result(self, tool_result: str, metadata: dict) -> None:
        """Embed a tool result into OpenSearch programmatically."""
        # Generate embedding using Bedrock
        response = self.bedrock_client.invoke_model(
            modelId="amazon.titan-embed-text-v2", body=json.dumps({"inputText": tool_result})
        )
        embedding = json.loads(response["body"].read())["embedding"]

        # Prepare document for OpenSearch
        document = {
            "bedrock-knowledge-base-default-vector": embedding,
            "AMAZON_BEDROCK_TEXT_CHUNK": tool_result,
            "AMAZON_BEDROCK_METADATA": metadata,
        }

        # Index into OpenSearch
        url = f"{settings.opensearch_endpoint}/llm_kb/_doc"
        headers = self._sign_request("POST", url, document)
        response = requests.post(url, headers=headers, data=json.dumps(document))

        if response.status_code != 201:
            raise RuntimeError(f"Failed to embed tool result: {response.text}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def retrieve_documents(self, query: str, num_results: int = 4) -> list:
        retriever = AmazonKnowledgeBasesRetriever(
            knowledge_base_id=self.knowledge_base_id,
            retrieval_config={"vectorSearchConfiguration": {"numberOfResults": num_results}},
        )
        return retriever.invoke(query)

    async def build_rag_prompt(self, query: str, num_results: int = 4):
        # Retrieve documents
        documents = await self.retrieve_documents(query, num_results)

        # Extract content and metadata
        retrieved_content = []
        sources = []
        for doc in documents:
            content = doc.page_content
            metadata = doc.metadata
            retrieved_content.append(content)
            sources.append(
                {
                    "content": content[:200] + "..." if len(content) > 200 else content,
                    "title": metadata.get("title", ""),
                    "uri": metadata.get("source", ""),
                }
            )

        # Build prompt
        context_text = "\n\n".join(retrieved_content)
        formatted_messages = self.rag_prompt.format_messages(context=context_text, input=query)

        # Format the prompt directly as a string
        prompt = ""
        for message in formatted_messages:
            if message.type == "system":
                prompt += f"{message.content}\n\n"
            elif message.type == "human":
                prompt += f"Human: {message.content}\n"
        prompt += "Assistant: "

        return prompt, sources
