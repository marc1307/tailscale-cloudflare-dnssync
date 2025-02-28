import requests, json
from termcolor import colored
from tailscale import alterHostname

def getHeadscaleDevice(apikey, baseurl):
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
                    output.append({'hostname': alterHostname(device['givenName'].split('.')[0].lower()), 'address': address})
        return output
    else:
        exit(colored("getTailscaleDevice() - {status}, {error}".format(status=str(response.status_code), error=data['message']), "red"))
