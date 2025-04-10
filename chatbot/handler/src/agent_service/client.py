import httpx
from fastapi import HTTPException
from typing import Optional
from config.config import config


async def enhance_prompt(content: Optional[str] = None, file_url: Optional[str] = None) -> str:
    """
    Call the Agent Service to enhance a user prompt.

    Args:
        content (str, optional): The user's text input.
        file_url (str, optional): Presigned URL of an uploaded file (e.g., from S3).

    Returns:
        str: The enhanced prompt.

    Raises:
        HTTPException: If the Agent Service call fails.
    """
    payload = {
        "content": content,
        "file_url": file_url
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{config.AGENT_SERVICE_URL}/enhance",
                json=payload,
                timeout=10.0  # 10-second timeout
            )
            response.raise_for_status()
            return response.json()["enhanced_prompt"]
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Agent Service error: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to connect to Agent Service: {str(e)}"
            )