# config/model_config.py
"""
Model configuration for Indian Legal Assistant GGUF
"""
from langchain_community.llms import LlamaCpp

def load_legal_model():
    """Initialize GGUF model with GPU acceleration"""
    
    print("Loading Indian Legal Assistant GGUF model...")
    
    # Initialize LlamaCpp with GGUF model
    llm = LlamaCpp(
        model_path="./models/indian_legal_assitant-q6_k.gguf",
        n_gpu_layers=35,  # GPU offload (all layers to GPU)
        n_ctx=2048,  # Context window
        n_batch=512,  # Batch size
        temperature=0.7,
        max_tokens=256,
        verbose=True  # Show loading progress
    )
    
    print("✅ Model loaded successfully on GPU!")
    return llm

_model_instance = None

def get_model():
    global _model_instance
    if _model_instance is None:
        _model_instance = load_legal_model()
    return _model_instance
