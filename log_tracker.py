#!/usr/bin/env python
# coding=utf-8


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
    """ Aggregate each bucket size and method count.

    time: Aggregated time.
    bucket: Logged bucket name.
    size: Total bucket size.
    head: Counting of HEAD method.
    put: Counting of PUT method.
    get: Counting of GET method.
    delete: Counting of DELETE method.
    total: Counting of all method.
    """
    aggr = {
        "time":self.date,
        "bucket":bucket_name,
        "size":0,
        "head":0,
        "put":0,
        "get":0,
        "delete":0,
        "total":0,
    }
    for d in self.access_log_list:
      if aggr["bucket"] == d.bucket_name:
        if d.method == "[HEAD]":
          aggr["head"] += 1
          aggr["total"] += 1
        elif d.method == "[PUT]":
          aggr["put"] += 1
          aggr["total"] += 1
          aggr["size"] += int(d.object_size)
        elif d.method == "[GET]":
          aggr["get"] += 1
          aggr["total"] += 1
        elif d.method == "[DELETE]":
          aggr["delete"] += 1
          aggr["total"] += 1
          aggr["size"] -= int(d.object_size)
    return aggr


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


def gen_json(aggr_res, modified_now):
  json_with_time = "".join(("data.json.",str(modified_now)))
  sym_json = "data.json"
  with open(json_with_time, "w") as output_log:
    json.dump(aggr_res, output_log, sort_keys=True)
  if os.path.islink(sym_json):
    os.unlink(sym_json)
    os.symlink(json_with_time, sym_json)
  else:
    os.symlink(json_with_time, sym_json)


def main():
  # Define log timestamp
  log_timestamp = (os.stat(sys.argv[1])).st_mtime
  now = datetime.datetime.now()
  modified_now = now.strftime("%Y%m%d%H%M%S")
  subtracted_time = time.mktime(
      (now - datetime.timedelta(hours = 1)).timetuple())

  # Open log when timestamp is within time subtraction.
  if log_timestamp > subtracted_time:
    with open(sys.argv[1], "r") as input_log:
      access_list = [f[:-1].split("\t") for f in input_log]
  else:
    sys.exit("No log within 1 hour.")

  # Define named log tuple.
  access_log_list = define_named_log(access_list)

  # Generate Aggregate Class.
  aggregate = Aggregate(modified_now, access_log_list)

  # Generate list which has set by bucket name.
  bucket_list = set([l.bucket_name for l in access_log_list])
  aggr_res = [aggregate.bucket_aggregate(m) for m in bucket_list]

  # Generage json output.
  gen_json(aggr_res, modified_now)


if __name__ == '__main__':
  main()
