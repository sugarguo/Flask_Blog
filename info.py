#! usr/bin/python
#  -_-  coding:utf-8 -_-

'''
@author          sugarguo

@email           sugarguo@live.com

@date            2016年04月18日

@version         v1.0.0 

@copyright       Sugarguo

File             info.py

'''



#from __future__ import print_function
from collections import OrderedDict
from collections import namedtuple
import os


def netdevs():
    ''' RX and TX bytes for each of the network devices '''
 
    with open('/proc/net/dev') as f:
        net_dump = f.readlines()
     
    device_data={}
    data = namedtuple('data',['rx','tx'])
    for line in net_dump[2:]:
        line = line.split(':')
        if line[0].strip() != 'lo':
            device_data[line[0].strip()] = data(float(line[1].split()[0])/(1024.0*1024.0),
                                                float(line[1].split()[8])/(1024.0*1024.0))
     
    return device_data


def process_list():
    pids = []
    for subdir in os.listdir('/proc'):
        if subdir.isdigit():
            pids.append(subdir)
 
    return pids


def meminfo():
    ''' Return the information in /proc/meminfo
    as a dictionary '''
    #meminfo=OrderedDict()
    meminfo = {}

    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    return meminfo

if __name__=='__main__':
    meminfo = meminfo()
    pids = process_list()
    netdevs = netdevs()
    
    print netdevs.keys()[2]
    
    print('{0}: {1} MiB {2} MiB'.format(netdevs.keys()[2], netdevs[netdevs.keys()[2]].rx, netdevs[netdevs.keys()[2]].tx))
    #for dev in netdevs.keys():
        #print('{0}: {1} MiB {2} MiB'.format(dev, netdevs[dev].rx, netdevs[dev].tx))
    
    print('Total number of running processes: {0}'.format(len(pids)))
    
    print float(meminfo['MemTotal'][:-3]) - float(meminfo['MemFree'][:-3])
    
    print('Total memory: {0}'.format(meminfo['MemTotal']))
    print('Free memory: {0}'.format(meminfo['MemFree']))
