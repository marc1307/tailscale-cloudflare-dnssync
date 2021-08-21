import ipaddress
import json

from requests.api import delete

from cloudflare import CreateDNSRecords, DeleteDNSRecords, GetZoneRecords
from tailscale import getTailscaleDevice
from config import getConfig

def main():
    config = getConfig()
    cf_recordes = GetZoneRecords(config['cf-key'], config['cf-domain'])
    ts_records = getTailscaleDevice(config['ts-key'])

    records_typemap = {
        4: 'A',
        6: 'AAAA'
    }

    # Check if current hosts already have records:
    for ts_rec in ts_records: 
        #if ts_rec['hostname'] in cf_recordes['name']:
        if any(a['name'] == ts_rec['hostname'].lower()+"."+config['cf-domain'] and a['content'] == ts_rec['address'] for a in cf_recordes):
            print("yay record found :) {host} -> {ip}".format(host=ts_rec['hostname'], ip=ts_rec['address']))
        else:
            print("record not found :( {host} -> {ip}".format(host=ts_rec['hostname'], ip=ts_rec['address']))
            ip = ipaddress.ip_address(ts_rec['address'])
        
            CreateDNSRecords(config['cf-key'], config['cf-domain'], ts_rec['hostname'], records_typemap[ip.version], ts_rec['address'])

    # Check for old records:
    cf_recordes = GetZoneRecords(config['cf-key'], config['cf-domain'])
    
    # set tailscale hostnames to lower cause dns is
    for i in range(len(ts_records)):
        ts_records[i]['hostname'] = ts_records[i]['hostname'].lower()
        

    for cf_rec in cf_recordes:
        if any(a['hostname'] == cf_rec['name'].split('.')[0] and a['address'] == cf_rec['content'] for a in ts_records):
            print("yay :) {host} -> {ip}".format(host=cf_rec['name'], ip=cf_rec['content']))
        else:
            print("nay :( {host} -> {ip}".format(host=cf_rec['name'], ip=cf_rec['content']))
            DeleteDNSRecords(config['cf-key'], config['cf-domain'], cf_rec['id'])
            print("deleted")


if __name__ == '__main__':
    main()