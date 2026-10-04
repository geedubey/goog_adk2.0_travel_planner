from litellm import completion

# Find your Windows host IP from WSL by running: ip route | grep default | awk '{print $3}'
# Or use 'http://docker.internal' if running inside Docker on WSL
WINDOWS_HOST_IP = "http://192.168.29.21:11434"

try:
    response = completion(
        model="ollama/qwen2.5:7b",  # Replace with your pulled model name (e.g., ollama/llama3.2)
        messages=[{"role": "user", "content": "Hello! Are you working?"}],
        api_base=WINDOWS_HOST_IP,
    )
    print("Connection successful!")
    print(response["choices"][0]["message"]["content"])
except Exception as e:
    print(f"Connection failed: {e}")
