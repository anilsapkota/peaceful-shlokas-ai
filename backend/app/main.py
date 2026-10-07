from fastapi import FastAPI
from pydantic import BaseModel 
from backend.app.services.vagdhenu import generate_chant

app = FastAPI(
    title="Peaceful Shlokas AI",
    description="Generate Sanskrit chant audio from text",
    version = "0.1.0"
)


class ChantRequest(BaseModel):
    text: list[str]


@app.get("/health")
def health_check():
    return {"status":"healthy"}

@app.post("/generate")
def generate(request:ChantRequest):
    result = generate_chant(request.text)
    return result 