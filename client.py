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
    query = 'bottomk(1, avg by (instance) (100 - rate(node_cpu_seconds_total{mode="idle"}[30s]) * 100))'
    url = 'http://10.199.2.120:9090/api/v1/query?query=' + query
    while(True):
        r = requests.get(url)
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