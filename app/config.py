import configparser, os
import os.path
from sys import path

keysToImport = ['cf-key', 'cf-domain', 'ts-key', 'ts-tailnet']

def importkey(name):
    key = name

    secretPath = "/run/secrets/"+key
    if (os.path.isfile(secretPath)):
        secret = open("secretPath", "r")
        return secret.readlines()
    elif (key in os.environ):
        return os.environ.get(key)
    else:
        try:
            cfgPath = os.path.dirname(os.path.realpath(__file__))+'/config.ini'
            print(cfgPath)
            with open(path, 'r') as file:
                config = configparser.ConfigParser()
                config.read(cfgPath)
                cfg=config['DEFAULT']
        except:
            exit('could not read config file')
        finally:
            try:
                out = cfg[key]
                return out
            except:
                exit('could not you read config key')
    
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
    return static

if __name__ == '__main__':
    print(getConfig())