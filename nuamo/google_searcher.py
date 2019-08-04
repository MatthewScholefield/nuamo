import time
from time import sleep

import random
import re
import requests
from requests import Response


class GoogleSearcher:
    def __init__(self, search_delay=2, user_agent=None):
        self.search_delay = search_delay
        self.params = {"tbs": "li:1"}
        self.headers = {
            'User-Agent': user_agent or 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/59.0'
        }
        self.next_search_time = time.time()

    def get_num_results(self, query):
        r = self.search(query)
        if 'No result' in r.text or 'did not match any' in r.text:
            return 0
        m = re.search(r'id="resultStats">([^<]*)<', r.text)
        if not m:
            print('Unkown response from search engine.')
            return -1
        return int(''.join(c for c in m.group(1) if c.isdigit()))

    def search(self, query) -> Response:
        cur_time = time.time()
        if self.next_search_time > cur_time:
            sleep(self.next_search_time - cur_time)
        self.next_search_time = time.time() + self.search_delay + self.search_delay * random.random()

        pause = 10
        while True:
            r = requests.get('http://www.google.com/search', params=dict(self.params, q=query), headers=self.headers)
            if 'recaptcha' in r.text:
                pause *= 1 + 2 * random.random()
                print('Rate limit exceeded. Sleeping {:.2f} seconds...'.format(pause))
                sleep(pause)
                continue
            return r
