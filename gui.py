import tkinter as tk
from time import sleep

t = 1

window = tk.Tk()
window.resizable(False, False)
window.iconbitmap("pic.ico")
window.title("Are They Still Online?")

def change_ip():
    pass

for i in range(2):
    for j in range(5):
        frame = tk.Button(master=window, relief=tk.RAISED, borderwidth=1, command=change_ip)
        frame.grid(row=i, column=j)
        label = tk.Label(master=frame, text=f"{t} IP: 255.255.255.{i}\nPing: {j}.385729s", bg="#ff8080")
        textbox = tk.Entry(master=frame, width=12)
        textbox.pack()
        label.pack()

window.mainloop()
