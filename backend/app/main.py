from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel 
from backend.app.services.vagdhenu import generate_chant, VAGDHENU_ROOT

app = FastAPI(
    title="Peaceful Shlokas AI",
    description="Generate Sanskrit chant audio from text",
    version = "0.1.0"
)

#Allow our React Development server to access the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET","POST"],
    allow_headers=["Content-Type"],
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