#! /bin/bash

if [ "$1" == "" ]; then
    echo "Usage: setup.sh SERVER_1_IP,SERVER_2_IP,..SERVER_N_IP"
    exit
fi
export SERVER_IPS="$1"
export SERVERS="root@$(echo $SERVER_IPS | sed -e "s+,+,root@+g")"

(IFS=, ; for SERVER in $SERVERS; do ssh -oStrictHostKeyChecking=no $SERVER 'echo done'; done; ) 

parallel --no-notice --nonall --line-buffer -S $SERVERS 'apt install -y language-pack-en'
parallel --no-notice --nonall --line-buffer -S $SERVERS 'apt install -y language-pack-nb'
parallel --no-notice --nonall --line-buffer -S $SERVERS 'apt install -y python-pip python-virtualenv'
parallel --no-notice --nonall --line-buffer -S $SERVERS 'pip install tensorflow'

(
    IFS=,
    for SERVER in $SERVERS; do
        scp trainingserver.py $SERVER:
    done
) 


export SERVER_PORTS="$(echo $SERVER_IPS | sed -e "s+,+:4711,+g"):4711"
parallel --no-notice --nonall --line-buffer -S $SERVERS "nohup ./trainingserver.py --hosts $SERVER_PORTS & sleep 2"
