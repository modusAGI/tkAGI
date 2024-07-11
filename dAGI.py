import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from api import APIManager
from chatter import GPT4o, GroqModel, OllamaModel
#from make_decision import SocraticReasoning, Proposition

class DecideAGIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Decide AGI")
        self.api_manager = APIManager()
        self.setup_ui()
        self.chatter = None
        self.socratic_reasoning = None

    def setup_ui(self):
        # API Key Management
        self.api_frame = ttk.LabelFrame(self.root, text="API Key Management")
        self.api_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.add_api_button = ttk.Button(self.api_frame, text="Add API Key", command=self.add_api_key)
        self.add_api_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.remove_api_button = ttk.Button(self.api_frame, text="Remove API Key", command=self.remove_api_key)
        self.remove_api_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.list_api_button = ttk.Button(self.api_frame, text="List API Keys", command=self.list_api_keys)
        self.list_api_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Model Selection
        self.model_frame = ttk.LabelFrame(self.root, text="Model Selection")
        self.model_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        self.model_var = tk.StringVar()
        self.model_var.set("openai")
        
        self.openai_radio = ttk.Radiobutton(self.model_frame, text="OpenAI", variable=self.model_var, value="openai")
        self.openai_radio.grid(row=0, column=0, padx=5, pady=5)
        
        self.groq_radio = ttk.Radiobutton(self.model_frame, text="Groq", variable=self.model_var, value="groq")
        self.groq_radio.grid(row=0, column=1, padx=5, pady=5)
        
        self.ollama_radio = ttk.Radiobutton(self.model_frame, text="Ollama", variable=self.model_var, value="ollama")
        self.ollama_radio.grid(row=0, column=2, padx=5, pady=5)
        
        self.select_model_button = ttk.Button(self.model_frame, text="Select Model", command=self.select_model)
        self.select_model_button.grid(row=0, column=3, padx=5, pady=5)
        
        # Premise Input
        self.premise_frame = ttk.LabelFrame(self.root, text="Premise Input")
        self.premise_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        self.premise_entry = ttk.Entry(self.premise_frame, width=80)
        self.premise_entry.grid(row=0, column=0, padx=5, pady=5)
        
        self.add_premise_button = ttk.Button(self.premise_frame, text="Add Premise", command=self.add_premise)
        self.add_premise_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Decision Output
        self.decision_frame = ttk.LabelFrame(self.root, text="Decision Output")
        self.decision_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        
        self.decision_text = tk.Text(self.decision_frame, height=10, width=80, state=tk.DISABLED)
        self.decision_text.grid(row=0, column=0, padx=5, pady=5)
        
        self.make_decision_button = ttk.Button(self.decision_frame, text="Make Decision", command=self.make_decision)
        self.make_decision_button.grid(row=1, column=0, padx=5, pady=5)

    def add_api_key(self):
        service = simpledialog.askstring("Add API Key", "Enter the name of the service (e.g., 'openai', 'groq'):")
        api_key = simpledialog.askstring("Add API Key", f"Enter the API key for {service}:")
        if service and api_key:
            self.api_manager.save_api_key(service, api_key)
            messagebox.showinfo("Success", f"API key for {service} added successfully.")
        else:
            messagebox.showerror("Error", "Service name and API key cannot be empty.")

    def remove_api_key(self):
        service = simpledialog.askstring("Remove API Key", "Enter the name of the service to delete (e.g., 'openai', 'groq'):")
        if service:
            self.api_manager.remove_api_key(service)
            messagebox.showinfo("Success", f"API key for {service} removed successfully.")
        else:
            messagebox.showerror("Error", "Service name cannot be empty.")

    def list_api_keys(self):
        api_keys = self.api_manager.load_env_api_keys()
        if api_keys:
            keys_list = "\n".join([f"{service}: {key[:4]}...{key[-4:]}" for service, key in api_keys.items()])
            messagebox.showinfo("Stored API Keys", keys_list)
        else:
            messagebox.showinfo("Stored API Keys", "No API keys stored.")

    def select_model(self):
        model = self.model_var.get()
        api_key = self.api_manager.get_api_key(model)
        print(f"Selected model: {model}, API key: {api_key}")  # Debug print
        if api_key:
            if model == "openai":
                self.chatter = GPT4o(api_key)
            elif model == "groq":
                self.chatter = GroqModel(api_key)
            elif model == "ollama":
                self.chatter = OllamaModel()
            self.socratic_reasoning = SocraticReasoning(self.chatter)
            print("Model and SocraticReasoning instance initialized.")  # Debug print
            messagebox.showinfo("Success", f"{model.capitalize()} model selected successfully.")
        else:
            messagebox.showerror("Error", f"No API key found for {model}. Please add the API key first.")

    def add_premise(self):
        premise = self.premise_entry.get().strip()
        print(f"Adding premise: '{premise}', SocraticReasoning instance: {self.socratic_reasoning}")  # Debug print
        if premise and self.socratic_reasoning:
            self.socratic_reasoning.add_premise(premise)
            self.premise_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Premise added successfully.")
        else:
            messagebox.showerror("Error", "Premise cannot be empty or model not selected.")

    def make_decision(self):
        if self.socratic_reasoning:
            decision = self.socratic_reasoning.make_decision()
            self.decision_text.config(state=tk.NORMAL)
            self.decision_text.insert(tk.END, f"Decision: {decision}\n")
            self.decision_text.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Error", "Model not selected.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DecideAGIApp(root)
    root.mainloop()

