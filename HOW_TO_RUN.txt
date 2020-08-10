Instruction to Run the Project

Initial Setup:

1. Clone the github repository.
2. Run the install.bash script if you're on Linux or the install.ps1 script if you're on Windows.
	* Note that the install script uses wget to download the GloVe embeddings from a private server.
	* If you do not have wget simply download the embeddings by following this link:
		www.screenjunkie.life/textsum/glove.6B.100d.txt
	* Then, drop the embeddings file into the repository directory.

Run with Jupyter Notebook:

1. Open the Jupyter Notebook file and click "Run All" under the "Cell" tab.
2. Once all the cells have ran, put the article links you want summarized along with the number
   of sentences to include in the summary. If entering multiple article links, then make sure all articles
   are about the same topic. 
3. Run the last cell again to test again with different links.

Run as an interactive prompt:

* (Windows) Run .\activate_venv.ps1 to activate the virtual environment if you chose to install it. 
	Don't forget to run deactivate_venv.ps1 once you're done.
* Simply execute "python CMD_TextSummarizer.py" in the terminal to start an interactive prompt.

Run as a non-interactive command:

* (Windows) Run .\activate_venv.ps1 to activate the virtual environment if you chose to install it. 
	Don't forget to run deactivate_venv.ps1 once you're done.
* python CMD_TextSummarizer.py [space_separated_list_of_links] -s [number_of_sentences]
* If no "-s" flag is given along with links, a default of 5 sentence summaries will be used.

NOTE FOR LINUX USERS:
Additional packages may need to be installed from you package manager. Some of the likely suspects are:
	1. python3
	2. python3-pip
	3. python3-lxml 
	
