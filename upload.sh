#!/bin/bash

git pull origin master
git add .
git commit -m "Routine commit for data upload"
spawn git push origin master
expect "Username for 'https://github.com':"         # Wait/expect for the Password string from the spawned process
send "Scott-Bunting\r"      # send the password to spawned process as an input.
expect "Password for 'https://Scott-Bunting@github.com':"
send "Jaguar2018\r"
git status
