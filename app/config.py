import configparser, os
import os.path
from sys import path
from termcolor import cprint

keysToImport = ['cf-key', 'cf-domain', 'ts-tailnet']
keysOptional = ['cf-sub', 'prefix', 'postfix', 'ts-key', 'ts-client-id', 'ts-client-secret', "mode", "hs-baseurl", "hs-apikey", 'ignore-ipv6', 'wildcardhost']

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

    # check for tailscale config
    if static['mode'] == "" or static['mode'] == "tailscale":
        static['mode'] = "tailscale"
        if not static['ts-key'] and not (static['ts-client-id'] and static['ts-client-secret']):
            cprint("ERROR: mandatory tailscale configuration not found: ts-key or ts-client-id/ts-client-secret missing", "red")
            exit(1)
    # check for headscale Config
    if static['mode'] == "headscale":
        if not (static['hs-baseurl'] and static['hs-apikey']):
            cprint("ERROR: mandatory headscale configuration not found: hs-baseurl and/or hs-apikey missing", "red")
            exit(1)
    # unkown mode unfigured
    if static['mode'] not in ["", "tailscale", "headscale"]:
        cprint("ERROR: unknown mode configured (got: {mode})".format(mode=static['mode']), "red")
        exit(1)

    return static

if __name__ == '__main__':
    from pprint import pprint
    pprint(getConfig())
