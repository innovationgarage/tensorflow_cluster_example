#! /bin/bash

parallel --no-notice --nonall --line-buffer --tag -S $SERVERS "killall -KILL python"
killall -KILL tensorboard
