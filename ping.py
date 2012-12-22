# encoding: utf-8
#!/usr/bin/env python
# Ned Batchelder ( http://nedbatchelder.com/ )
import xmlrpclib
pm = "http://rpc.pingomatic.com/RPC2"
remoteServer = xmlrpclib.Server(pm)
ret = remoteServer.weblogUpdates.ping(
    "ckunte.net",
    "http://ckunte.net"
    )
print ret['message']