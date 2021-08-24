# Send-CLOC-Report
## Objective
Scan a specified GitHub source repository with CLOC and send the output to a specified email address.

## Implementation
The Send CLOC (count lines of code) Report script works by first prompting the user for a sender email address and password. These account credentials will be used to login into the Gmail email service and send the CLOC report to a specified email address. 
The user is then prompted for a receiver email address for where to the send the CLOC report, the url of a Github repository, and a specified branch within the repository to scan.
The repository is processed with CLOC and the output is placed into a CSV file 

## Requirements
 - Python 3.7.4 or later
 - pip 20.0.1 or later
 - pip install gitpython 
