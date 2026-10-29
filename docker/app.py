
import logging
import os
from functools import lru_cache

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from devmate import DevMate


# Configure logging for Docker diagnostics.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="DevMate API",
    description="Experimental DevMate V3 text-generation API",
    version="0.1.1",
)


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)


class GenerateResponse(BaseModel):
    response: str


@lru_cache(maxsize=1)
def load_model():
    logger.info("Loading DevMate model...")

    model = DevMate(
        max_new_tokens=int(
            os.getenv("DEVMATE_MAX_NEW_TOKENS", "180")
        )
    )

    logger.info("DevMate model loaded successfully.")
    return model


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "devmate-api",
    }


@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    try:
        logger.info("Received generation request.")

        model = load_model()
        result = model.generate(request.prompt)

        logger.info("Generation completed successfully.")
        return GenerateResponse(response=result)

    except Exception as exc:
        # Log the full traceback for diagnosis.
        logger.exception("DevMate generation failed.")

        # Keep internal details hidden from API clients.
        raise HTTPException(
            status_code=500,
            detail=(
                "Generation failed. Check the server logs "
                "and model access."
            ),
        ) from exc
