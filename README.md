# tailscale-cloudflare-dnssync
Syncs Tailscale host IPs to a cloudflare hosted DNS zone.
Basically works like Magic DNS, but with your domain.
The main benefit for me is the ability to use letsencrypt with certbot + dns challenge

## Features
- Adds ipv4 and ipv6 records for all devices
- Removes DNS records for deleted devices
- Updates DNS records after the hostname/alias changes
- Checks if DNS records is part of tailscale network (100.64.0.0/12 or fd7a:115c:a1e0::/48) before deleting records :P

## Run
### Run using docker (using env var)
```
docker run --rm -it --env-file ~/git/tailscale-cloudflare-dnssync/env.txt ghcr.io/marc1307/tailscale-cloudflare-dnssync:main
```
Envfile:
```env
cf-key=<cloudflare api key>
cf-domain=<cloudflare target zone>
ts-key=<tailscale api key>
ts-tailnet=<tailnet>
```
tailnet can be found at the top of the tailscale admin page

### Run using docker (using secrets)
tbd

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
1. Login to Tailscale website
2. Create API key at: https://login.tailscale.com/admin/settings/authkeys

