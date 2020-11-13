from ping3 import ping
from socket import gethostbyname, gethostname
from multiprocessing.pool import ThreadPool
from time import sleep
from load_settings import LoadSettings


class Ping:
    def __init__(self):
        loading = LoadSettings()
        loading.open_settings("IPs", "timeout", 2)
        self.timeout = loading.load_settings()
        loading.open_settings("IPs", "ips", ["8.8.8.8"])
        self.ips = loading.load_settings()
        self.pool = ThreadPool(10)
        self.host = None

    def find_self(self):
        try:
            self.host = gethostbyname(gethostname())
        except RuntimeError as error:
            print(f"Could not read own IP. Are you root? {error}")
            self.host = False

    def ping_target(self, ip):
        sleep(1)
        print(f"Trying to reach {ip}...")
        request = ping(ip, timeout=self.timeout)
        if request is None:
            print(f"Can't reach {ip}")
            return False
        else:
            print(f"Ping for {ip}: {request}")
            return True

    def main(self):
        self.find_self()
        print(f"This device has IP {self.host}")
        for ips in self.ips:
            self.pool.apply_async(self.ping_target, args=(ips, ))

    def await_results(self):
        sleep(self.timeout + 1) # Give the threads some time to return the results.


while True:
    ping_class = Ping()
    ping_class.main()
    ping_class.await_results()