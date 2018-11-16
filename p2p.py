import socket #'NF CERF VTYZ E;T PFT,FKF!!!!! FKTYF [ETXRJ ,KZNM! CEXRF, ',FYFNRF!!!!!!!!!

class Peer(object):
    s = None
    isudp = False
    serv = ('',0)
    def __init__(self,serv):
        self.s = socket.socket()
        self.serv = serv
        return
    def connect(self,username):
        self.s.connect(self.serv)
        self.s.send('c ')
        self.s.send(username)
        try:
            self.s.settimeout(10)
        except:
            self.s.close()
            print "Server is unavaible"
            return
        adr = self.s.recv(124)
        if adr == "er"*64:
            print username+" is unavaible"
            return
        else:
            self.s.close()
            return (adr.replace('`','').split(':')[0],int(adr.replace('`','').split(':')[1]))
    def recv(self,user_name,ip,port):
        self.s.connect(self.serv)
        self.s.send('l ')
        self.s.send(user_name)
        try:
            self.s.settimeout(10)
        except:
            self.s.close()
            return 0
        if self.s.recv(2) == 'ok':
            self.s.send(port)
            self.s.send(ip+("`"*124)[:124])
            self.s.close()
            return 1
        self.s.close()
        return 0
            
class Server(object):
    s = None
    def handle(self,port):
        try:
            self.s = socket.socket()
            self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            self.s.bind(('',int(port)))
            self.s.listen(1)
            conn,addr = self.s.accept()
            r = conn.recv(2)
            if r == 'c ':
                uname = conn.recvfrom(16)
                f = open('db')
                usr = f.read()
                f.close()
                usrl = usr.replace('\n','^').split('^')
                usrd = dict(zip(usrl[::2], usrl[1::2]))
                conn.send((usrd[str(uname[0])]+"`"*124)[:124])
                conn.close()
                self.s.shutdown(2)
                self.s.close()
                return
            if r == 'l ':
                user_name = conn.recv(16)
                conn.send('ok')
                port = conn.recv(4)
                ip = conn.recv(124)
                f = open('db','a')
                f.write(user_name+'^'+ip.replace('`','')+':'+str(port)+'\n')
                f.close()
                self.s.close()
                return
        except Exception as e:
            print "Error!"
            print e
            self.s.shutdown(2)
            self.s.close()
            return
