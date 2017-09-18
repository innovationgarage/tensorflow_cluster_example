#! /usr/bin/env python

import argparse
import sys

import tensorflow as tf
import netifaces
import socket

FLAGS = None

def main(_):
  def addport(host):
    if ':' not in host:
      host = "%s:%s" % (host, FLAGS.default_port)
    return host
  
  hosts = [addport(host) for host in FLAGS.hosts.split(",")]
      
  
  local_ips = set([netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
                   for iface in netifaces.interfaces()
                   if netifaces.AF_INET in netifaces.ifaddresses(iface)])

  task_ips = [host.split(":")[0] for host in hosts]
  task_ips = [socket.gethostbyname(ip) for ip in task_ips]
  local_task_ip = iter(local_ips.intersection(set(task_ips))).next()
  
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
  parser.add_argument(
      "--default_port",
      type=int,
      default=4711,
      help="Default port number"
  )
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
