import tkinter as tk    

def 인사():
    print("안녕하세요")

root = tk.Tk()

root.title("나만의 메모장")
root.geometry("600x400") 

btn = tk.Button(root, text="누르기", command=인사)
btn.pack()

root.mainloop()