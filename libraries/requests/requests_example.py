""" python requests example """
import requests  # make http requests

# http = Hypertext Transfer Protocol
# https = Hypertext Transfer Protocol Secure
# secure = encrypted using Transport Layer Security (TLS) or, formerly, Secure Sockets Layer (SSL)

URL_EXAMPLE = "https://www.okx.com/api/v5/public/instruments"
params = {"instType": "SPOT"}
headers = {}

r = requests.get(URL_EXAMPLE, headers=headers, params=params, timeout=10)

r_content = r.content
r_json = r.json()
r_text = r.text
r_headers = r.headers
r_encoding = r.encoding
