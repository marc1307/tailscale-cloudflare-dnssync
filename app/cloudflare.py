import requests, json, re

from termcolor import cprint, colored
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
        exit(colored('getZoneId(): '+json.dumps(data['errors'], indent=2), "red"))


def getZoneRecords(token, domain, hostname=False, zoneId=False):
    if zoneId != False:
        url = "https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records?per_page=150".format(zone_identifier=zoneId)
    else:
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
        exit(colored("getZoneRecords() - error\n{}".format(json.dumps(data['errors'], indent=2)), "red"))

def createDNSRecord(token, domain, name, type, content, subdomain=None, zoneId=False, priority=False, ttl=120):
    if zoneId != False:
        url = "https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records".format(zone_identifier=zoneId)
    else:
        url = "https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records".format(zone_identifier=getZoneId(token, domain))
    if subdomain:
        fqdn = name+"."+subdomain+"."+domain
    else:
        fqdn = name+"."+domain
        
    payload={
        'type': type,
        'name': fqdn,
        'content': content,
        'ttl': ttl
    }
    headers = {
        'Authorization': "Bearer {}".format(token)
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    data = json.loads(response.text)

    if data['success'] == True:
        print("--> [CLOUDFLARE] [{code}] {msg}".format(code=response.status_code, msg=colored('record created', "green")))
        return True
    else:
        cprint("[ERROR]", 'red')
        exit("createDNSRecord():  "+json.dumps(data['errors'], indent=2))

def deleteDNSRecord(token, domain, id, zoneId=False):
    if zoneId != False:
        url = "https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records/{identifier}".format(zone_identifier=zoneId, identifier=id)
    else:
        url = "https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records/{identifier}".format(zone_identifier=getZoneId(token, domain), identifier=id)
    headers = {
        'Authorization': "Bearer {}".format(token)
    }
    response = requests.request("DELETE", url, headers=headers)
    data = json.loads(response.text)
    print("--> [CLOUDFLARE] [{code}] {msg}".format(code=response.status_code, msg=colored('record deleted', "green")))

def isValidDNSRecord(name):
    regex = "^([a-zA-Z]|\d|-|\.)*$"
    return re.match(regex, name)



if __name__ == '__main__':
    token = ""
    domain = ""
    print(getZoneId(token, domain))
    print(json.dumps(getZoneRecords(token, domain), indent=2))
