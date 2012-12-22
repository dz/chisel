# encoding: utf-8
#!/usr/bin/env python

import xmlrpclib

# Ping-o-matic the Pinging service:
ps = "http://rpc.pingomatic.com/RPC2"

# Your site's title and URL:
title = "ckunte.net"
url = "http://ckunte.net"

remoteServer = xmlrpclib.Server(ps)
ret = remoteServer.weblogUpdates.ping(title, url)
print ret['message']
