#!/usr/bin/python

import sys
import boto3
import subprocess

# TODO: Update s3 function
#initiate connection to bucket, using service name and date as parameters
def init_conn(service,date):

   filename = date + "-" + service + "-access.log.gz"
   resource = boto3.resource('s3')
   my_bucket = resource.Bucket('url')
   print(filename)
   my_bucket.download_file(filename, filename)

   return filename


def max_avg_response(c_log):
   cnt_res = 0
   max_res = 0
   for line in c_log:
      #split line into array by spaces for parsing 
      split_str = line.split()
      if(split_str[17] == '.'):
         split_str[17] = 0
      else:
         split_str[17] = float(split_str[17])
   #cases where response time may be .
      if( split_str[17] == '.'):
         cnt_res += 0
      else:
         cnt_res += float(split_str[17])
      if( float(split_str[17]) > max_res and split_str[17] != '.'): 
          max_res = float(split_str[17])
      
   print("Max response: ", float(max_res))
   print("Avg response: ", float(cnt_res)/len(c_log))   
def max_avg_upstream(c_log):

   cnt_upstr = 0
   max_upstr = 0
   for line in c_log:
      #split line into array by spaces for parsing
      split_str = line.split()
      size = len(split_str) - 1 
      if(split_str[size] == '.'):
         split_str[size] = 0
      else:
         split_str[size] = float(split_str[size])
   #cases where response time may be .
      if( split_str[size] == '.'):
         cnt_upstr += 0
      else:
         cnt_upstr += float(split_str[size])
      if( split_str[size] > max_upstr and split_str[size] != '.'):
          max_upstr = float(split_str[size])

   print("Max Upstream response: ", max_upstr)
   print("Avg Upstream response: ", float(cnt_upstr)/len(c_log))

#neeeds improvement, replace with regex
def http_code_count(c_log):
   endpoint = ""
   http_code = ""
   count = ""
   cnt_dic = {}
   for line in c_log:
      split_str = line.split()
      endpoint = split_str[0]
      http_code = split_str[8]
      #print(endpoint, http_code)
      key = (endpoint, http_code)
      if key in cnt_dic:
        cnt_dic[key] += 1
      else:
        cnt_dic[key] = 1
   print("---Endpoint, HTTP code, count---")
   for k, v in cnt_dic.items():
        print(k,v)
def proc_log(filename):
  c_log = []
  #filter out healthchecks the unix way, needs improvement
  cmd = "zcat " + filename + " | grep -v 'Ruby\|400'"
  zcat_out = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE, stderr= subprocess.STDOUT)
  for line in zcat_out.stdout.readlines():
      c_log.append(line) 

  return c_log 

if __name__ == '__main__':

  if (len(sys.argv) > 3 or len(sys.argv) < 3):
    print("usage")
    print("./grab_aws_log logname date")
    print("./grab_aws_log score 2016-04-24")
  else:
    f_name = init_conn(sys.argv[1], sys.argv[2])
    ret = proc_log(f_name)
    max_avg_response(ret)
    max_avg_upstream(ret)
    http_code_count(ret)


'''
:~/.aws$ python grab_aws_log score 2016-04-24
2016-04-24-score-access.log.gz
('Max response: ', 1.616)
('Avg response: ', 0.1576842105263158)
('Max Upstream response: ', 1.611)
('Avg Upstream response: ', 0.14757894736842106)
---Endpoint, HTTP code, count---
(('172.31.31.3', '200'), 19)
'''
