from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import OVSKernelSwitch    
from mininet.cli import CLI
from mininet.node import Host
from mininet.log import setLogLevel, info
from mininet.link import Link, TCLink
import socket
import time


class SimpleTopology(Topo):
    def build(self):
        h1 = self.addHost('h1', cls=Host, defaultRoute=None)
        h2 = self.addHost('h2', cls=Host, defaultRoute=None)
        h3 = self.addHost('h3', cls=Host, defaultRoute=None)
        h4 = self.addHost('h4', cls=Host, defaultRoute=None)

        s1 = self.addSwitch( 's1', cls=OVSKernelSwitch, failMode='standalone')
        s2 = self.addSwitch( 's2', cls=OVSKernelSwitch, failMode='standalone')

        
        #self.addLink(h1, s1, cls=TCLink, bw=10000000, delay='0.1ms', loss=0.1) #this is orgiranl
        #self.addLink(h2, s1, cls=TCLink, bw=10000000, delay='0.1ms')

        #self.addLink(h2, s1)

        
        #11-26
        self.addLink(h1, s1, cls=TCLink, bw=100000, delay='0.1ms')
        self.addLink(h1, s2, cls=TCLink, bw=100000, delay='0.1ms')
        self.addLink(h2, s1, cls=TCLink, bw=100000, delay='0.1ms')
        self.addLink(h2, s2, cls=TCLink, bw=100000, delay='0.1ms')

        self.addLink(h3, s1, cls=TCLink, bw=100000, delay='0.1ms')
        self.addLink(h3, s2, cls=TCLink, bw=100000, delay='0.1ms')
        self.addLink(h4, s1, cls=TCLink, bw=100000, delay='0.1ms')
        self.addLink(h4, s2, cls=TCLink, bw=100000, delay='0.1ms')
        


def main():
    topo = SimpleTopology()
    net = Mininet( topo=topo, autoSetMacs=True, build=False, ipBase="10.0.0.0/24")

#    net.build()
    net.start()

    h1 = net.getNodeByName('h1')
    h2 = net.getNodeByName('h2')
    h3 = net.getNodeByName('h3')
    h4 = net.getNodeByName('h4')

    h1.setIP(intf="h1-eth0", ip="10.0.0.1/24")
    h2.setIP(intf="h2-eth0", ip="10.0.0.2/24")
    h3.setIP(intf="h3-eth0", ip="10.0.0.3/24")
    h4.setIP(intf="h4-eth0", ip="10.0.0.4/24")
    
    """
    print("h4 as server h1 h2 h3 client:")
    h4.cmd('iperf -s &')

    for h in [h1, h2, h3]:
        h.cmd('iperf -c 10.0.0.4 -t 60 &')

    print()
    """

    src, dst = net.hosts[0], net.hosts[2]
    s_bw, c_bw = net.iperf([src, dst], seconds=10)
    info(s_bw)
    print()
    
    src, dst = net.hosts[0], net.hosts[3]
    s_bw, c_bw = net.iperf([src, dst], seconds=10)
    info(s_bw)
    print()
    
    src, dst = net.hosts[1], net.hosts[2]
    s_bw, c_bw = net.iperf([src, dst], seconds=10)
    info(s_bw)
    print()
    
    src, dst = net.hosts[1], net.hosts[3]
    s_bw, c_bw = net.iperf([src, dst], seconds=10)
    info(s_bw)
    print()
    
    # added 23-11-09
    print("ping from h1 to h3")
    result = h1.cmd('ping -c 10', "10.0.0.3")
    lines = result.split('\n')
    print("the result of ping is ", lines[-2])
    print()

    print("ping from h1 to h4")
    result = h1.cmd('ping -c 10', "10.0.0.4")
    lines = result.split('\n')
    print("the result of ping is ", lines[-2])
    print()

    print("ping from h2 to h3")
    result = h2.cmd('ping -c 10', "10.0.0.3")
    lines = result.split('\n')
    print("the result of ping is ", lines[-2])
    print()
    
    print("ping from h2 to h4")
    result = h2.cmd('ping -c 10', "10.0.0.4")
    lines = result.split('\n')
    print("the result of ping is ", lines[-2])
    print()
    #
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    main()
