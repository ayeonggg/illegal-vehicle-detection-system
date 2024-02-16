import tkinter as tk
from tkinter import scrolledtext
import webbrowser
import re
from datetime import datetime

class BoardApp:
    
    def __init__(self, frame, width, height):
        self.num = 1
        self.board_data = []
        self.board_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=width, height=height)
        self.board_text.pack(padx=10, pady=10)

    def update_board(self, address, source):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_info = f"[{self.num}]\n{current_time}\n{address}\n{source}\n\n"
        self.num = self.num + 1
        self.board_data.insert(0, new_info)
        self.board_text.delete(1.0, tk.END)
        for info in self.board_data:
            self.insert_with_hyperlinks(info)

    def insert_with_hyperlinks(self, text):
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        parts = re.split(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)

        for i in range(len(parts)):
            if i < len(urls):
                self.board_text.insert(tk.END, parts[i], f"url_{i}")
                self.board_text.tag_add(f"url_{i}", f"{tk.END}-{len(parts[i])}c", tk.END)
                self.board_text.tag_config(f"url_{i}", foreground="blue", underline=True)
                self.board_text.tag_bind(f"url_{i}", "<Button-1>", lambda e, url=urls[i]: self.open_url(url))
            else:
                self.board_text.insert(tk.END, parts[i])

        self.board_text.insert(tk.END, "\n")

    def open_url(self, url):
        webbrowser.open(url)