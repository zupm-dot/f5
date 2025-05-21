#!/bin/bash

# run as root

# Define list of F5 hosts
F5_HOSTS=(
  "f5-host-a"
  "f5-host-b"
)

# Prompt for F5 username
read -p "Enter F5 username: " F5_USER

# Prompt for password securely
read -s -p "Enter password for $F5_USER: " F5_PASS
echo

# Command to run on each F5
# REMOTE_COMMAND="tmsh -q -c 'cd /; show running-config recursive' | grep '1.1.1.1\\|2.2.2.21\\|pe-np'"
REMOTE_COMMAND="tmsh -q -c 'cd /; show running-config recursive' | grep 'pe-np'"
# Loop through each host
for F5_HOST in "${F5_HOSTS[@]}"; do
  echo "------ Connecting to $F5_HOST ------"
  sshpass -p "$F5_PASS" ssh -o StrictHostKeyChecking=no "$F5_USER@$F5_HOST" "$REMOTE_COMMAND"
  echo ""
done
