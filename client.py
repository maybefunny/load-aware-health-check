import sys
import time
import requests
import json

def main():
    # get host address from user
    addr = input("your address (None): ")
    if(addr == ''):
        print('server address is needed!')
        sys.exit(0)
    queries = []
    queries.append('bottomk(1, avg by (instance) (100 - rate(node_cpu_seconds_total{mode="idle"}[30s]) * 100) )')
    queries.append('bottomk(1,100*(1-((avg_over_time(node_memory_MemFree_bytes[30s])+avg_over_time(node_memory_Cached_bytes[30s])+avg_over_time(node_memory_Buffers_bytes[30s]))/avg_over_time(node_memory_MemTotal_bytes[30s]))))')
    queries.append('bottomk(1, rate(node_network_transmit_bytes_total{device="eth0"}[1m])*8/1024/1024)')
    url = 'http://172.28.128.3:9090/api/v1/query?query='
    while(True):
        for query in queries:
            r = requests.get(url+query)
            try:
                if(r.status_code == 200):
                    res = json.loads(r.text)
                    data = []
                    stat = ''
                    for item in res["data"]["result"]:
                        data.append(item["metric"]["instance"][:-5])
                    if(addr in data):
                        stat = 'true'
                    else:
                        stat = 'false'
                    print(repr(data))
                    f = open('stat.html', 'w')
                    f.writelines(stat)
                    f.close()
            except:
                pass
        time.sleep(10)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)