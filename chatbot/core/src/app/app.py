from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
import json
from transformers import AutoModelForCausalLM, AutoTokenizer

from src.config.settings import settings

app = FastAPI(title=settings.app_name)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load code generation model
try:
    model_name = settings.code_model_name
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    print(f"Model {model_name} loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    tokenizer = None


class CodeGenerationRequest(BaseModel):
    prompt: str
    max_length: int = settings.code_model_max_length
    temperature: float = settings.code_model_default_temperature
    top_p: float = settings.code_model_default_top_p
    num_return_sequences: int = 1


class CodeGenerationResponse(BaseModel):
    generated_code: str


@app.post("/generate-code", response_model=CodeGenerationResponse)
async def generate_code(request: CodeGenerationRequest):
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not available")

    try:
        inputs = tokenizer(request.prompt, return_tensors="pt")

        with torch.no_grad():
            generated_ids = model.generate(
                inputs.input_ids,
                max_length=request.max_length,
                temperature=request.temperature,
                top_p=request.top_p,
                num_return_sequences=request.num_return_sequences,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
            )

        generated_code = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

        # Remove the original prompt from the generated code
        if generated_code.startswith(request.prompt):
            generated_code = generated_code[len(request.prompt) :]

        return CodeGenerationResponse(generated_code=generated_code)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Code generation error: {str(e)}")


@app.post("/invocations")
async def sagemaker_invocations(request: Request):
    """
    SageMaker-compatible invocation endpoint for code generation.
    Accepts JSON with the same parameters as the /generate-code endpoint.
    """
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not available")
    
    try:
        # Get the raw request body
        body = await request.body()
        
        # Parse JSON
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON payload")
        
        # Extract parameters with defaults
        prompt = payload.get("prompt")
        if not prompt:
            raise HTTPException(status_code=400, detail="Missing 'prompt' in request")
            
        max_length = payload.get("max_length", settings.code_model_max_length)
        temperature = payload.get("temperature", settings.code_model_default_temperature)
        top_p = payload.get("top_p", settings.code_model_default_top_p)
        num_return_sequences = payload.get("num_return_sequences", 1)
        
        # Generate code
        inputs = tokenizer(prompt, return_tensors="pt")
        
        with torch.no_grad():
            generated_ids = model.generate(
                inputs.input_ids,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                num_return_sequences=num_return_sequences,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
            )
        
        generated_code = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        
        # Remove the original prompt from the generated code
        if generated_code.startswith(prompt):
            generated_code = generated_code[len(prompt):]
        
        # Return SageMaker-compatible response (JSON string)
        return {"generated_code": generated_code}
    
    except Exception as e:
        # SageMaker expects HTTP 200 with error details in response body
        return {"error": str(e)}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.get("/ping")
async def sagemaker_ping():
    """SageMaker-compatible health check endpoint"""
    return {"status": "healthy"}
