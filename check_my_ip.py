import requests
print(requests.get('https://api.myip.com').json()['ip'])