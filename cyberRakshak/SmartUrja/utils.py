import socket

def getIP():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip

