# encoding: utf-8
#!/usr/bin/env python
# Ned Batchelder ( http://nedbatchelder.com/ )
import xmlrpclib

remoteServer = xmlrpclib.Server("http://rpc.pingomatic.com/RPC2")
ret = remoteServer.weblogUpdates.ping(
    "ckunte.net",
    "http://ckunte.net"
    )
print ret['message']