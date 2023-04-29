#!/bin/bash

echo "Update RHEL Packages"
sudo yum update -y

echo "Install and enable Docker"
sudo amazon-linux-extras install -y docker
sudo systemctl start docker
sudo systemctl enable docker

echo "Add dcoker group to ec2-user"
sudo usermod -a -G docker ec2-user
sudo su ec2-user

echo "Install docker-compose"
sudo mkdir -p /usr/local/lib/docker/cli-plugins
VER=2.4.1                                                                                                                                                    sudo curl -L https://github.com/docker/compose/releases/download/v${VER}/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
sudo ln -s /usr/local/lib/docker/cli-plugins/docker-compose /usr/bin/docker-compose
docker-compose --version
