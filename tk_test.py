import tkinter as tk

root = tk.Tk()
root.title("Tkinter Test")
root.geometry("400x300")

txt = tk.Text(root, height=10)
txt.pack(fill="both", expand=True, padx=10, pady=10)

entry = tk.Entry(root)
entry.pack(fill="x", padx=10, pady=(0, 10))

btn = tk.Button(root, text="Send")
btn.pack(padx=10, pady=(0, 10))

root.mainloop()