#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function

import logging
import re

import requests
import retrying

logger = logging.getLogger(__name__)


class Proxy(object):
    def __init__(self):
        self.re_ip_port_pattern = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):([\d]{1,5})")

        self.cur_proxy = None
        self.proxies = []
        self.result = []

        self.txt_list = [
            # 'http://api.xicidaili.com/free2016.txt',
            'http://static.fatezero.org/tmp/proxy.txt',
            'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt',
            'http://pubproxy.com/api/proxy?limit=20&format=txt&type=http',
            # 'http://comp0.ru/downloads/proxylist.txt',
            'http://www.proxylists.net/http_highanon.txt',
            'http://www.proxylists.net/http.txt',
            'http://ab57.ru/downloads/proxylist.txt',
            'https://www.rmccurdy.com/scripts/proxy/good.txt',
            'https://raw.githubusercontent.com/parserpp/ip_ports/main/proxyinfo.txt',
            'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt',
            'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
            'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
            'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt',
            'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
            'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
            'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt',
            'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt',
            'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt',
            'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt'
        ]

    @retrying.retry(stop_max_attempt_number=3)
    def extract_proxy(self, url):
        try:
            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) "
                              "Chrome/21.0.1180.89 Safari/537.1'"
            }
            rp = requests.get(url, proxies=self.cur_proxy, headers=headers, timeout=10)

            re_ip_port_result = self.re_ip_port_pattern.findall(rp.text)

            if not re_ip_port_result:
                raise Exception("empty")

        except Exception as e:
            logger.error("[-] Request url {url} error: {error}".format(url=url, error=str(e)))
            while self.proxies:
                new_proxy = self.proxies.pop(0)
                self.cur_proxy = {new_proxy['type']: "%s:%s" % (new_proxy['host'], new_proxy['port'])}
                raise e
            else:
                return []
        for cc in range(10):
            u = 'https://gimmeproxy.com/api/getProxy?ipPort=true&post=true&supportsHttps=true&maxCheckPeriod=300&minSpeed=50'
            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) "
                              "Chrome/21.0.1180.89 Safari/537.1'"
            }
            res = requests.get(u, proxies=self.cur_proxy, headers=headers, timeout=10)
            if res.text not in re_ip_port_result:
                re_ip_port_result.append(res.text)

        return [{'host': host, 'port': int(port), 'from': 'txt'} for host, port in re_ip_port_result]

    def start(self):
        for url in self.txt_list:
            try:
                page_result = self.extract_proxy(url)
            except:
                continue

            if not page_result:
                continue

            self.result.extend(page_result)


if __name__ == '__main__':
    p = Proxy()
    p.start()

    for i in p.result:
        print(i)

    print(len(p.result))
