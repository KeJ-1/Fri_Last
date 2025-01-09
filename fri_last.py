import tkinter as tk
from tkinter import filedialog
import requests

# Deepl のAI使用
DEEPL_AUTH_KEY = "12f0dd73-6f02-4330-8fd1-83307db98dcf:fx"
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"

class TranslationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Translation Application")
        
        # ラベル
        self.input_label = tk.Label(root, text="Enter Text for Translation:")
        self.input_label.pack(pady=5)

        # 入力スペース
        self.input_text = tk.Text(root, height=5, width=50)
        self.input_text.pack(pady=10)

        # キーボード入力ボタン
        self.translate_button = tk.Button(root, text="Translate Input Text", command=self.translate_input_text)
        self.translate_button.pack(pady=5)

        # ファイルのボタン
        self.file_button = tk.Button(root, text="Translate File", command=self.translate_file)
        self.file_button.pack(pady=5)

        # 出力エリア
        self.text_area = tk.Text(root, height=15, width=50)
        self.text_area.pack(pady=20)

    def translate_input_text(self):
        content = self.input_text.get(1.0, tk.END).strip()
        if not content:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, "Please enter text to translate.")
            return

        target_lang = "JA"  # 言語設定　多言語から日本語に変換
        translated_text = self.deepl_translate(content, target_lang)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, f"Translated Input Text:\n{translated_text}")

    def translate_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        target_lang = "JA" 
        translated_text = self.deepl_translate(content, target_lang)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, f"Translated File Content:\n{translated_text}")

    def deepl_translate(self, text, target_lang):
        try:
            params = {
                "auth_key": DEEPL_AUTH_KEY,
                "text": text,
                "target_lang": target_lang
            }
            response = requests.post(DEEPL_API_URL, data=params)
            response.raise_for_status()
            return response.json()["translations"][0]["text"]
        except Exception as e:
            return f"Error in translation: {e}"

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationApp(root)
    root.mainloop()
