provider aws {
  profile                  = "default"
  shared_credentials_files = ["~/.aws/credentials"]
  region                   = var.aws_region 
}

resource aws_s3_bucket terraform_state {
  bucket = var.aws_s3_bucket 
}

resource aws_s3_bucket_versioning terraform_state {
  bucket = aws_s3_bucket.terraform_state.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource aws_s3_bucket_server_side_encryption_configuration terraform_state {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource aws_s3_bucket_public_access_block terraform_state {
  bucket                  = aws_s3_bucket.terraform_state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource aws_dynamodb_table terraform_state {
  name         = var.aws_dynamodb_table
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}

terraform {
  backend s3 {
    bucket         = "infra-chatbot-remote-state" 
    key            = "global/terraform.tfstate"
    dynamodb_table = "infra-chatbot-remote-state"
    region         = "ap-southeast-2"
    encrypt        = true
  }
}
