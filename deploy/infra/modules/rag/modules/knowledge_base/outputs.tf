output "knowledge_base_id" {
  description = "The ID of the Bedrock Agent Knowledge Base"
  value       = aws_bedrockagent_knowledge_base.llm_kb.id
}

output "knowledge_base_arn" {
  description = "The ARN of the Bedrock Agent Knowledge Base"
  value       = aws_bedrockagent_knowledge_base.llm_kb.arn
}
