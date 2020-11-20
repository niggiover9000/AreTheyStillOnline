import tkinter as tk
from load_settings import LoadSettings
from ipaddress import ip_address


def validate_ip(ip):
    try:
        ip = ip_address(ip)
        return True, None
    except ValueError:
        return False, "Not a valid IP!"


class RenderWindow:
    def __init__(self):
        loading = LoadSettings()
        loading.open_settings("IPs", "ips", {})
        self.ip_list = loading.load_settings()
        ip = None
        self.label_online = None
        self.ip_entry = None

    def change_ip(self):
        ip = self.ip_entry.get()
        confirmation = validate_ip(ip)
        if confirmation[0] is True:
            if ip not in self.ip_list:
                self.ip_list[ip] = None
                loading = LoadSettings()
                loading.save_settings("IPs", "ips", self.ip_list)
                self.label_online["text"] = f"IP: {ip}\nPing: {self.ip_list[ip]}"
            else:
                self.label_online["text"] = "IP already used!"
        else:
            self.label_online["text"] = confirmation[1]

    def draw_window(self):
        window = tk.Tk()
        window.resizable(False, False)
        window.iconbitmap("pic.ico")
        window.title("Are They Still Online?")

        frame = tk.Frame(master=window)
        label_ip = tk.Label(master=frame, text="IP:")
        self.ip_entry = tk.Entry(master=frame, width=10)

        self.ip_entry.grid(row=0, column=1, sticky="w")
        label_ip.grid(row=0, column=0, sticky="e")

        enter_button = tk.Button(master=window, text="Enter", command=self.change_ip)
        self.label_online = tk.Label(master=window, text="Please select an IP")

        frame.grid(row=0, column=0, padx=10)
        enter_button.grid(row=0, column=2, sticky="e")
        self.label_online.grid(row=1, column=0, sticky="e")
        window.after(1000, self.draw_window)
        window.mainloop()


if __name__ == "__main__":
    window = RenderWindow()
    window.draw_window()
    window.mainloop()
