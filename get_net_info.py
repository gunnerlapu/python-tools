#!/usr/sbin/python

import os
import sys
import subprocess

def open_l(filename):
  hosts = []
  with open(filename) as fh:
         lines=fh.read()

  return lines

def check_host(host):
  print(host)
  p = subprocess.Popen(['ping', '-c', '2', host  ], stdin = subprocess.PIPE, stdout= subprocess.PIPE, stderr=subprocess.PIPE)
  out, ret = p.communicate()      
  return p.returncode

def parse_net(out):
  cnt = 0
  line = out
  lowest = 255 
  ip_low = 0
  net_dict = {} 
  for i in range(len(out)):
    if(line[i] == "\n"):
      cnt = 0 
    elif(cnt == 0):
      split_out = line[i].split()
     # print(split_out[0])
      split_out = (line[i+1]).split()
    # print("   " + split_out[1])
      ip_q = split_out[1].split(".")
      key_ip = ip_q[0] + "." + ip_q[1] + "." + ip_q[2] + "." + "0"
      
      if key_ip in net_dict:
         net_dict[key_ip] = ip_low
      else:
         net_dict[key_ip] = ip_low
    #  print("Network address is",key_ip)
      if(int(ip_q[3]) < lowest):
         lowest = ip_q[3]
         ip_low = split_out[1]
         net_dict[key_ip] = ip_low 
      cnt += 1 
    else:
      cnt += 1
  for k,v in net_dict.items():
        print(k + "/24",v)
  #print("lowest ip used is", ip_low)

def get_net(hosts):
  hosts = hosts.split("\n")
  for host in hosts:
      if(check_host(host) == 0):
           print("Host is alive...")
           p = subprocess.Popen(['ssh', host, 'ifconfig'  ], stdin = subprocess.PIPE, stdout= subprocess.PIPE, stderr=subprocess.PIPE)
           out = p.stdout.readlines()
           p = subprocess.Popen(['ssh', host, 'hostname'  ], stdin = subprocess.PIPE, stdout= subprocess.PIPE, stderr=subprocess.PIPE)
           print(p.stdout.read())
           parse_net(out)
      else:
          print("Host is not available", host)
  return 0
 
ret = open_l(sys.argv[1])
get_net(ret)
