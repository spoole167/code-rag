import os
import git
import requests
import hashlib
from sentence_transformers import SentenceTransformer
import time

# ✅ Configurations
GIT_REPO_URL = os.getenv("GIT_REPO_URL", "https://github.com/your/repo.git")
LOCAL_REPO_PATH = "/tmp/repo"
VECTOR_DB_URL = "http://vector-db:6333"
EMBEDDER_URL = "http://embedder:5001"

# ✅ Initialize Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

def clone_or_update_repo():
    """Clones the repo if not exists, else pulls latest changes."""
    if os.path.exists(LOCAL_REPO_PATH):
        repo = git.Repo(LOCAL_REPO_PATH)
        repo.remotes.origin.pull()
        print("✅ Repo updated!")
    else:
        git.Repo.clone_from(GIT_REPO_URL, LOCAL_REPO_PATH)
        print("✅ Repo cloned!")

def wait_for_qdrant():
    """Waits for Qdrant to be ready before indexing."""
    while True:
        try:
            response = requests.get(f"{VECTOR_DB_URL}/collections")
            if response.status_code == 200:
                print("✅ Qdrant is ready!")
                break
        except requests.exceptions.ConnectionError:
            print("⏳ Waiting for Qdrant...")
        time.sleep(2)


def generate_hash(content):
    """Generate a unique hash for a code snippet (avoids duplicate indexing)."""
    return hashlib.sha256(content.encode()).hexdigest()

def extract_code():
    """Extracts functions, classes, and relevant code from the repo."""
    code_snippets = []

    for root, _, files in os.walk(LOCAL_REPO_PATH):
        for file in files:
            if file.endswith(".py") or file.endswith(".java"):  # ✅ Extend for more languages
                file_path = os.path.join(root, file)

                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # ✅ Break content into functions/classes (basic version)
                snippets = content.split("\n\n")  # 🔹 Replace with AST-based parsing for accuracy
                for snippet in snippets:
                    if len(snippet) > 20:  # Avoid indexing tiny fragments
                        code_snippets.append((file_path, snippet))

    return code_snippets

def embed_and_store():
    """Embeds code snippets and stores them in Qdrant."""
    clone_or_update_repo()
    code_snippets = extract_code()

    for file_path, code in code_snippets:
        snippet_hash = generate_hash(code)

        # ✅ Step 1: Generate embedding
        response = requests.post(f"{EMBEDDER_URL}/embed", json={"text": code})
        embedding = response.json().get("embedding", [])

        # ✅ Step 2: Store in Qdrant
        payload = {
            "points": [
                {
                    "id": snippet_hash,
                    "vector": embedding,
                    "payload": {
                        "filename": file_path,
                        "code": code[:500],  # Store a preview (avoid large storage)
                    }
                }
            ]
        }

        requests.post(f"{VECTOR_DB_URL}/collections/code_rag/points", json=payload)
        print(f"✅ Indexed: {file_path}")

if __name__ == "__main__":
    # Ensure Qdrant is ready before indexing
        wait_for_qdrant()
        print("🔄 Running repo indexer...")
        embed_and_store()
        print("✅ Indexing complete.")
