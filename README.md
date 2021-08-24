# Send-CLOC-Report
## Objective
Scan a specified GitHub source repository with CLOC and send the output to a specified email address.

## Implementation
The Send CLOC (count lines of code) Report script works by first prompting the user for a sender email address and password. These account credentials will be used to login into the Gmail email service and send the CLOC report to a specified email address. 
The user is then prompted for a receiver email address for where to the send the CLOC report, the url of a Github repository, and a specified branch within the repository to scan.
The repository is processed with CLOC and the output is placed into a CSV file. This CSV file is sent as an attachment from the sender email address to the specified receiver email address.

## Requirements
 - Python 3.7.4 or later
  - An interpreted high-level general-purpose programming language
  - Python 3 installation and documentation: https://www.python.org/downloads/
  - Python executable must be on system PATH
 - pip 20.0.1 or later
  - Package management system used to install and manage software packages/libraries written in Python.
  - Pip installation and documentation: https://pip.pypa.io/en/stable/installation/
 - GitPython 3.1.10 or later 
  - A python library used to interact with Git repositories
  - GitPython installation and documentation: https://gitpython.readthedocs.io/en/stable/


