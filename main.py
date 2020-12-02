import tkinter as tk
from load_settings import LoadSettings
from ipaddress import ip_address
from ping3 import ping
from socket import gethostbyname, gethostname
from multiprocessing.pool import ThreadPool


def validate_ip(ip):
    try:
        ip = ip_address(ip)
        return True, None
    except ValueError:
        return False, "Not a valid IP!"


class RenderWindow:
    def __init__(self):
        self.host_ip = None
        self.ip_id = 1
        self.pool = ThreadPool(10)

        loading = LoadSettings()
        loading.open_settings("IPs", "ips", {})
        self.ip_list = loading.load_settings()
        self.ip = None
        self.label_ping = None
        self.ip_entry = None

        self.timeout = 1

        self.window = tk.Tk()
        self.frame = tk.Frame(master=self.window)
        self.label_ip = tk.Label(master=self.frame, text="IP:")
        self.ip_entry = tk.Entry(master=self.frame, width=15)
        self.enter_button = tk.Button(master=self.frame, text="Enter", command=self.change_ip)
        self.label_ping = tk.Label(master=self.frame, text=None)
        self.label_self_ip = tk.Label(master=self.window, text=None)
        self.label_error = tk.Label(master=self.frame, text=None)

    def change_ip(self):
        ip = self.ip_entry.get()
        confirmation = validate_ip(ip)
        if confirmation[0] is True:
            self.ip_list[self.ip_id-1] = ip
            loading = LoadSettings()
            loading.save_settings("IPs", "ips", self.ip_list)
            self.label_error["text"] = ip
        else:
            self.label_error["text"] = confirmation[1]

    def find_self(self):
        try:
            self.host_ip = gethostbyname(gethostname())
            self.label_self_ip["text"] = f"This device has IP {self.host_ip}"
        except RuntimeError as error:
            self.label_self_ip["text"] = f"Could not read own IP. Are you root? {error}"
            self.host_ip = False

    def draw_window(self):
        """Window Look General"""
        self.window.resizable(False, False)
        self.window.iconbitmap("pic.ico")
        self.window.title("Are they still online?")

        """Window Grid"""
        self.frame.grid(row=0, column=0, padx=10)
        self.label_ip.grid(row=0, column=0, sticky="w")
        self.ip_entry.grid(row=0, column=1, sticky="w")
        self.enter_button.grid(row=0, column=2, sticky="w")
        self.label_ping.grid(row=0, column=3, sticky="w")
        self.label_error.grid(row=1, column=1, sticky="w")
        self.label_self_ip.grid(row=2, column=0, sticky="w")

        """Find out own IP address"""
        self.find_self()

        """Run Main Loop and update window every second"""
        self.label_error["text"] = self.ip_list[self.ip_id-1]
        self.window.after(self.timeout * 1000, self.ping_target, self.ip_list[self.ip_id-1])
        self.window.mainloop()

    def ping_target(self, ip):
        ping_ms = ping(ip, timeout=self.timeout)
        if ping_ms is None:
            self.label_ping["text"] = "0.0ms"
            self.label_ping["bg"] = "#E27070"
        else:
            ping_ms = round(ping_ms*1000, 2)
            self.label_ping["text"] = f"{ping_ms}ms"
            self.label_ping["bg"] = "#CAFBB6"
        self.window.after(self.timeout * 1000 + 1000, self.ping_target, self.ip_list[self.ip_id-1])


if __name__ == "__main__":
    window = RenderWindow()
    window.draw_window()
