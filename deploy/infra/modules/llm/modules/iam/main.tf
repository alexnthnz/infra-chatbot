resource "aws_iam_role" "llm_exec" {
  name = "${var.sagemaker_name}-sagemaker-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = { Service = "sagemaker.amazonaws.com" }
    }]
  })
}

resource "aws_iam_policy" "sagemaker_access_policy" {
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
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetAuthorizationToken"
        ],
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "llm_ecr_access" {
  role       = aws_iam_role.llm_exec.name
  policy_arn = aws_iam_policy.sagemaker_access_policy.arn
}

resource "aws_iam_role_policy_attachment" "llm_sagemaker_access" {
  role       = aws_iam_role.llm_exec.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}
