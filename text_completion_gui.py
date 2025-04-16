import tkinter as tk
from tkinter import scrolledtext
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Debug: Print the API key (first 5 characters for security)
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key loaded (first 5 chars): {api_key[:5] if api_key else 'None'}")

class TextCompletionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Completion App")
        self.root.geometry("800x600")
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Input section
        self.input_label = tk.Label(self.main_frame, text="Enter your prompt:")
        self.input_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.input_text = scrolledtext.ScrolledText(self.main_frame, height=5)
        self.input_text.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        
        # Submit button
        self.submit_button = tk.Button(self.main_frame, text="Submit", command=self.submit_prompt)
        self.submit_button.grid(row=2, column=0, pady=(0, 10))
        
        # Output section
        self.output_label = tk.Label(self.main_frame, text="Completion Result:")
        self.output_label.grid(row=3, column=0, sticky="w", pady=(0, 5))
        
        self.output_text = scrolledtext.ScrolledText(self.main_frame, height=10)
        self.output_text.grid(row=4, column=0, sticky="nsew")
        
        # Configure grid weights for main frame
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(4, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Initialize OpenAI
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            self.output_text.insert(tk.END, "Error: API key not found in .env file")
        
    def submit_prompt(self):
        prompt = self.input_text.get("1.0", tk.END).strip()
        if not prompt:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "Please enter a prompt first!")
            return
            
        try:
            # Get completion from OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Display the result
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, response.choices[0].message.content)
            
        except Exception as e:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextCompletionApp(root)
    root.mainloop() 