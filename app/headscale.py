import requests, json, ipaddress
from termcolor import colored
from tailscale import alterHostname

def getHeadscaleDevice(apikey, baseurl, ignoreipv6=False, wildcardhost=False):
    url = "{baseurl}/api/v1/node".format(baseurl=baseurl)
    payload={}
    headers = {
        "Authorization": "Bearer {apikey}".format(apikey=apikey)
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    output=[]

    data = json.loads(response.text)
    if (response.status_code == 200):
        output = []
        for device in data['nodes']:
            for address in device['ipAddresses']:
                if not device['givenName'].lower().startswith('localhost'):
                    ip = ipaddress.ip_address(address)
                    if ip.version == 6 and ignoreipv6:
                        continue
                    output.append({'hostname': alterHostname(device['givenName'].split('.')[0].lower()), 'address': address})
                    if wildcardhost:
                        output.append({'hostname': "*.{host}".format(host=alterHostname(device['givenName'].split('.')[0].lower())), 'address': address})
        return output
    else:
        exit(colored("getTailscaleDevice() - {status}, {error}".format(status=str(response.status_code), error=data['message']), "red"))
