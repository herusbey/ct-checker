import requests
from bs4 import BeautifulSoup
import concurrent.futures
import os
import pyfiglet

# Banner oluşturma
banner = pyfiglet.figlet_format("Crackturkey")
print(banner)

# Alınacak proxy listesi dosyası
urls_file = 'proxy_urls.txt'

# Test edilecek hedef URL
test_url = 'http://www.google.com'

# Proxy'lerin kaydedileceği dosya adı
output_file = 'working_proxies.txt'
not_working_proxies_file = 'not_working_proxies.txt'

# Çalışan ve çalışmayan proxy'leri depolamak için liste oluştur
working_proxies = []
not_working_proxies = []

# İnternet bağlantısı kontrolü
def check_internet():
    try:
        requests.get('http://www.google.com', timeout=5)
        return True
    except:
        return False

# Proxy testi işlevi
def test_proxy(proxy):
    try:
        response = requests.get(test_url, proxies={'http': proxy, 'https': proxy}, timeout=10)
        if response.status_code == 200:
            working_proxies.append(proxy)
            print(f"{proxy} çalışıyor...")
        else:
            not_working_proxies.append(proxy)
            print(f"{proxy} çalışmıyor...")
    except:
        not_working_proxies.append(proxy)
        print(f"{proxy} çalışmıyor...")

# İnternet bağlantısı yoksa programı sonlandır
if not check_internet():
    print("Hata: İnternet bağlantısı yok.")
    exit()

# Tüm proxy listelerini birleştir
with open(urls_file, 'r') as file:
    urls = file.read().splitlines()

all_proxies = []
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    proxies = soup.get_text().split('\n')
    all_proxies += proxies

# Proxy'leri eş zamanlı olarak test et
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = [executor.submit(test_proxy, proxy) for proxy in all_proxies]

    # Proxy'leri belirli bir aralıkta ekrana yazdır
    for i, _ in enumerate(concurrent.futures.as_completed(results)):
        if i % 100 == 0:
            print(f"{i} proxy test edildi...")

# Çalışan proxy'leri dosyaya yaz
with open(output_file, 'w') as file:
    file.write('\n'.join(working_proxies))

# Çalışmayan proxy'leri dosyaya yaz
with open(not_working_proxies_file, 'w') as file:
    file.write('\n'.join(not_working_proxies))