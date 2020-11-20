from ping3 import ping
from socket import gethostbyname, gethostname
from multiprocessing.pool import ThreadPool
from time import sleep
from load_settings import LoadSettings
from gui import RenderWindow


class Ping:
    def __init__(self):
        self.window = RenderWindow()
        loading = LoadSettings()
        loading.open_settings("IPs", "timeout", 2)
        self.timeout = loading.load_settings()
        self.pool = ThreadPool(10)
        self.host = None

    def find_self(self):
        try:
            self.host = gethostbyname(gethostname())
        except RuntimeError as error:
            print(f"Could not read own IP. Are you root? {error}")
            self.host = False

    def ping_target(self, ip):
        print(f"Trying to reach {ip}...")
        ping_ms = ping(ip, timeout=self.timeout)
        if ping_ms is None:
            self.window.ip_list[ip] = None
            return ip, None  # Return None if IP can't be reached
        else:
            self.window.ip_list[ip] = ping_ms
            return ip, ping_ms  # Return ping if IP can be reached

    def main(self):
        self.find_self()
        print(f"This device has IP {self.host}")
        for ips in self.window.ip_list:
            self.pool.apply_async(self.ping_target, args=(ips, ))

    def await_results(self):
        sleep(self.timeout + 1)  # Give the threads some time to return the results.


while True:
    ping_class = Ping()
    ping_class.main()
    ping_class.await_results()
    ping_class.window.draw_window()
