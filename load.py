import time
import psutil

app_cpu_usage = 0.01
app_mem_usage = 10

while(True):
    cpu_percent = psutil.cpu_percent(4)
    cpu_usage = psutil.cpu_count() * ( (100 - cpu_percent) / 100)
    mem_usage = psutil.virtual_memory()[1]

    app_count = round(min(mem_usage / app_mem_usage, cpu_usage / app_cpu_usage))

    print(app_count)

    f = open("stat.html", 'w')
    f.writelines(str(app_count))
    f.close()
    
    time.sleep(10)