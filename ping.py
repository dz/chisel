import xmlrpclib

remoteServer = xmlrpclib.Server("http://rpc.pingomatic.com/RPC2")
ret = remoteServer.weblogUpdates.ping(
    "ckunte.net",
    "http://ckunte.net"
    )
print ret['message']
