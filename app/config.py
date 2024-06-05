import configparser, os
import os.path
from sys import path
from termcolor import cprint

keysToImport = ['cf-key', 'cf-domain', 'ts-tailnet']
# maybe ts-client-id & ts-client-secret are better for names ?
keysOptional = ['cf-sub', 'prefix', 'postfix', 'ts-key', 'ts-clientid', 'ts-clientsecret']

def importkey(name, optional=False):
    key = name
    envKey = key.replace("-", "_")

    secretPath = "/run/secrets/"+key
    if (os.path.isfile(secretPath)):
        secret = open(secretPath, "r")
        out = "{}".format(secret.readline().strip())
        return out
    elif (key in os.environ):
        return os.environ.get(key)
    elif (envKey in os.environ):
        return os.environ.get(envKey)
    else:
        try:
            cfgPath = os.path.dirname(os.path.realpath(__file__))+'/config.ini'
            with open(cfgPath, 'r') as file:
                config = configparser.ConfigParser()
                config.read(cfgPath)
                cfg=config['DEFAULT']
        except Exception as e:
            print(e)
            if optional:
                return ""
            exit('could not read config file')
        finally:
            try:
                out = cfg[key]
                return out
            except:
                if optional:
                    return ""
                cprint("ERROR: mandatory configuration not found: {}".format(key), "red")
    
def getConfig():
    # static = {
    #     'cf-key': '',
    #     'cf-domain': "".lower(),
    #     'ts-key': 'tskey-',
    #     'ts-tailnet': ''
    # }
    static = {}
    for key in keysToImport:
        static[key] = importkey(key)
    for key in keysOptional:
        static[key] = importkey(key, True)
    if not static['ts-key'] and not (static['ts-clientid'] and static['ts-clientsecret']):
        cprint("ERROR: mandatory tailscale configuration not found: ts-key or ts-clientid/ts-clientsecret missing", "red")
        exit(1)
    return static

if __name__ == '__main__':
    print(getConfig())
