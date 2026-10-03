"""Diagnostic script to test Ollama connectivity and LiteLLM directly.
Run with: uv run python test_ollama.py
"""
import sys
import requests

OLLAMA_URL = "http://localhost:11434"

print("=" * 50)
print("Step 1: Testing direct HTTP connection to Ollama...")
print("=" * 50)

try:
    resp = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
    if resp.status_code == 200:
        models = resp.json().get("models", [])
        model_names = [m.get("name") for m in models]
        print(" SUCCESS: Connected to Ollama!")
        print(f" Available models: {model_names}")
        
        # Check if qwen2.5:7b or similar exists
        has_qwen = any("qwen" in m for m in model_names)
        if not has_qwen:
            print("\n  WARNING: No 'qwen' model found in Ollama!")
            print("  Run in Windows: ollama pull qwen2.5:7b")
    else:
        print(f"❌ Ollama returned status code: {resp.status_code}")
except Exception as e:
    print(f"❌ FAILED to connect to Ollama at {OLLAMA_URL}")
    print(f"   Error: {e}")
    print("\n   Probable causes:")
    print("   1. Ollama is not running on Windows.")
    print("   2. OLLAMA_HOST=0.0.0.0 is not set on Windows (Ollama is rejecting WSL connections).")
    print("   3. WSL2 cannot reach Windows localhost (NAT vs mirrored mode).")
    sys.exit(1)

print("\n" + "=" * 50)
print("Step 2: Testing LiteLLM chat completion...")
print("=" * 50)

try:
    import litellm
    # Test simple completion
    print("Sending test prompt 'Say hello in 3 words' to LiteLLM...")
    res = litellm.completion(
        model="ollama_chat/qwen2.5:7b",
        messages=[{"role": "user", "content": "Say hello in 3 words"}],
        timeout=30
    )
    reply = res.choices[0].message.content
    print(" SUCCESS: LiteLLM received response from Ollama!")
    print(f" Response: {reply}")
except Exception as e:
    print(f"❌ LiteLLM FAILED with error: {e}")
    sys.exit(1)

print("\n" + "=" * 50)
print(" ALL CHECKS PASSED! Your Ollama setup is ready for ADK.")
print("=" * 50)
