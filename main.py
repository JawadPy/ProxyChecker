import socket, json
from requests import get as GET

def isProxyUp(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def checkAllProxies(proxies):
    output = list()
    for proxy in proxies:
        p = proxy.split(':')
        if isProxyUp(p[0], p[1]):
            output.append(proxy)
    
    return output

def main(online=False):
    if not online:
        with open('proxylist.txt','a+') as p:
            output = checkAllProxies(p.readlines())
    else:
        output = list()
        for proxy in (
            GET('https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
            ).text.split('\n')):
            proxy = json.loads(proxy)

            if type(proxy['type']) is list:
                t = proxy['type'][0]
            else:
                t = proxy['type']

            if isProxyUp(proxy['host'], proxy['port']):
                proxy = '{}://{}:{}'.format(
                        t,
                        str(proxy['host']),
                        str(proxy['port'])
                    )
                output.append(proxy)
                print(proxy)


    with open('output.txt', 'a+') as o:
        o.writelines('\n'.join(i for i in output))

if __name__ == '__main__':
    # online=False will make it check proxylist.txt file
    # then print out proxies any up proxy in output.txt
    main(online=True) 