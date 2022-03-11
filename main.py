
def wifi():
    import network
    try:
        with open('wifi.txt','r') as f:
            wificfg = f.read().splitlines()
        ssid = wificfg[0]
        password = wificfg[1]
    except OSError as e:
        print('error opening "wifi.txt":')
        print(e)
        return
    station = network.WLAN(network.STA_IF)
    station.active(True)
    if not station.isconnected():
        print("connecting to wifi '%s'" % (ssid))
        station.connect(ssid, password)
        while not station.isconnected():
            pass
        print('network config:', station.ifconfig())
        print('most probably you want to run "https()" now')

def ls():
    import os
    ls = os.listdir()
    for e in ls:
        print('%s: %d' % (e, os.stat(e)[6]))

def rm(name):
    import os
    os.remove(name)

def cat(name):
    with open(name,'r') as f:
        print(f.read())

def reboot():
    import machine
    machine.reset()

def https():
    from HTTPSServer import HTTPSServer
    HTTPSServer().run()

wifi()
