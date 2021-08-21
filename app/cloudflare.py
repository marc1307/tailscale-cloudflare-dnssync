import requests
import json

from requests.models import Response

def getZoneId(token, domain):
    url = "https://api.cloudflare.com/client/v4/zones"
    payload={}
    headers = {
    'Authorization': "Bearer {}".format(token)
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)

    if data['success']:
        for zone in data['result']:
            if zone['name'] == domain:
                return zone['id']
    else:
        exit('fuck: '+json.dumps(data['errors'], indent=2))
    


    #print(json.dumps(json.loads(response.text), indent=2))


def GetZoneRecords(token, domain, hostname=False):
    url = "https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records?per_page=150".format(zone_identifier=getZoneId(token, domain))
    payload={}
    headers = {
    'Authorization': "Bearer {}".format(token)
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)

    output = []

    if data['success']:
        for record in data['result']:
            if record['type'] in ['A', 'AAAA']:
                #print("{name} {ttl} in {type} {content}".format(name=record['name'], ttl=record['ttl'], type=record['type'], content=record['content']))
                output.append(record)
        return output
    else:
        exit('shit')

def CreateDNSRecords(token, domain, name, type, content):
    url = "https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records?per_page=150".format(zone_identifier=getZoneId(token, domain))
    payload={
        'type': type,
        'name': name+"."+domain,
        'content': content,
        'ttl': 120
    }
    headers = {
        'Authorization': "Bearer {}".format(token)
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    data = json.loads(response.text)

    if data['success'] == True:
        print("created")
        return True
    else:
        print(json.dumps(data['errors']))
        exit('fuck')

def DeleteDNSRecords(token, domain, id):
    url = "https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records/{identifier}".format(zone_identifier=getZoneId(token, domain), identifier=id)
    headers = {
        'Authorization': "Bearer {}".format(token)
    }
    response = requests.request("DELETE", url, headers=headers)
    data = json.loads(response.text)





if __name__ == '__main__':
    token = ""
    domain = ""
    print(getZoneId(token, domain))
    print(json.dumps(GetZoneRecords(token, domain), indent=2))
