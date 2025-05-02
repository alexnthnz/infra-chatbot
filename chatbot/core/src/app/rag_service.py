import boto3
import json
from langchain_aws.retrievers import AmazonKnowledgeBasesRetriever
from langchain.prompts import ChatPromptTemplate
from tenacity import retry, stop_after_attempt, wait_exponential
from src.config.settings import settings


class RAGService:
    def __init__(self):
        if not settings.bedrock_kb:
            raise ValueError(
                "Bedrock Knowledge Base ID not configured. Set BEDROCK_KB environment variable."
            )

        self.knowledge_base_id = settings.bedrock_kb
        self.bedrock_client = boto3.client(
            "bedrock-agent-runtime",
            region_name=settings.aws_region,
        )
        self.session = boto3.Session()
        self.credentials = self.session.get_credentials()

        # Define the system prompt and RAG template
        self.system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, say that you "
            "don't know. Use three sentences maximum and keep the "
            "answer concise.\n\nContext:\n{context}"
        )
        self.rag_prompt = ChatPromptTemplate.from_messages(
            [("system", self.system_prompt), ("human", "{input}")]
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def retrieve_documents(self, query: str, num_results: int = 4) -> list:
        retriever = AmazonKnowledgeBasesRetriever(
            knowledge_base_id=self.knowledge_base_id,
            retrieval_config={"vectorSearchConfiguration": {"numberOfResults": num_results}},
            region_name=settings.aws_region,
        )
        documents = retriever.invoke(query)
        # Parse raw JSON if necessary
        parsed_documents = []
        for doc in documents:
            try:
                # If page_content is JSON, extract the 'content' field
                if doc.page_content.startswith("{"):
                    json_content = json.loads(doc.page_content)
                    doc.page_content = json_content["content"]
                    doc.metadata.update(json_content["metadata"])
                    doc.metadata["title"] = json_content["title"]
                parsed_documents.append(doc)
            except json.JSONDecodeError:
                parsed_documents.append(doc)
        return parsed_documents

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