import requests
import json
import sys


######
domain='example.com'                            #主域名
subdomain4='4.example.com'                      #v4域名
subdomain6='6.example.com'                      #v6域名
username='username'                             #cloudflare登录名
apikey='aaaaaaaaaaaaaaaaa'                      #Global API Key
v4_flag=1                                       #是否解析ipv4,
v6_flag=1                                       #是否解析ipv6
######

headers = {
    "Content-Type": "application/json",
    "X-Auth-Email": username,
    "X-Auth-Key": apikey
}

#查询主域名id
url_list_zones = "https://api.cloudflare.com/client/v4/zones"
response = requests.request("GET", url_list_zones, headers=headers)
zone_list=json.loads(response.text)['result']

for dic in zone_list:
    if dic['name'] == domain:
        domainid=dic['id']
        url_list_dns_records = 'https://api.cloudflare.com/client/v4/zones/'+domainid+'/dns_records'
if domainid == None:
    print('未查询到域名信息，退出')
    sys.exit(0)

#查询子域名id
def list_dns_records(subdomain):
    response = requests.request("GET", url_list_dns_records, headers=headers)
    dns_records=json.loads(response.text)['result']

    for dic in dns_records:
        if dic['name'] == subdomain:
            subdomainid=dic['id']
            return(subdomainid)
    if subdomainid == None:
        print('未查询到解析记录，退出')
        sys.exit(0)

#解析v4
if v4_flag == 1:
    ipv4 = requests.get('https://4.ipw.cn').text.strip()
    url_update_dns_records = url_list_dns_records + '/'+list_dns_records(subdomain4)
    payload = {
        "content": ipv4,
        "name": subdomain4,
        "proxied": False,
        "type": "A",
        "ttl": 0
    }
    response = requests.request("PUT", url_update_dns_records, json=payload, headers=headers)
    print(response.text)

#解析v6
if v6_flag == 1:
    ipv6 = requests.get('https://6.ipw.cn').text.strip()
    url_update_dns_records = url_list_dns_records + '/'+list_dns_records(subdomain6)
    payload = {
        "content": ipv6,
        "name": subdomain6,
        "proxied": False,
        "type": "AAAA",
        "ttl": 0
    }
    response = requests.request("PUT", url_update_dns_records, json=payload, headers=headers)
    print(response.text)