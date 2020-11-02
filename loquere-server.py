server=__import__('server')
Server = server.Server()
lastmsg=b""
messages = []
clients=[]
import pickle,_thread,time
def kick(connection):
    connection.conn.sendall(b'A' * 999999)
def console(*arg):
    while True:
        command = input('')
        try:
            exec(command)
        except Exception as e:
            print('console error:',e)
def before(**arg):
    c = arg['Client']
    
def system(**arg):
    global lastmsg,messages,clients
    c = arg['Client']
    if c not in clients:
        clients.append(c)
    lastmsg=arg['data'].decode()
    if len(lastmsg) < 300:
        if "/reload" not in lastmsg:
            print(lastmsg)
            messages.append(server.message(lastmsg))
        if lastmsg != "" and lastmsg != "/reload":
            print('sending data:',arg['data'],'<to>',c)
            c.conn.sendall(pickle.dumps(messages))
        
       
            
        
                
            #print("sending reply:",lastmsg)
        if lastmsg == "/reload":
            c.conn.sendall(pickle.dumps(messages))
    else:
        c.conn.sendall(pickle.dumps([server.message('server: too many characters!')]))
def threadcleanup(*args):
    global messages
    while True:
        time.sleep(5)
        messages = []
_thread.start_new_thread(console,(0,0))
_thread.start_new_thread(threadcleanup,(0,0))
Server.OnDataBehavior = system
Server.run(0,1)
