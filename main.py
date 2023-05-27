import uvicorn

if __name__ == "__main__":
    # Dla możliwości rozbudowy podstawowych argumentów uvicorn jest uruchamiany programowo
    uvicorn.run("generator.app:api", host="0.0.0.0",
                port=8055, log_level="debug", reload=True)
