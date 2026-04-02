import tkinter as tk
import subprocess

def run_scan():
    subprocess.run("python clienthigh.py", shell=True)

root = tk.Tk()
root.title("Fingerprint Tool")

tk.Label(root, text="Click to Start Scan").pack(pady=20)
tk.Button(root, text="Start", command=run_scan).pack()

root.mainloop()