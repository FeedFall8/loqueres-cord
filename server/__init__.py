import socket,datetime,random,time,json,os,sys

from _thread import *
try:
    plugininfo = json.load(open('plugins.json'))
except FileNotFoundError:
    f = open('plugins.json','w')
    json.dump({'pluginfolder':"",'plugins':[]},f,indent=4)
    f.close()
    plugininfo = json.load(open('plugins.json'))
class message:
    def __init__(self,text):
        self.text=text
        self.time=time.time()
class plugin:
    def __init__(self,name,script):
        self.name=name
        self.script=script
    def run(self,args):
        self.script.run(args)
class plugin_manager:
    plugins = []
    def load_plugins():
        sys.path.append(plugininfo['pluginfolder'])
        for file in plugininfo['plugins']:
            print(f"attempting to load:{file}")
            p = __import__(file)#os.path.join(os.path.abspath(''),os.path.join(plugininfo['pluginfolder'],file)))
            plugin_manager.plugins.append(plugin(file,p))
            print(f"loaded:{file}")
    def run_plugins(**inputs):
        for plugin in plugin_manager.plugins:
            plugin.run(inputs)
            

def blank(**args):
    pass
def hostname():
    return socket.gethostname()
def gethostbyname(name):
    return socket.gethostbyname(name)
class Client:
    def __init__(self,ip,port):
        self.ip=ip
        self.port=port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.freply = self.socket.connect((ip,port))
        self.replyfromserver=None
    def send(self,data):
        self.socket.send(data)
        
        #return self.socket.recv(1024)
    def recv(self,len=8024):
        return self.socket.recv(len)
    pass
class Connection:
    def __init__(self,connection,addr):
        self.conn=connection
        self.addr=addr
        
class Packet:
    def __init__(self,data={}):
        self.data=data
class Server:
    def __init__(self,ip=socket.gethostbyname(socket.gethostname()),port=19132,maxconnections=2):
        self.ip=ip
        self.port=port
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.data = {}
        self.recvsize=8024
        self.running=False
        self.OnDataBehavior=blank
        self.mainbehavior=blank
       
        try:
            self.server.bind((ip,port))
        except Exception as e:
            print(f'failed to bind to addresses -> {e}')
        self.server.listen(maxconnections)
    def threaded_client(self,client,log=False):
        cs={"closeconnection":False,"banip":False}
        try:
            while self.running == True:
                if  cs["closeconnection"]==True:
                    print('closing connection to: ',client)
                    break
                #plugin_manager.run_plugins(log=log,Client=client)
                self.mainbehavior(Client=client)
                #print(self.running)
                if self.running==False:
                    raise RuntimeError("server: thread shutdown")
                data = client.conn.recv(self.recvsize)
                #data is data gotten from client
                if data:
                    if log:
                        print(f"recv {data}")
                    self.OnDataBehavior(data=data,Client=client)
                    plugin_manager.run_plugins(log=log,Client=client,data=data,cs=cs)
                else:
                    if log:
                        print(f'communication ended with {client}')
                    break
        except Exception as e:
            print('error: ',e)
    def run(self,log=False,threaded=False,firstreply=None):
        plugin_manager.load_plugins()
        self.running=True
        while self.running==True:
            plugin_manager.run_plugins(log=log,threading=threaded,firstreply=firstreply)
            #print('main',self.running)
            if self.server==False:
                raise RuntimeError("Server: Connection Acception system, shutdown")
            con,addr = self.server.accept()
            if log:
                print(f"connected to server {addr} at {datetime.datetime.now()}")
            connection = Connection(con,addr)
            if not threaded:
                self.threaded_client(connection,log)
            if threaded:
                start_new_thread(self.threaded_client,(connection,log))
        self.running=False

    def stop(self):
        self.running=False
        raise RuntimeError("Server shutdown initiated")
    

##while True:
##    # wait for a connection
##    print ('waiting for a connection')
##    connection, client_address = sock.accept()
##
##    try:
##        # show who connected to us
##        print ('connection from', client_address)
##
##        # receive the data in small chunks and print it
##        while True:
##            data = connection.recv(64)
##            if data:
##                # output received data
##                print ("Data: %s" % data)
##            else:
##                # no more data -- quit the loop
##                print ("no more data.")
##                break
##    finally:
##        # Clean up the connection
##        connection.close()
