import customtkinter as ctk
from tkinter import filedialog, messagebox
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize NLTK VADER
nltk.download('vader_lexicon', quiet=True)
analyzer = SentimentIntensityAnalyzer()

# UI Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SentimentApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Sentiment Analyzer 2026")
        self.geometry("800x600")

        # --- Layout ---
        self.grid_columnconfigure(0, weight=1)
        
        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Sentiment Analysis Engine", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=20)

        # Text Input Area
        self.textbox = ctk.CTkTextbox(self, width=600, height=200, corner_radius=15)
        self.textbox.pack(pady=10)
        self.textbox.insert("0.0", "Paste your text here or upload a file...")

        # Buttons Frame
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=20)

        self.upload_btn = ctk.CTkButton(self.button_frame, text="Upload .txt File", command=self.upload_file, corner_radius=10)
        self.upload_btn.grid(row=0, column=0, padx=10)

        self.analyze_btn = ctk.CTkButton(self.button_frame, text="Analyze Sentiment", command=self.analyze_text, fg_color="#2ecc71", hover_color="#27ae60", corner_radius=10)
        self.analyze_btn.grid(row=0, column=1, padx=10)

        # Results Display
        self.result_frame = ctk.CTkFrame(self, width=600, height=150, corner_radius=15)
        self.result_frame.pack(pady=20, padx=20, fill="x")

        self.score_label = ctk.CTkLabel(self.result_frame, text="Overall Score: N/A", font=ctk.CTkFont(size=18))
        self.score_label.pack(pady=10)

        self.feature_label = ctk.CTkLabel(self.result_frame, text="Detected Features: None", font=ctk.CTkFont(size=14))
        self.feature_label.pack(pady=5)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.textbox.delete("0.0", "end")
                self.textbox.insert("0.0", content)

    def analyze_text(self):
        text = self.textbox.get("0.0", "end").strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text first!")
            return

        # Perform Analysis
        scores = analyzer.polarity_scores(text)
        compound = scores['compound']
        
        # Determine Label
        if compound >= 0.05:
            sentiment = "Positive 😊"
            color = "#2ecc71"
        elif compound <= -0.05:
            sentiment = "Negative ☹️"
            color = "#e74c3c"
        else:
            sentiment = "Neutral 😐"
            color = "#f1c40f"

        # Update UI
        self.score_label.configure(text=f"Sentiment: {sentiment} (Score: {compound})", text_color=color)
        
        # Display breakdown features
        features = f"Positive: {scores['pos']} | Neutral: {scores['neu']} | Negative: {scores['neg']}"
        self.feature_label.configure(text=features)

if __name__ == "__main__":
    app = SentimentApp()
    app.mainloop()