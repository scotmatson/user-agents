#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Scrapes User-Agent strings from:
    http://www.useragentstring.com/pages/useragentstring.php?typ=Browser
'''

__author__    = 'Scot Matson'
__copyright__ = 'Copyright 2016'

import logging
import sys
import datetime
import requests
import json
from bs4 import BeautifulSoup

def main():
    urls = [
        'http://www.useragentstring.com/pages/useragentstring.php?typ=Crawler',
        'http://www.useragentstring.com/pages/useragentstring.php?typ=Browser',
        'http://www.useragentstring.com/pages/useragentstring.php?typ=Mobile%20Browser',
        'http://www.useragentstring.com/pages/useragentstring.php?typ=Console',
        'http://www.useragentstring.com/pages/useragentstring.php?typ=Offline%20Browser',
        'http://www.useragentstring.com/pages/useragentstring.php?typ=E-mail%20Client',
        'http://www.useragentstring.com/pages/useragentstring.php?typ=Link%20Checker',
        'http://www.useragentstring.com/pages/useragentstring.php?typ=E-mail%20Collector',
        'http://www.useragentstring.com/pages/useragentstring.php?typ=Validator',
        'http://www.useragentstring.com/pages/useragentstring.php?typ=Feed%20Reader',
        'http://www.useragentstring.com/pages/useragentstring.php?typ=Librarie',
        'http://www.useragentstring.com/pages/useragentstring.php?typ=Cloud%20Platform',
        'http://www.useragentstring.com/pages/useragentstring.php?typ=Other'
    ]

    filenames = [
        'crawler/crawler.json',
        'browser/browser-desktop.json',
        'browser/browser-mobile.json',
        'console/console.json',
        'browser/browser-offline.json',
        'email/email-client.json',
        'linkchecker/link-checker.json',
        'email/email-collector.json',
        'validator/validator.json',
        'feedreader/feed-reader.json',
        'library/library.json',
        'cloudplatform/cloud-platform.json',
        'other/other.json'
    ]

    if len(urls) == len(filenames):
        headers = {
            'Host': 'www.useragentstring.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': 1,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'DNT': 1,
            'Referer': 'http://www.useragentstring.com/pages/useragentstring.php',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
        }

        number_of_resources = len(urls)
        for i in range(number_of_resources):
            soup = None
            try:
                r = requests.get(urls[i], headers=headers)
                if r.status_code is requests.codes.ok:
                    soup = BeautifulSoup(r.text, 'html5lib')
                else:
                    logging.warning([r.status_code, t.text])
            except requests.exceptions.RequestException:
                logging.exception([url,header,r])

            if soup:
                ua_div = soup.find('div', {'id' : 'liste'})
                browsers = dict()
                current_browser = None
                current_version = None
                for tag in ua_div:
                    if tag.name == 'h3':
                        current_browser = browser_name = tag.get_text()
                        browsers[browser_name] = list()

                    if tag.name == 'h4':
                        current_version = version_name = tag.get_text()

                    agents = list()
                    if tag.name == 'ul':
                        for li in tag:
                            if li.name == 'li':
                                agents.append(li.get_text())
                    if current_version and agents:
                        browsers[current_browser].append({current_version : agents})

            else:
                logging.info('SOUP; No HTML data was returned!')

            if browsers:
                with open(filenames[i], 'w') as jsonfile:
                    json.dump(browsers, jsonfile, indent=4)

################################################################################
if __name__ == '__main__':
    current_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d.%H%M%S')
    logging_file = 'logs/uascraper-%s.log' % (current_time)
    logging_format = '%(asctime)s %(message)s'
    logging.basicConfig(filename=logging_file, format=logging_format, level=logging.DEBUG)
    main()
    logging.info('Execution completed successfully')
    sys.exit()
