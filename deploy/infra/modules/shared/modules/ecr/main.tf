resource "aws_ecr_repository" "agent_model_repo" {
  name                 = "agent-model-repo"
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}
