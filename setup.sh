#!/bin/bash
sudo yum upgrade -y
cd /home/ec2-user || exit
sudo amazon-linux-extras enable python3.8
sudo amazon-linux-extras install epel -y
yum clean metadata
sudo yum install htop -y
sudo yum install python3.8 -y
sudo yum install git -y
git clone https://github.com/sinanartun/awsbc4_kin.git
sudo chown -R ec2-user:ec2-user /home/ec2-user/awsbc4_kin
sudo chmod 2775 /home/ec2-user/awsbc4_kin && find /home/ec2-user/awsbc4_kin -type d -exec sudo chmod 2775 {} \;
cd awsbc4_kin || exit
pip3.8 install -r requirements.txt
python3.8 main.py