# python=3.11
# 공공데이터 api 파이썬 3.10 이상에서 호출시 SSLError 해결
# 공공데이터에서는 파이썬 3.9 버전을 권장하고 있음

import requests
from urllib3.util.ssl_ import create_urllib3_context
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

class SSLAdapter(HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)

# SSL/TLS 컨텍스트 생성
context = create_urllib3_context()
context.set_ciphers('DEFAULT@SECLEVEL=1')

url = '공공데이터api'

session = requests.Session()
adapter = SSLAdapter(ssl_context=context)
session.mount('https://', adapter)

response = session.get(url)
response.raise_for_status()

# 인코딩을 UTF-8로 설정
response.encoding = 'utf-8'
data = response.text

print(data)
