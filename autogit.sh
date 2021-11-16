#!/bin/bash

path=$(cd `dirname $0`; pwd)
cd $path
git add .
remark=$(date +"%Y-%m-%d %H:%M:%S")
git commit -m "Update: ${remark}"
git pull origin master
git push origin master
