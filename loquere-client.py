server=__import__('server')
version='1.0.1'
import time
import _thread
import threading,pickle,os
def runserver():
    try:
        os.system('loquere-server.py')
    except Exception as e:
        print("error:",e)
    
def hub():
    print(f'loquere chat client {version}')
    modes=['host - type to host a server','chat - type to chat']
    print('====modes=====')
    for m in modes:
        print(m)
    print('==============')
    mode = input('mode: ')
    
    if mode == 'host':
        runserver()
    if mode == 'chat':
        main()
def main():
    
    print(f'loquere chat lient {version}')
    
    
    print("server list\n===================")
    for ip in open("servers.txt"):
        print(ip)
    print("===============")
    info=input("connect > IP/port:")
    try:
        client = server.Client(info.split(':')[0],int(info.split(':')[1]))
    except  Exception as e:
        print(f"loquire-error: there was a error connecting to the server, the server may be offline error: {e}; Rebooting of loquere will now begin")
        time.sleep(1)
        print(' '*9000)
        print('rebooted!')
        main()
    #_thread.start_new_thread(cm,(client,0,0))
    ng=[]
    def sendmsg(*arg):
        while True:
            #print(' ')
            #time.sleep(1)
            msg = input('')
            if msg != "" or not "/reload" in msg:
                client.send(msg.encode())
            
            
##            reply = client.recv()
##            messages = pickle.loads(reply)
##            for i in messages:
##                if i.time not in ng:
##                    print(i.text)
##                    ng.append(i.time)
           
        #print(client.replyfromserver)
    def reload(ng,somethin=1):
        time.sleep(.1)
        client.send(b'/reload')
        reply = client.recv()
        
            
        messages = pickle.loads(reply)
        for i in messages:
            if i.time not in ng and not '/reload' in i.text:
                print(">",i.text + '\n')
                ng.append(i.time)
    _thread.start_new_thread(sendmsg,(0,0))
    while True:
        reload(ng)
            
    
hub()
