import ipaddress
import json

from requests.api import delete
from termcolor import colored, cprint

from cloudflare import createDNSRecord, deleteDNSRecord, getZoneRecords, isValidDNSRecord
from tailscale import getTailscaleDevice, isTailscaleIP
from config import getConfig

import sys

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
        if config.get("cf-sub"):
            sub = "." + config.get("cf-sub")
        else:
            sub = ""
        tsfqdn = ts_rec['hostname'].lower()+sub+"."+config['cf-domain']
        if any(c['name'] == tsfqdn and c['content'] == ts_rec['address'] for c in cf_recordes):
            print("[{state}]: {host} -> {ip}".format(host=ts_rec['hostname'], ip=ts_rec['address'], state=colored("FOUND", "green")))
        else:
            ip = ipaddress.ip_address(ts_rec['address'])
            if isValidDNSRecord(ts_rec['hostname']):
                print("[{state}]: {host} -> {ip}".format(host=ts_rec['hostname'], ip=ts_rec['address'], state=colored("ADDING", "yellow")))
                createDNSRecord(config['cf-key'], config['cf-domain'], ts_rec['hostname'], records_typemap[ip.version], ts_rec['address'],subdomain=config["cf-sub"])
            else:
                print("[{state}]: {host}.{tld} -> {ip} -> (Hostname: \"{host}.{tld}\" is not valid)".format(host=ts_rec['hostname'], ip=ts_rec['address'], state=colored("SKIPING", "red"), tld=config['cf-domain']))



    cprint("Cleaning up old records:", "blue")
    # Check for old records:
    cf_recordes = getZoneRecords(config['cf-key'], config['cf-domain'])
    
    # set tailscale hostnames to lower cause dns is
    for i in range(len(ts_records)):
        ts_records[i]['hostname'] = ts_records[i]['hostname'].lower()
        

    for cf_rec in cf_recordes:
        if config.get('cf-sub'):
            sub = '.' + config.get('cf-sub')
        else: sub = ""
        cf_name = cf_rec['name'].rsplit(sub + '.' + config['cf-domain'], 1)[0]

        # Ignore any records not matching our prefix/postfix
        if not cf_name.startswith(config.get('prefix', '')):
            continue
        if not cf_name.endswith(config.get('postfix', '')):
            continue

        if any(a['hostname'] == cf_name and a['address'] == cf_rec['content'] for a in ts_records):
            print("[{state}]: {host} -> {ip}".format(host=cf_rec['name'], ip=cf_rec['content'], state=colored("IN USE", "green")))
        else:
            if (isTailscaleIP(cf_rec['content'])):
                print("[{state}]: {host} -> {ip}".format(host=cf_rec['name'], ip=cf_rec['content'], state=colored('DELETING', "yellow")))
                deleteDNSRecord(config['cf-key'], config['cf-domain'], cf_rec['id'])
            else:
                print("[{state}]: {host} -> {ip} (IP does not belong to a tailscale host. please remove manualy)".format(host=cf_rec['name'], ip=cf_rec['content'], state=colored('SKIP DELETE', "red")))




if __name__ == '__main__':
    main()