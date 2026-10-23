#!/usr/bin/env python3
"""Explicit-target DNS / HTTPS health probe; never discovers or scans a subnet."""
import argparse
import socket
import ssl
import urllib.parse
import urllib.request

p=argparse.ArgumentParser()
p.add_argument('--host',help='Your server hostname to resolve')
p.add_argument('--url',help='Your own authorized HTTP(S) URL to test')
a=p.parse_args()
if not a.host and not a.url: p.error('provide --host or --url')
host=a.host or urllib.parse.urlparse(a.url).hostname
if not host: p.error('host cannot be parsed')
try:
    ips=sorted({x[4][0] for x in socket.getaddrinfo(host,None)})
    print('DNS OK:',host,', '.join(ips))
except OSError as e:
    print('DNS ERROR:',type(e).__name__,str(e))
if a.url:
    url=urllib.parse.urlparse(a.url)
    if url.scheme not in ('http','https'): p.error('only http/https allowed')
    request=urllib.request.Request(a.url, method='HEAD',headers={'User-Agent':'LiangYou-Network-Diagnose/1.0'})
    try:
        with urllib.request.urlopen(request,timeout=8) as r:
            print('HTTP:',r.status,'final host:',urllib.parse.urlparse(r.url).hostname)
    except Exception as e:
        print('HTTP CHECK:',type(e).__name__,str(e)[:180])
