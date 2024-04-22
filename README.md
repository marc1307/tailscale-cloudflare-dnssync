# tailscale-cloudflare-dnssync
Syncs Tailscale host IPs to a cloudflare hosted DNS zone.
Basically works like Magic DNS, but with your domain.
The main benefit for me is the ability to use letsencrypt with certbot + dns challenge

## Features
- Adds ipv4 and ipv6 records for all devices
- Removes DNS records for deleted devices
- Updates DNS records after the hostname/alias changes
- Add a pre- and/or postfixes to dns records
- Checks if DNS records is part of tailscale network (100.64.0.0/12 or fd7a:115c:a1e0::/48) before deleting records :P


## Run
### Run using docker (using env var)
```shell
docker run --rm -it --env-file ~/git/tailscale-cloudflare-dnssync/env.txt ghcr.io/marc1307/tailscale-cloudflare-dnssync:latest
```
Envfile:
```env
cf-key=<cloudflare api key>
cf-domain=<cloudflare target zone>
#cf-sub=<subdomain to use, optional>
ts-key=<tailscale api key>
ts-tailnet=<tailnet>
#ts-clientid=<oauth clientid, optional>
#ts-clientsecret=<oauth clientsecret, optional>
#prefix=<prefix for dns records, optional>
#postfix=<postfix for dns records, optional>
```
> **ts-tailnet** can be found in the [Tailscale Settings](https://login.tailscale.com/admin/settings/general)
```Settings -> General -> Organization``` or at the top left on the admin panel.

### Run using docker (using secrets)
```yaml
version: "3"

secrets:
  cf-key:
    file: "./cloudflare-key.txt"
  ts-key:
    file: "./tailscale-key.txt"
  ts-clientid:
    file: "./tailscale-clientid.txt"
  ts-clientsecret:
    file: "./tailscale-clientsecret.txt"

services:
  cloudflare-dns-sync:
    image: ghcr.io/marc1307/tailscale-cloudflare-dnssync:latest
    environment:
      - ts_tailnet=<tailnet>
      - cf_domain=example.com
      - cf_sub=sub      # optional, uses sub domain for dns records
      - prefix=ts-      # optional, adds prefix to dns records
      - postfix=-ts     # optional, adds postfix to dns records
    secrets:
      - cf-key
      - ts-key
```

### Run native using python
tbd

## How to get API Keys
### Cloudflare
1. Login to Cloudflare Dashboard
2. Create API Key at https://dash.cloudflare.com/profile/api-tokens
3. Template: Edit Zone
4. Permissions: 
```
Permission | Zone - DNS - edit
Resource | include - specific zone - <your zone>
```

### Tailscale

#### API Key
1. Login to Tailscale website
2. Create API key at: https://login.tailscale.com/admin/settings/authkeys

#### Oauth
1. Login to Tailscale website
2. Create Oauth client at: https://login.tailscale.com/admin/settings/oauth with Devices Read permission
