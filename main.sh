#!/bin/sh
echo "Welcome to the MDF action"
env
echo "pwd"
pwd
ls -lht

python /main.py "$@"
