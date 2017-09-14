#! /usr/bin/env python

import argparse
import sys

import tensorflow as tf

FLAGS = None

def main(_):
  hosts = FLAGS.hosts.split(",")

  import os
  with os.popen('ifconfig eth0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1') as f:
      local_ip=f.read().strip()

  task_index = [host.split(":")[0] for host in hosts].index(local_ip)

  ps_hosts = hosts[:FLAGS.ps_servers]
  worker_hosts = hosts[FLAGS.ps_servers:]

  job_name = "ps"
  if task_index >= FLAGS.ps_servers:
      job_name = "worker"
      task_index -= FLAGS.ps_servers
      
  cluster = tf.train.ClusterSpec({"ps": ps_hosts, "worker": worker_hosts})

  server = tf.train.Server(cluster,
                           job_name=job_name,
                           task_index=task_index)

  server.join()

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.register("type", "bool", lambda v: v.lower() == "true")
  # Flags for defining the tf.train.ClusterSpec
  parser.add_argument(
      "--hosts",
      type=str,
      default="",
      help="Comma-separated list of hostname:port pairs"
  )
  parser.add_argument(
      "--ps_servers",
      type=int,
      default=1,
      help="Number of parameter servers"
  )
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
