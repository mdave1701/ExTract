# There ain't much to it. This is just a shell script that downloads dependencies from
# pip, nltk module (which is strange but ok), and my private server.

python -m pip install --upgrade pip setuptools wheel # update pip and related components
python -m pip install jupyter 
python -m pip install nltk # discovered dependency
python -m pip install bs4 # ?? can't remember 
python -m pip install numpy
python -m pip install sklearn # I think discovered dependency? Or maybe it was already there, who knows. 
python -m pip install networkx # discovered dependency
python -m pip install lxml # discovered dependency. this one also requires linux users to isntall the python-lxml package.
python nltk_setup.py # nltk was insistent on having me download some files lol. this runs the py script to do that. 
# Bottom line, anything that I added here was based solely on error messages that python gave me while
# I tried to run the jupyter notebook. Only this exact setup was sufficient for the code to run on my
# system without complaining. 

Invoke-WebRequest -Uri www.screenjunkie.life/textsum/glove.6B.100d.txt -OutFile .\glove.6B.100d.txt # for windows
