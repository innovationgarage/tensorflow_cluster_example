#! /usr/bin/env python

import argparse
import sys

import tensorflow as tf
import netifaces

FLAGS = None

def main(_):
  hosts = FLAGS.hosts.split(",")

  local_ips = set([netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
                   for iface in netifaces.interfaces()
                   if netifaces.AF_INET in netifaces.ifaddresses(iface)])

  task_ips = [host.split(":")[0] for host in hosts]
  local_task_ip = local_ips.intersection(set(task_ips))[0]
  
  task_index = task_ips.index(local_task_ip)

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
