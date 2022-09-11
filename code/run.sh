#!/bin/bash


cd ${0%/run.sh} # go to code directory

if ! [ -d "database" ]
then
    echo "creating database directory"
    mkdir database
fi

if ! [ -d "datadump" ]
then
    echo "creating datadump"
    mkdir datadump
fi

python3 scraper.py