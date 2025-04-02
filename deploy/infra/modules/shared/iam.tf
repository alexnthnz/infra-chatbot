resource "aws_iam_role" "agent_model_role" {
  name = var.agent_model_role_name

  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = { Service = "sagemaker.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role" "foundation_model_role" {
  name = var.foundation_model_role_name

  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = { Service = "sagemaker.amazonaws.com" }
    }]
  })
}

resource "aws_iam_policy" "sagemaker_s3_access_policy" {
  name        = "sagemaker-s3-access"
  description = "Policy to allow SageMaker to access S3 bucket for model artifacts."
  policy      = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = ["s3:ListBucket"],
        Resource = [aws_s3_bucket.model_artifacts.arn]
      },
      {
        Effect   = "Allow",
        Action   = ["s3:GetObject", "s3:PutObject"],
        Resource = ["${aws_s3_bucket.model_artifacts.arn}/*"]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "agent_model_s3_access" {
  role       = aws_iam_role.agent_model_role.name
  policy_arn = aws_iam_policy.sagemaker_s3_access_policy.arn
}

resource "aws_iam_role_policy_attachment" "foundation_model_s3_access" {
  role       = aws_iam_role.foundation_model_role.name
  policy_arn = aws_iam_policy.sagemaker_s3_access_policy.arn
}
