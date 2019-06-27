from urllib.parse import urlencode

import requests
from pyquery import PyQuery as pq

base_url = 'https://weixin.sogou.com/weixin?'

# 需要登陆
header = {
    'Cookie': 'SUV=00DB16B6B4A9F4EA5CEF5EA0FCB50910; CXID=F5F358424031EAEB4DC1E2B213FAA784; SUID=A6FFEC743865860A5CB44F4100049056; wuid=AAGiiuMvKAAAAAqLMXXNZAgApwM=; ad=cyllllllll2NlG4DlllllV1GXSUlllllH3X1fkllll9lllllVqxlw@@@@@@@@@@@; IPLOC=CN3100; ABTEST=5|1561534031|v1; SNUID=2B366B76C1C44DF53BFCD260C2FE708D; weixinIndexVisited=1; JSESSIONID=aaaoLvE-Bbj-QdXYEnqRw; sct=2',
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}
keyword = "风景"

proxy = None

max_count = 5


def get_proxy():
    proxy_pool_url = "http://localhost:5555/random"
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None


def get_html(url, count=1):
    global proxy

    if count >= max_count:
        print("出错次数较多")
        return None
    try:
        if proxy:
            proxies = {
                'http': "http://" + proxy
            }
            response = requests.get(url, allow_redirects=False, headers=header, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=header)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            # need proxy
            print("302!!!!!!!!!!!!!!!!!!!!!!!!")
            proxy = get_proxy()
            if proxy:
                print("可用")
                return get_html(url)
            else:
                return None
    except ConnectionError:
        count += 1
        proxy = get_proxy()  # 更换代理
        return get_html(url, count)


def get_index(keyword, page):
    data = {
        "query": keyword,
        "type": 2,
        "page": page
    }
    query = urlencode(data)
    url = base_url + query
    html = get_html(url)
    return html


def main():
    for page in range(1, 101):
        html = get_index(keyword, page)
        print(html)


def parse_index(html):
    doc=pq(html)
    item=doc('')


if __name__ == '__main__':
    main()
