Class: OllamaModel

1. __init__(self)

Initializes the OllamaModel class with the API URL set to "http://localhost:11434/api".
2. async generate_response_async(self, knowledge, model="llama3")

Asynchronously generates a response from the Llama3 model using the provided knowledge prompt.
Streams the response and accumulates it in response_content.
Logs errors if the API call fails.
3. async show_ollama_info_async(self)

Asynchronously shows information about the Ollama service by running the ollama show command.
Logs and returns the command's output or errors if the command fails.
4. list_models(self)

Lists all available models by running the ollama list command.
Returns the list of models or logs and returns an empty list if the command fails.
5. install_ollama(self)

Installs Ollama using a shell script obtained via curl.
Runs the script and returns the installation status or logs and returns an error message if the command fails.
Function: check_ollama_installation()

Checks if Ollama is installed by running the ollama list command.
Logs and returns True if the command succeeds, otherwise logs and returns False.

# example usage

```
import asyncio
from ollamahandler import OllamaModel, check_ollama_installation

# Create an instance of OllamaModel
ollama_model = OllamaModel()

# Check if Ollama is installed
if check_ollama_installation():
    print("Ollama is installed.")

    # List available models
    models = ollama_model.list_models()
    print("Available models:", models)

    # Install Ollama
    installation_status = ollama_model.install_ollama()
    print(installation_status)

    # Show Ollama info asynchronously
    async def show_info():
        info = await ollama_model.show_ollama_info_async()
        print(info)

    asyncio.run(show_info())

    # Generate response asynchronously
    async def generate_response():
        response = await ollama_model.generate_response_async("Tell me about artificial intelligence.")
        print(response)

    asyncio.run(generate_response())
else:
    print("Ollama is not installed.")
```
