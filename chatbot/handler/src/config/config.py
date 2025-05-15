import os
import json
import logging
import boto3
from botocore.exceptions import ClientError

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class AppConfig:
    def __init__(self):
        self._client = boto3.client("secretsmanager", region_name="ap-southeast-2")
        self._secret_arn = os.environ["SECRET_ARN"]

    @property
    def DATABASE_URL(self):
        try:
            resp = self._client.get_secret_value(SecretId=self._secret_arn)
            secret = json.loads(resp["SecretString"])
            return secret["DATABASE_URL"]
        except ClientError as e:
            logger.error(f"Secrets Manager error: {e}")
            raise
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Invalid secret: {e}")
            raise

    @property
    def AWS_REGION_NAME(self):
        try:
            resp = self._client.get_secret_value(SecretId=self._secret_arn)
            secret = json.loads(resp["SecretString"])
            return secret["AWS_REGION_NAME"]
        except ClientError as e:
            logger.error(f"Secrets Manager error: {e}")
            raise
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Invalid secret: {e}")
            raise

    @property
    def AWS_BEDROCK_MODEL_ID(self):
        try:
            resp = self._client.get_secret_value(SecretId=self._secret_arn)
            secret = json.loads(resp["SecretString"])
            return secret["AWS_BEDROCK_MODEL_ID"]
        except ClientError as e:
            logger.error(f"Secrets Manager error: {e}")
            raise
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Invalid secret: {e}")
            raise

    @property
    def SERPER_API_KEY(self):
        try:
            resp = self._client.get_secret_value(SecretId=self._secret_arn)
            secret = json.loads(resp["SecretString"])
            return secret["SERPER_API_KEY"]
        except ClientError as e:
            logger.error(f"Secrets Manager error: {e}")
            raise
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Invalid secret: {e}")
            raise

    @property
    def TAVILY_API_KEY(self):
        try:
            resp = self._client.get_secret_value(SecretId=self._secret_arn)
            secret = json.loads(resp["SecretString"])
            return secret["TAVILY_API_KEY"]
        except ClientError as e:
            logger.error(f"Secrets Manager error: {e}")
            raise
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Invalid secret: {e}")
            raise

    @property
    def JWT_ACCESS_SECRET(self):
        try:
            resp = self._client.get_secret_value(SecretId=self._secret_arn)
            secret = json.loads(resp["SecretString"])
            return secret["JWT_ACCESS_SECRET"]
        except ClientError as e:
            logger.error(f"Secrets Manager error: {e}")
            raise
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Invalid secret: {e}")
            raise

    @property
    def JWT_REFRESH_SECRET(self):
        try:
            resp = self._client.get_secret_value(SecretId=self._secret_arn)
            secret = json.loads(resp["SecretString"])
            return secret["JWT_REFRESH_SECRET"]
        except ClientError as e:
            logger.error(f"Secrets Manager error: {e}")
            raise
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Invalid secret: {e}")
            raise

    @property
    def JWT_ALGORITHM(self):
        try:
            resp = self._client.get_secret_value(SecretId=self._secret_arn)
            secret = json.loads(resp["SecretString"])
            return secret["JWT_ALGORITHM"]
        except ClientError as e:
            logger.error(f"Secrets Manager error: {e}")
            raise
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Invalid secret: {e}")
            raise

    @property
    def JWT_AUDIENCE(self):
        try:
            resp = self._client.get_secret_value(SecretId=self._secret_arn)
            secret = json.loads(resp["SecretString"])
            return secret["JWT_AUDIENCE"]
        except ClientError as e:
            logger.error(f"Secrets Manager error: {e}")
            raise
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Invalid secret: {e}")
            raise

    @property
    def JWT_ISSUER(self):
        try:
            resp = self._client.get_secret_value(SecretId=self._secret_arn)
            secret = json.loads(resp["SecretString"])
            return secret["JWT_ISSUER"]
        except ClientError as e:
            logger.error(f"Secrets Manager error: {e}")
            raise
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Invalid secret: {e}")
            raise

    @property
    def REDIS_HOST(self):
        try:
            resp = self._client.get_secret_value(SecretId=self._secret_arn)
            secret = json.loads(resp["SecretString"])
            return secret["REDIS_HOST"]
        except ClientError as e:
            logger.error(f"Secrets Manager error: {e}")
            raise
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Invalid secret: {e}")
            raise

    @property
    def REDIS_PORT(self):
        try:
            resp = self._client.get_secret_value(SecretId=self._secret_arn)
            secret = json.loads(resp["SecretString"])
            return secret["REDIS_PORT"]
        except ClientError as e:
            logger.error(f"Secrets Manager error: {e}")
            raise
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Invalid secret: {e}")
            raise

    @property
    def REDIS_DB(self):
        try:
            resp = self._client.get_secret_value(SecretId=self._secret_arn)
            secret = json.loads(resp["SecretString"])
            return secret["REDIS_DB"]
        except ClientError as e:
            logger.error(f"Secrets Manager error: {e}")
            raise
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Invalid secret: {e}")
            raise

    @property
    def AWS_S3_BUCKET(self):
        try:
            resp = self._client.get_secret_value(SecretId=self._secret_arn)
            secret = json.loads(resp["SecretString"])
            return secret["AWS_S3_BUCKET"]
        except ClientError as e:
            logger.error(f"Secrets Manager error: {e}")
            raise
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Invalid secret: {e}")
            raise

    @property
    def GOOGLE_CLIENT_ID(self):
        try:
            resp = self._client.get_secret_value(SecretId=self._secret_arn)
            secret = json.loads(resp["SecretString"])
            return secret["GOOGLE_CLIENT_ID"]
        except ClientError as e:
            logger.error(f"Secrets Manager error: {e}")
            raise
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Invalid secret: {e}")
            raise

    @property
    def GOOGLE_CLIENT_SECRET(self):
        try:
            resp = self._client.get_secret_value(SecretId=self._secret_arn)
            secret = json.loads(resp["SecretString"])
            return secret["GOOGLE_CLIENT_SECRET"]
        except ClientError as e:
            logger.error(f"Secrets Manager error: {e}")
            raise
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Invalid secret: {e}")
            raise

    @property
    def GOOGLE_REDIRECT_URI(self):
        try:
            resp = self._client.get_secret_value(SecretId=self._secret_arn)
            secret = json.loads(resp["SecretString"])
            return secret["GOOGLE_REDIRECT_URI"]
        except ClientError as e:
            logger.error(f"Secrets Manager error: {e}")
            raise
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Invalid secret: {e}")
            raise


config = AppConfig()
