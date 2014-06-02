#coding=utf-8
from logger import logger as rlogger
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import struct


client_pc={}
client_dev={}
"""
get the package id
"""
def get_syn_id(r_data):
    if r_data!=None and len(r_data)>14:
        head =struct.unpack("<H8sI",r_data[:14])
        return (head[0],head[2])
    else:
        return (0,0)

"""
the protocol dowith the package
"""
class tudpProtocol(DatagramProtocol):
    def __init__(self):
        pass
    def datagramReceived(self, data, addr):
        rlogger.message("recieve data from %s :%d"%(addr))
        syn,dev_id = get_syn_id(data)
        if syn!=0:
            t_data=list(data)
            if syn==0x7F00:
                t_data[0]=0xFF
                client_dev[dev_id]=addr
                rlogger.message("add dev %d"%(dev_id))
                des = client_pc.get(dev_id)
                if des!=None:
                    res_data = ''.join([chr(i) for i in t_data])
                    self.transport.write(res_data,des)
            if syn==0x7FF:
                t_data[0]=0x00
                client_pc[dev_id]=addr
                rlogger.message("add pc %d"%(dev_id))
                des=client_dev.get(dev_id)
                if des!=None:
                    res_data = ''.join([chr(i) for i in t_data])
                    self.transport.write(res_data,des)
        else:
            rlogger.message("recieve wrong package")

def run_udp(port):
    reactor.listenUDP(port,tudpProtocol())
    reactor.run()
    pass

class client:
    '''
    The class contain the client paires
    '''
    def __init__ (self,host,port):
        self.host = host
        self.port = port

    def get_socket (self):
        return (self.host,self.port)

if __name__ == '__main__':
    rlogger.debug("server run")
    run_udp(10047)
