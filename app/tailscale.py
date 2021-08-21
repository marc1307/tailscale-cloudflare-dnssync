import requests, json
from requests.auth import HTTPBasicAuth

### Get Data
def getTailscaleDevice(apikey):
    url = "https://api.tailscale.com/api/v2/tailnet/marc1307.de/devices"
    payload={}
    headers = {
    }
    response = requests.request("GET", url, headers=headers, data=payload, auth=HTTPBasicAuth(username=apikey, password=""))
    #print(response.text)
    #print(json.dumps(json.loads(response.text), indent=2))

    output=[]

    if (response.status_code == 200):
        data = json.loads(response.text)
        output = []
        for device in data['devices']:
            #print(device['hostname']+": "+json.dumps(device['addresses']))
            for address in device['addresses']:
                output.append({'hostname': device['hostname'], 'address': address})
                if device['name'].split('.')[0].lower() != device['hostname'].lower():
                    output.append({'hostname': device['name'].split('.')[0].lower(), 'address': address})
        return output
    else:
        exit('fuck')

if __name__ == '__main__':
    print(json.dumps(getTailscaleDevice(), indent=2))