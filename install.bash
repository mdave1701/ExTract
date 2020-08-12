#!/bin/bash
# There ain't much to it. This is just a shell script that downloads dependencies from
# pip, nltk module (which is strange but ok), and my private server.

python3 -m pip install --upgrade pip setuptools wheel # update pip and related components
python3 -m pip install jupyter 
python3 -m pip install nltk # discovered dependency
python3 -m pip install bs4 # ?? can't remember 
python3 -m pip install numpy
python3 -m pip install sklearn # I think discovered dependency? Or maybe it was already there, who knows. 
python3 -m pip install networkx # discovered dependency
python3 -m pip install lxml # discovered dependency. this one also requires linux users to isntall the python-lxml package.
python3 nltk_setup.py # nltk was insistent on having me download some files lol. this runs the py script to do that. 
python3 -m pip install pyttsx3
# Bottom line, anything that I added here was based solely on error messages that python gave me while
# I tried to run the jupyter notebook. Only this exact setup was sufficient for the code to run on my
# system without complaining. 

wget www.screenjunkie.life/textsum/glove.6B.100d.txt 

# Requires sudo priveleges and I'm also too lazy to figure out how to work around different package managers.
# This will have to do for now lol. 
echo; echo; echo 
echo IMPORTANT MESSAGE FOR LINUX USERS; echo
echo You may have to install the python-lxml package from your distro\'s repository.
echo Its name may differ, but for Arch Linux based distros it\'s python-lxml.
echo I dunno, google it xD; echo
