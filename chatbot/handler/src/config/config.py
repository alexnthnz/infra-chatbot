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
    def LANGSMITH_API_KEY(self):
        try:
            resp = self._client.get_secret_value(SecretId=self._secret_arn)
            secret = json.loads(resp["SecretString"])
            return secret["LANGSMITH_API_KEY"]
        except ClientError as e:
            logger.error(f"Secrets Manager error: {e}")
            raise
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Invalid secret: {e}")
            raise


config = AppConfig()
