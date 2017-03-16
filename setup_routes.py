#!/usr/bin/python


#parse linux route utility output file
#10.134.118.96   10.134.152.193  255.255.255.248 UG    0      0        0 bond1
#10.185.207.0    10.187.209.1    255.255.255.248 UG    0      0        0 bond2
 
#generate new permanent routes in correct format for /etc/sysconfig/network-scripts/route-bond1

# $ more route-bond2
#10.185.207.0/29 via 10.187.209.1 dev bond2
#10.187.209.0/29 via * dev bond2
 
import os
 
bond0 = open("route-bond0", "w+")
bond1 = open("route-bond1", "w+")
bond2 = open("route-bond2", "w+")
 
routes = open("routes", "r+")
 
route_list = routes.read().splitlines();
lc=0
list = []
 
for line in route_list:
 
#print line
 lc = lc + 1
 words = line.split()
#print words
 
#Destination Gateway Genmask Iface
 list.append(words)
#print list[0]
 
 
print lc
str = ""
via = "via"
dev = "dev"
sub = " "
 
for i in xrange(0,lc):
  bon = list[i].pop(7)
  print bon
 
  if( bon == "bond0" ):
       str = list[i].pop(0)
       str2 = list[i].pop(0)
       str3 = list[i].pop(0)
       subnet = str3[-3:]
       if( subnet == "248"):
         sub = "29"
       elif( subnet == "224"):
         sub = "27"
       else:
         sub = "0"
       str = str + "/" + sub + " " + "via"  + " " + "".join(str2) + " " +  "dev" + " " + bon 
       bond0.write(str)
       bond0.write("\n")
  elif( bon == "bond2"):
       str = list[i].pop(0)
       str2 = list[i].pop(0)
       str3 = list[i].pop(0)
       subnet = str3[-3:]
       if( subnet == "248"):
         sub = "29"
       elif( subnet == "224"):
         sub = "27"
       else:
         sub = "0"
       str = str + "/" + sub + " " + "via"  + " " + "".join(str2) + " " +  "dev" + " " + bon 
       bond2.write(str)
       bond2.write("\n")
  else:
       str = list[i].pop(0)
       str2 = list[i].pop(0)
       str3 = list[i].pop(0)
       subnet = str3[-3:]
       if( subnet == "248"):
         sub = "29"
       elif( subnet == "224"):
         sub = "27"
       else:
         sub = "0"
       str = str + "/" + sub + " " + "via"  + " " + "".join(str2) + " " +  "dev" + " " +  bon 
       bond1.write(str)
       bond1.write("\n") 
 
bond0.close()
bond1.close()
bond2.close()
