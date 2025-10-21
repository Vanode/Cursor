"""
Ollama LLM Client
Functions to interact with Ollama for ESG analysis
"""
import requests
from config import OLLAMA_HOST


def query_ollama(prompt: str, model: str = "llama2") -> str:
    """
    Sends a prompt to the local Ollama model and returns the response.
    
    Args:
        prompt (str): The prompt to send to the LLM
        model (str): The Ollama model to use (default: llama2)
    
    Returns:
        str: The response from Ollama or a mock response if not available
    
    Note:
        This is a stub implementation for now. In production, this will:
        - Make actual HTTP requests to Ollama API
        - Handle streaming responses
        - Implement error handling and retry logic
        - Support different models and parameters
    """
    
    # Stub implementation - returns mock response
    print(f"[OLLAMA STUB] Prompt: {prompt}")
    print(f"[OLLAMA STUB] Model: {model}")
    print(f"[OLLAMA STUB] Host: {OLLAMA_HOST}")
    
    mock_response = (
        f"[Mock Response] This is a placeholder response for the prompt: '{prompt}'. "
        "In production, this will connect to Ollama LLM for actual ESG analysis."
    )
    
    return mock_response


def query_ollama_streaming(prompt: str, model: str = "llama2"):
    """
    Sends a prompt to Ollama and streams the response.
    
    Args:
        prompt (str): The prompt to send to the LLM
        model (str): The Ollama model to use
    
    Yields:
        str: Chunks of the response as they are generated
    
    Note:
        Stub implementation - will be implemented when connecting to actual Ollama API
    """
    print(f"[OLLAMA STUB - STREAMING] Prompt: {prompt}")
    
    # Mock streaming response
    chunks = [
        "This is a ",
        "mock streaming ",
        "response for ",
        "ESG analysis."
    ]
    
    for chunk in chunks:
        yield chunk


def analyze_esg_with_ollama(company_name: str, context: str = "") -> dict:
    """
    Analyze ESG metrics for a company using Ollama LLM.
    
    Args:
        company_name (str): Name of the company to analyze
        context (str): Additional context or data about the company
    
    Returns:
        dict: Structured ESG analysis results
    
    Note:
        Stub implementation - will include prompt engineering for ESG analysis
    """
    prompt = f"""
    Analyze the ESG (Environmental, Social, and Governance) performance for {company_name}.
    
    Context: {context}
    
    Please provide:
    1. Environmental score (0-100)
    2. Social score (0-100)
    3. Governance score (0-100)
    4. Key insights and recommendations
    """
    
    response = query_ollama(prompt)
    
    # Stub: Return mock structured data
    return {
        "company": company_name,
        "analysis": response,
        "scores": {
            "environmental": 75,
            "social": 80,
            "governance": 85,
            "overall": 80
        },
        "status": "stub_response"
    }
