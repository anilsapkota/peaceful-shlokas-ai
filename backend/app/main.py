from fastapi import FastAPI

app = FastAPI(
    title="Peaceful Shlokas AI",
    description="Generate Sanskrit chant audio from text",
    version = "0.1.0"
)

@app.get("/health")
def health_check():
    return {"status":"healthy"}