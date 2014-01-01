#!/usr/bin/env python


import collections
import datetime
import json
import os
import sys
import time


class Aggregate(object):

  def __init__(self, date, access_log_list):
    self.date = date
    self.access_log_list = access_log_list

  def bucket_aggregate(self, bucket_name):
    """ Aggregate each bucket size, count.
    bucket_name: Logged bucket name.
    bucket_size: Total bucket size.
    head_count: Counting of HEAD method.
    put_count: Counting of PUT method.
    get_count: Counting of GET method.
    delete_count: Counting of DELETE method.
    """
    bucket_size = head_count = put_count = get_count = delete_count = 0
    for d in self.access_log_list:
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
    aggr_result = [
        self.date,
        bucket_name,
        bucket_size,
        head_count,
        put_count,
        get_count,
        delete_count,
        head_count + put_count + get_count + delete_count,
    ]
    return aggr_result


def define_named_log(access_list):
  # Deifine namedtuple fields.
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


def list2dict(values):
  keys = [
      "time",
      "bucket",
      "size",
      "head",
      "put",
      "get",
      "delete",
      "total",
  ]
  return [dict(zip(keys, v)) for v in values]


def main():
  # Define log timestamp
  log_timestamp = (os.stat(sys.argv[1])).st_mtime
  now = datetime.datetime.now()
  an_hour_ago = time.mktime((now - datetime.timedelta(hours = 1)).timetuple())

  # Open log when timestamp is within 1 hour.
  if log_timestamp > an_hour_ago:
    with open(sys.argv[1], "r") as f:
      access_list = [ln[:-1].split("\t") for ln in f]
  else:
    sys.exit("No log within 1 hour.")

  # Define named log list.
  access_log_list = define_named_log(access_list)

  # Generate Aggregate Class.
  aggr = Aggregate(now.strftime("%Y%m%d%H%M%S"), access_log_list)

  # Generate list which has set by bucket name.
  bucket_list = set([l.bucket_name for l in access_log_list])
  aggr_res = [aggr.bucket_aggregate(m) for m in bucket_list]

  with open("data.json", "w") as fp:
    json.dump(list2dict(aggr_res), fp, sort_keys=True)


if __name__ == '__main__':
  main()
