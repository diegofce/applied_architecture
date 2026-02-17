from fastapi import FastAPI

app = FastAPI(title="Applied Architecture API")

@app.get("/api/health")
def health():
    return {"status": "ok"}
