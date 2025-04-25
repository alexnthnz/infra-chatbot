data "aws_caller_identity" "current" {}

resource "aws_iam_role" "agent_model_role" {
  name = var.agent_model_role_name

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = { Service = "sagemaker.amazonaws.com" }
    }]
  })
}

resource "aws_iam_policy" "sagemaker_ecr_access_policy" {
  name        = "sagemaker-ecr-access"
  description = "Policy to allow SageMaker to pull images from ECR."
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability"
        ],
        Resource = "arn:aws:ecr:${var.aws_region}:${data.aws_caller_identity.current.account_id}:repository/agent-model-repo"
      },
      {
        Effect   = "Allow",
        Action   = "ecr:GetAuthorizationToken",
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "agent_model_ecr_access" {
  role       = aws_iam_role.agent_model_role.name
  policy_arn = aws_iam_policy.sagemaker_ecr_access_policy.arn
}

resource "aws_iam_role_policy_attachment" "foundation_model_ecr_access" {
  role       = aws_iam_role.foundation_model_role.name
  policy_arn = aws_iam_policy.sagemaker_ecr_access_policy.arn
}

resource "aws_iam_role_policy_attachment" "agent_model_sagemaker_access" {
  role       = aws_iam_role.agent_model_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}

resource "aws_iam_role_policy_attachment" "foundation_model_sagemaker_access" {
  role       = aws_iam_role.foundation_model_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}
