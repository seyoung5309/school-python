import tkinter as tk

def greet():
    name = entry.get().strip() or "여러분"
    result.config(text=f"{name}님, 안녕하세요!")

def reset():
    entry.delete(0, tk.END)
    result.config(text="이름을 입력하세요.")

root = tk.Tk()
root.title("인사 실습 · tkinter")
root.geometry("480x260")
tk.Label(root, text="나의 첫 GUI", font=("sans-serif", 20)).pack(pady=16)
entry = tk.Entry(root)
entry.pack(fill="x", padx=30)
tk.Button(root, text="인사하기", command=greet).pack(pady=8)
tk.Button(root, text="초기화", command=reset).pack()
result = tk.Label(root, text="이름을 입력하세요.")
result.pack(pady=12)
root.mainloop()
