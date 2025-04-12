# core_service/client.py
import httpx
from fastapi import HTTPException
from config.config import config


async def generate_response(prompt: str) -> str:
    """
    Call the Core Service to generate a response based on an enhanced prompt.

    Args:
        prompt (str): The enhanced prompt from the Agent Service.

    Returns:
        str: The generated response.

    Raises:
        HTTPException: If the Core Service call fails.
    """
    payload = {"prompt": prompt}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{config.CORE_SERVICE_URL}/generate",
                json=payload,
                timeout=10.0,  # 10-second timeout
            )
            response.raise_for_status()
            return response.json()["response"]
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, detail=f"Core Service error: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to connect to Core Service: {str(e)}"
            )
