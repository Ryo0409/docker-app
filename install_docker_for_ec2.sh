#!/bin/bash

echo "Update RHEL Packages"
sudo yum update -y

echo "Install and enable Docker"
sudo amazon-linux-extras install -y docker
sudo systemctl start docker
sudo systemctl enable docker

echo "Add dcoker group to ec2-user"
sudo usermod -a -G docker ec2-user
