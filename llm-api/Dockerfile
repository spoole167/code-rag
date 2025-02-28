# --- Stage 1: Builder (download model) ---
    FROM ollama/ollama:latest AS builder

    # Start Ollama in background and download model
    RUN ollama serve & \
        sleep 2 && \
        ollama pull gemma:2b

    # --- Stage 2: Final Image ---
    FROM ollama/ollama:latest

    # Copy pre-downloaded models from builder stage
    COPY --from=builder /root/.ollama /root/.ollama

    # Start Ollama serve
    #CMD ["ollama", "serve"]
