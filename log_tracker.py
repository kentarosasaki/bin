#!/usr/bin/env python

# http://d.hatena.ne.jp/torazuka/20120114/list


import collections
import datetime
import os
import sys
import time


class Summarize(object):
  def __init__(self, access_data_list):
    self.access_data_list = access_data_list

  def summarize(self, bucket_name):
    bucket_size = 0
    head_count = 0
    put_count = 0
    get_count = 0
    delete_count = 0
    for d in self.access_data_list:
      if bucket_name == d.bucket_name:
        if d.method == "[HEAD]":
          head_count += 1
        elif d.method == "[PUT]":
          put_count += 1
          bucket_size += int(d.object_size)
        elif d.method == "[GET]":
          get_count += 1
        elif d.method == "[DELETE]":
          delete_count += 1
          bucket_size -= int(d.object_size)

    total_count = head_count + put_count + get_count + delete_count
    return bucket_name, bucket_size, head_count, put_count, get_count, delete_count, total_count


def define_named_log(access_list):
  fields = [
      "method",
      "bucket_name",
      "object_name",
      "object_size",
      "timestamp",
      "unixtime",
      "response",
  ]
  named_log = collections.namedtuple("access_log", " ".join(fields))
  return [named_log(*a) for a in access_list]


def main():
  log_timestamp = (os.stat(sys.argv[1])).st_mtime
  now = datetime.datetime.now()
  d = now - datetime.timedelta(hours = 1)
  one_hour_ago = time.mktime(d.timetuple())
  if one_hour_ago < log_timestamp:
    with open(sys.argv[1], "r") as f:
      access_list = [line[:-1].split("\t") for line in f]
  else:
    sys.exit(1)

  access_data_list = define_named_log(access_list)
  bucket_sum = Summarize(access_data_list)
  bucket_list = set([data.bucket_name for data in access_data_list])
  result = map(bucket_sum.summarize, bucket_list)

  print("Get Time, Bucket Name, Bucket Size(Byte), HEAD Count, PUT Count, GET Count, DELETE Count, Total Count")
  for res in result:
    print("%s, %s, %d, %d, %d, %d, %d, %d" %
        (now, res[0], res[1], res[2], res[3], res[4], res[5], res[6]))
#    print("Get Time : %s" % now)
#    print("Bucket Name : %s" % res[0])
#    print("Bucket Size : %d(byte)" % res[1])
#    print("HEAD Count  : %d" % res[2])
#    print("PUT Count   : %d" % res[3])
#    print("GET Count   : %d" % res[4])
#    print("DELETE Count: %d" % res[5])
#    print("Total Count : %d" % res[6])
#    print("")


if __name__ == '__main__':
  main()
