#!/bin/bash
sudo yum update -y
sudo amazon-linux-extras install docker
sudo sed -i 's+--default-ulimit nofile=32768:65536+--default-ulimit nofile=32768:65536 --host=tcp://0.0.0.0:4243+g' /etc/sysconfig/docker
sudo service docker start
sudo usermod -a -G docker ec2-user
docker pull viniciusalves/tweet_extractor