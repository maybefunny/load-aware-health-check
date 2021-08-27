import time
import psutil

class load:
    net_capacity = 1000
    app_cpu_usage = 0.01
    app_mem_usage = 10
    app_net_usage = 10

    def __init__(self) -> None:
        while(True):
            cpu_percent = psutil.cpu_percent(4)
            cpu_available = psutil.cpu_count() * ( (100 - cpu_percent) / 100)
            mem_available = psutil.virtual_memory()[1]
            
            net_stat = psutil.net_io_counters(nowrap=True)
            net_in_1 = net_stat.bytes_recv
            net_out_1 = net_stat.bytes_sent
            time.sleep(1)
            net_stat = psutil.net_io_counters(nowrap=True)
            net_in_2 = net_stat.bytes_recv
            net_out_2 = net_stat.bytes_sent

            net_in = round((net_in_2 - net_in_1) / 1024, 3)
            net_out = round((net_out_2 - net_out_1) / 1024, 3)
            net_available = self.net_capacity - (net_in + net_out)

            app_count = round(min(mem_available / self.app_mem_usage, cpu_available / self.app_cpu_usage, net_available / self.app_net_usage))

            print(app_count)

            f = open("stat.html", 'w')
            f.writelines(str(app_count))
            f.close()
            
            time.sleep(10)

if(__name__ == "__main__"):
    load()