from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel 
from backend.app.services.vagdhenu import generate_chant, VAGDHENU_ROOT

app = FastAPI(
    title="Peaceful Shlokas AI",
    description="Generate Sanskrit chant audio from text",
    version = "0.1.0"
)

app.mount(
    "/audio",
    StaticFiles(directory=VAGDHENU_ROOT / "out"),
    name="audio"
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