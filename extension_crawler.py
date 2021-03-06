import requests, json, threading, os, time, sys, getopt
from tqdm import tqdm

def download(flag, id_list, path, url):
    exist = os.listdir(path + 'extensions')
    for id in tqdm(id_list):
        if id + '.crx' in exist:
            continue
        try:
            print(url.format(id=id))
            resp = requests.get(url.format(id=id))
            print(resp)
        except requests.exceptions.ProxyError:
            time.sleep(1)
            try:
                resp = requests.get(url.format(id=id))
            except Exception as e:
                with open(path + 'download.log', 'a') as f:
                    f.writelines([id + ' error in downloading.'])
                continue
        with open(path + '/extensions/' + id + '.crx', 'wb') as f:
            f.write(resp.content)
    print('Thread No.' + str(flag) + ' end.')
        

# url = 'https://clients2.google.com/service/update2/crx?response=redirect&prodversion=49.0&x=id%3D{id}%26installsource%3Dondemand%26uc'
# url = 'https://clients2.google.com/service/update2/' + 'crx?response=redirect&nacl_arch=x86-64&' + 'prodversion=9999.0.9999.0&x=id%3D{id}%26uc'
# url = 'https://www.crx4chrome.com/go.php?p=51576&s=1&l=https%3A%2F%2Ff6.crx4chrome.com%2Fcrx.php%3Fi%3D{id}%26v%3D1.99.9'
# url = 'https://f6.crx4chrome.com/crx.php?i={id}&v=1.99.9&p=51576'
# url = "https://clients2.google.com/service/update2/crx?response=redirect&prodversion=49.0&x=id%3D{id}%26installsource%3Dondemand%26uc"
url = "https://clients2.google.com/service/update2/crx?response=redirect&prodversion=31.0.1609.0&acceptformat=crx2,crx3&x=id%3D{id}%26uc"

#  elicpjhcidhpjomhibiffojpinpmmpil

path = './'
if 'extensions' not in os.listdir(path):
    os.mkdir('extensions')
if 'ids.txt' not in os.listdir(path):
    print('ids.txt not found in the current path.')
    sys.exit()
with open(path + 'ids.txt', 'r') as f:
    ids = json.loads(f.read())
thread_num = 200
# ids = ids[:20]
try:
    opts, args = getopt.getopt(sys.argv[1:], 't:', ['thread='])
except getopt.GetoptError:
    print('crawler.py [-t|--thread <thread_number>]')
    sys.exit()
for opt, arg in opts:
    if opt in ('--thread', '-t'):
        thread_num = int(arg)

threads = []
flag = 0
step = len(ids) // thread_num
print('Task started with %d threads.'%thread_num)
for i in range(thread_num - 1):
    t = threading.Thread(target=download, args=(i, ids[flag:flag+step], path, url))
    t.start()
    threads.append(t)
    flag += step
t = threading.Thread(target=download, args=(thread_num - 1, ids[flag:], path, url))
t.start()
threads.append(t)
for t in threads:
    t.join()
print('Task finished.')
