import ipaddress
import json

from requests.api import delete
from termcolor import colored, cprint

from cloudflare import createDNSRecord, deleteDNSRecord, getZoneRecords, isValidDNSRecord
from tailscale import getTailscaleDevice, isTailscaleIP
from config import getConfig

def main():
    config = getConfig()
    cf_recordes = getZoneRecords(config['cf-key'], config['cf-domain'])
    ts_records = getTailscaleDevice(config['ts-key'], config['ts-tailnet'])

    records_typemap = {
        4: 'A',
        6: 'AAAA'
    }

    cprint("Adding new devices:", "blue")

    # Check if current hosts already have records:
    for ts_rec in ts_records: 
        #if ts_rec['hostname'] in cf_recordes['name']:
        if any(a['name'] == ts_rec['hostname'].lower()+"."+config['cf-domain'] and a['content'] == ts_rec['address'] for a in cf_recordes):
            print("[{state}]: {host} -> {ip}".format(host=ts_rec['hostname'], ip=ts_rec['address'], state=colored("FOUND", "green")))
        else:
            ip = ipaddress.ip_address(ts_rec['address'])
            if isValidDNSRecord(ts_rec['hostname']):
                print("[{state}]: {host} -> {ip}".format(host=ts_rec['hostname'], ip=ts_rec['address'], state=colored("ADDING", "yellow")))
                createDNSRecord(config['cf-key'], config['cf-domain'], ts_rec['hostname'], records_typemap[ip.version], ts_rec['address'])
            else:
                print("[{state}]: {host}.{tld} -> {ip} -> (Hostname: \"{host}.{tld}\" is not valid)".format(host=ts_rec['hostname'], ip=ts_rec['address'], state=colored("SKIPING", "red"), tld=config['cf-domain']))




    cprint("Cleaning up old records:", "blue")
    # Check for old records:
    cf_recordes = getZoneRecords(config['cf-key'], config['cf-domain'])
    
    # set tailscale hostnames to lower cause dns is
    for i in range(len(ts_records)):
        ts_records[i]['hostname'] = ts_records[i]['hostname'].lower()
        

    for cf_rec in cf_recordes:
        if any(a['hostname'] == cf_rec['name'].split('.')[0] and a['address'] == cf_rec['content'] for a in ts_records):
            print("[{state}]: {host} -> {ip}".format(host=cf_rec['name'], ip=cf_rec['content'], state=colored("IN USE", "green")))
        else:
            if (isTailscaleIP(cf_rec['content'])):
                print("[{state}]: {host} -> {ip}".format(host=cf_rec['name'], ip=cf_rec['content'], state=colored('DELETING', "yellow")))
                deleteDNSRecord(config['cf-key'], config['cf-domain'], cf_rec['id'])
            else:
                print("[{state}]: {host} -> {ip} (IP does not belong to a tailscale host. please remove manualy)".format(host=cf_rec['name'], ip=cf_rec['content'], state=colored('SKIP DELETE', "red")))




if __name__ == '__main__':
    main()