# There ain't much to it. This is just a shell script that downloads dependencies from
# pip, nltk module (which is strange but ok), and my private server.

$virt_env = Read-Host 'Would you like to use a virtual environment? (y/n)'
if ($virt_env -eq 'y') {
	Write-Output ''
	Write-Output 'Creating a virtual environment...'
	python -m venv env # create a python virtual environment
	.\env\Scripts\activate # activate the virtual environment
	Write-Output 'Virtual environment has been created'
}

# This section is just downloading module dependencies with pip into the virtual environment.

Write-Output ''
Write-Output 'Installing PIP tools...'
python -m pip install --upgrade pip setuptools wheel # update pip and related components
Write-Output 'PIP tools successfully installed.'

Write-Output ''
Write-Output 'Installing jupyter...'
python -m pip install jupyter 
Write-Output 'Jupyter successfully installed.'

Write-Output ''
Write-Output 'Installing nltk...'
python -m pip install nltk 
python nltk_setup.py
Write-Output 'nltk successfully installed.'

Write-Output ''
Write-Output 'Installing bs4...'
python -m pip install bs4 
Write-Output 'bs4 successfully installed.'

Write-Output ''
Write-Output 'Installing numpy...'
python -m pip install numpy
Write-Output 'numpy successfully installed.'

Write-Output ''
Write-Output 'Installing sklearn...'
python -m pip install sklearn  
Write-Output 'sklearn successfully installed.'

Write-Output ''
Write-Output 'Installing networkx...'
python -m pip install networkx 
Write-Output 'networkx successfully installed.'

Write-Output ''
Write-Output 'Installing lxml...'
python -m pip install lxml 
Write-Output 'lxml successfully installed.'

Write-Output ''
Write-Output 'Downloading GloVe embeddings...'
Invoke-WebRequest -Uri www.screenjunkie.life/textsum/glove.6B.100d.txt -OutFile .\glove.6B.100d.txt # download
Write-Output 'GloVe embeddings successfully downloaded.'

Write-Output ''
if ($virt_env -eq 'y') {
	Write-Output 'Deactivating virtual environment...'
	deactivate # deactivate the virtual environment, since all packages are installed
	Write-Output 'Virtual environment has been deactivated.'
	Write-Output 'Make sure you run activate_venv.ps1 every time prior to using CMD_TextSummarizer.py'
}

Write-Output ''
Write-Output 'Installation is completed!'