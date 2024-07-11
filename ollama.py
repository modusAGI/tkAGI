# ollama.py (c) Gregory L. Magnusson MIT license 2024
# Module for handling Llama3 models via the Ollama service
# Ollama Python Library

import logging
import ollama
import subprocess

class OllamaModel:
    """
    Class to interact with Llama3 model via the Ollama service.
    """
    def __init__(self):
        pass

    def generate_response(self, knowledge, model="llama3"):
        """
        Generate a response from the Llama3 model based on the given knowledge prompt using streaming.
        """
        try:
            response_content = ""
            stream = ollama.chat(model=model, messages=[{'role': 'user', 'content': knowledge}], stream=True)
            for chunk in stream:
                response_content += chunk['message']['content']
            return response_content
        except Exception as e:
            logging.error(f"ollama api error: {e}")
            return "error: unable to generate a response due to an issue with the ollama api."

    def list_models(self):
        """
        List all available models in the Ollama service.
        """
        command = "ollama list"
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip().splitlines()
            else:
                logging.error(f"ollama api error: {result.stderr}")
                return []
        except Exception as e:
            logging.error(f"ollama api error: {e}")
            return []

    def install_ollama(self):
        """
        Install Ollama using the provided installation script.
        """
        command = "curl -fsSL https://ollama.com/install.sh | sh"
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return "Ollama installation successful."
            else:
                logging.error(f"ollama install error: {result.stderr}")
                return "error: unable to install ollama."
        except Exception as e:
            logging.error(f"ollama install error: {e}")
            return "error: unable to install ollama."

# Function to check if Ollama is installed from the default URL
def check_ollama_installation():
    command = "ollama list"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            logging.info("Ollama is installed and accessible.")
            return True
        else:
            logging.error("Ollama is not accessible.")
            return False
    except Exception as e:
        logging.error(f"Failed to check Ollama installation: {e}")
        return False

