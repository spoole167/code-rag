from fastapi import FastAPI, Request
from sentence_transformers import SentenceTransformer

app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")

@app.post("/embed")
async def embed_text(request: Request):
    data = await request.json()
    print("Text in");
    print(data["text"]);
    text = data["text"]
    embedding = model.encode(text).tolist()
    return {"embedding": embedding}
