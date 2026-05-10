import tkinter as tk
from tkinter import filedialog, messagebox
import random
import os
import platform
import subprocess

class GlitchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hex Glitcher")
        self.root.geometry("400x350")
        self.root.configure(bg="#f0f0f0")

        tk.Label(root, text="Настройка поломки", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)

        tk.Label(root, text="Насколько всё плохо:", bg="#f0f0f0").pack()
        self.slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, length=300, bg="#f0f0f0")
        self.slider.set(5)
        self.slider.pack(pady=5)

        tk.Label(root, text="Безопасный отступ (байт в начале):", bg="#f0f0f0").pack(pady=5)
        self.offset_entry = tk.Entry(root, justify='center')
        self.offset_entry.insert(0, "5000")
        self.offset_entry.pack()

        self.btn = tk.Button(root, text="ВЫБРАТЬ И СЛОМАТЬ", command=self.process_file, 
                             bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                             padx=20, pady=10)
        self.btn.pack(pady=25)

        self.status = tk.Label(root, text="Готов к работе", bg="#f0f0f0", fg="gray")
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def glitch_data(self, data):
        content = bytearray(data)
        chance = (self.slider.get() / 1000) 
        
        try:
            offset = int(self.offset_entry.get())
        except:
            offset = 5000

        if len(content) <= offset:
            return content

        for i in range(offset, len(content)):
            if random.random() < chance:
                content[i] = random.randint(0, 255)
        return content

    def open_file(self, path):
        current_os = platform.system()
        if current_os == 'Windows':
            os.startfile(path)
        elif current_os == 'Darwin':
            subprocess.call(('open', path))
        else:
            subprocess.call(('xdg-open', path))

    def process_file(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        try:
            with open(file_path, 'rb') as f:
                original_data = f.read()

            glitched_data = self.glitch_data(original_data)

            base, ext = os.path.splitext(file_path)
            output_path = f"{base}_glitched_{random.randint(10,99)}{ext}"

            with open(output_path, 'wb') as f:
                f.write(glitched_data)

            self.status.config(text=f"Создан: {os.path.basename(output_path)}")
            self.open_file(output_path)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Что-то пошло не так: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GlitchApp(root)
    root.mainloop()
