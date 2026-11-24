import tkinter as tk
from tkinter import filedialog

FILE_TYPES = [("Text Files", "*.txt")];

def open_file():
    file_path = filedialog.askopenfilename(filetypes=FILE_TYPES)
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, content)

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=FILE_TYPES)
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            content = text_area.get(1.0, tk.END)
            file.write(content)

window = tk.Tk()
window.title("나만의 메모장")
text_area = tk.Text(window, wrap="word")
text_area.pack(expand=True, fill="both") # True 대신 1도 가능. 

manu = tk.Menu(window)
window.config(menu=manu)
file_menu = tk.Menu(manu, tearoff=0)
manu.add_cascade(label="파일", menu=file_menu)
file_menu.add_command(label="열기", command=open_file)
file_menu.add_command(label="저장", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="종료", command=window.quit)
window.mainloop()

