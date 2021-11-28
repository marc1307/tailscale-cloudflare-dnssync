import requests, json
import ipaddress
from requests.auth import HTTPBasicAuth
from termcolor import colored

### Get Data
def getTailscaleDevice(apikey, tailnet):
    url = "https://api.tailscale.com/api/v2/tailnet/{tailnet}/devices".format(tailnet=tailnet)
    payload={}
    headers = {
    }
    response = requests.request("GET", url, headers=headers, data=payload, auth=HTTPBasicAuth(username=apikey, password=""))
    # print(response.text)
    # print(json.dumps(json.loads(response.text), indent=2))

    output=[]

    data = json.loads(response.text)
    if (response.status_code == 200):
        output = []
        for device in data['devices']:
            #print(device['hostname']+": "+json.dumps(device['addresses']))
            for address in device['addresses']:
                output.append({'hostname': alterHostname(device['hostname']), 'address': address})
                if device['name'].split('.')[0].lower() != device['hostname'].lower():
                    output.append({'hostname': alterHostname(device['name'].split('.')[0].lower()), 'address': address})
        return output
    else:
        exit(colored("getTailscaleDevice() - {status}, {error}".format(status=str(response.status_code), error=data['message']), "red"))

def isTailscaleIP(ip):
    ip = ipaddress.ip_address(ip)

    if (ip.version == 6):
        if (ip in ipaddress.IPv6Network('fd7a:115c:a1e0::/48')):
            return True
        else:
            return False
    elif (ip.version == 4):
        if (ip in ipaddress.IPv4Network('100.64.0.0/10')):
            return True
        else:
            return False
    else:
        exit("isTailscaleIP(): - unknown IP version")

def alterHostname(hostname):
    from config import getConfig
    config = getConfig()
    pre = config.get("prefix", "")
    post = config.get("postfix", "")

    newHostname = "{pre}{hostname}{post}".format(pre=pre, post=post, hostname=hostname)
    return newHostname

if __name__ == '__main__':
    print(json.dumps(getTailscaleDevice(), indent=2))