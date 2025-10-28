from config.model_config import get_model

if __name__ == "__main__":
    # Load model (will auto-detect and use GPU if available)
    llm = get_model()
    print("Next")
    # Test query
    result = llm.invoke("What is Section 420 IPC?")
    print(result)