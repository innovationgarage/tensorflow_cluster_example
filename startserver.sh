#! /bin/bash

parallel \
  --no-notice --nonall --line-buffer --tag \
  -S $SERVERS \
  "cd tfserver; nohup ./trainingserver.py --hosts $SERVERS < /dev/null > training.log 2>&1 & sleep 2"

nohup tensorboard --logdir=/root/tfserver/logs/ &
