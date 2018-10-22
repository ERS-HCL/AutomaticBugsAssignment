## Automatic Bug Assignment System
The aim is to develop a system to predict assignment of bug/issue to developer.

## Prerequisites
* Python 3.4 or later
* Download lemmatizer corpus. This can be done by opening python command prompt and typing as below:  
   \>\>\> import nltk  
   \>\>\> nltk.download('wordnet')

## Features
The system can run in three modes: 
* Simulation mode : This can be used as a validation mode to test the accuracy of the system.
>      $ AutomaticBugAssignment.py -f <PATH_TO_CONFIG_FILE> -t simulate
* Training mode : This can be used to train system so that there is correspondence of developer with bugs they fixed.
>      $ AutomaticBugAssignment.py -f <PATH_TO_CONFIG_FILE> -t train
* Query mode : This can be used to assign new bug reports to developers.
>      $ AutomaticBugAssignment.py -f <PATH_TO_CONFIG_FILE> -t query  
  
Sample configuration file (ABAInput.xml) and data file (Data.xlsx & Data_query.xlsx) are provided in data folder of the repository.
  
[For detailed help of the topic please download 'Automatic assignment of issues or bugs.pptx' presentation in the docs folder of repository. ](https://github.com/ERS-HCL/AutomaticBugsAssignment/blob/master/docs/Automatic%20assignment%20of%20issues%20or%20bugs.pptx)

## License
This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments
Special thanks to Ritesh Sinha and ACE team (HCL Technologies Limited).
