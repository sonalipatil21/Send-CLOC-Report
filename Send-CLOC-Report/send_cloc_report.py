import os, sys, re, git, ssl, smtplib, getpass, subprocess, platform, git
from datetime import datetime
from email import encoders
from pip._internal import main
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Import package or install first if required
'''
def import_installation_check(package, import_statement):
    # Import package
    try:
        print(f"Importing the following: '{import_statement}'")
        __import__(import_statement)

    # Install package and import
    except:
        print(f"Unable to import {package}. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Importing the following: '{import_statement}'")
        __import__(import_statement)
'''


# Validate user inputted email
def validate_email():
    # Regular expression for checking syntax of email address
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
    while True:
        try:
            email_input = input("Enter email: \n")
            # Check regex against email address
            if (re.fullmatch(email_regex, email_input)):
                return email_input
                break
            else:
                print(f"{email_input} is not a valid email address.")
        except:
            continue


# Validate user inputted repository url
def validate_repository_url():
    # Regular expression for checking syntax of repository url
    url_regex = r'((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)(/)?'
    while True:
        try:
            repository_url_input = input("Enter url: \n")
            # Check regex against repository url
            if (re.fullmatch(url_regex, repository_url_input)):
                return repository_url_input
                break
            else:
                print(f"{repository_url_input} is not a valid repository url.")
        except:
            continue


# Validate user inputted repository branch
def validate_repository_branch():
    # Regular expression for checking syntax of repository branch
    branch_regex = r'^[A-Za-z][A-Za-z0-9_-]*[A-Za-z0-9]$'
    while True:
        try:
            repository_branch_input = input("Enter branch: \n")
            # Check regex against repository branch
            if (re.fullmatch(branch_regex, repository_branch_input)):
                return repository_branch_input
                break
            else:
                print(f"{repository_branch_input} is not a valid repository branch.")
        except:
            continue


# Get current time, repository name, and output file name
def get_file_information(url, branch):
    # Get current time when CSV was created 
    current_time = datetime.now().strftime("%m-%d-%Y")

    # Get repository name
    repository_name = url.split('.git')[0].split('/')[-1]

    # Create CSV name
    output_file = repository_name + "-" + branch + "_" + current_time + '.csv' # + " (" + current_time + ")" + ''
    return current_time, repository_name, output_file


# Create CLOC report to send 
def create_cloc_report(repo_url, repo_branch, executable_name_entry):
    # Get repository name and output file name
    time_created, repo_name, output_file_name = get_file_information(repo_url, repo_branch)

    # Current working directory to repository name
    local_repo_path = os.path.join(os.getcwd(), repo_name)

    # Current working directory to cloc executable
    cloc_executable_path = os.path.join(os.getcwd(), executable_name_entry)

    if not os.path.exists(local_repo_path):
        # Clone repository
        git.Git(os.getcwd()).clone(repo_url)
    print(output_file_name)
    # Instance pointing to git-python repository
    repository_instance = git.Repo(local_repo_path)

    # Pull from repository
    repository_pull = git.cmd.Git(local_repo_path)
    repository_pull.pull()

    # Checkout repository branch
    repository_instance.git.checkout('-f', repo_branch)
    #output_file_name = 'hello.csv'
    print("Creating CSV file...")
    csv_output = subprocess.Popen([cloc_executable_path, local_repo_path, '--csv', '--out', output_file_name , '--quiet'], stdout=subprocess.PIPE)
    csv_output.stdout.read()

    return time_created, repo_name, output_file_name


# Send CLOC report to receiver email
def email_cloc_results(username_entry, password_entry, email_from_entry, email_to_entry, repo_url, repo_branch, repo_name_entry, output_file_name, time_entry):
    # Set email content
    email_subject_line = f"CLOC Report Created for {repo_name_entry} - {repo_branch} on {time_entry}"
    email_body = f"CLOC results are located in attachment below: {output_file_name}"

    # Set email headers
    email_message = MIMEMultipart()
    email_message['From'] = email_from_entry
    email_message['To'] = email_to_entry
    email_message['Subject'] = email_subject_line
    email_message['Bcc'] = email_to_entry

    # Add body to email
    email_message.attach(MIMEText(email_body, 'plain'))

    cloc_attachment = MIMEBase('application', 'octet-stream')
    cloc_attachment.set_payload(open(output_file_name, 'rb').read())
    encoders.encode_base64(cloc_attachment)

    cloc_attachment.add_header('Content-Disposition', "attachment", filename= output_file_name)
    email_message.attach(cloc_attachment)

    #context = ssl.create_default_context()
    #with smtplib.SMTP('smtp.gmail.com', 587) as server:
    #    server.ehlo()
    #    server.starttls(context=context)
    #    server.login(user_name, password)
    #    server.sendmail(email_from, email_to, email_message.as_string())

    # Log in to server using secure context and send email
    
    print(f"Emailing CLOC report to {email_to_entry}...")
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(username_entry,password_entry)
    server.sendmail(email_from_entry, email_to_entry, email_message.as_string())
    server.quit()
    context = ssl.create_default_context()
   
    print(f"CLOC report successfully sent to {email_to_entry}.")


def main():
    # Default/Test values

    '''
    username = 'testmail@gmail.com'
    email_from = username
    password = 'test1234!'

    email_to = 'testmail@gmail.com'

    repository_url = 'https://github.com/AlDanial/cloc.git'
    repository_branch = 'master'
    '''
    # CLOC executable
    executable_name = "cloc-1.90.exe"
    
     # Sender email information
    print("\n---Enter sender email---")
    email_from = validate_email()
    username = email_from
    password = getpass.getpass(prompt='Enter email password: ', stream=None)

    ## Receiver email information
    print("\n---Enter receiver email---")
    email_to = validate_email()

    ## Github repository information
    print("\n---Enter url of repository---")
    repository_url = validate_repository_url()

    print("\n ---Enter branch name within repository---")
    repository_branch = validate_repository_branch()

    ## Git imported above
    #import_installation_check("gitpython", "git")


    # Create CLOC report from repository
    print("Creating CLOC report...")
    creation_time, repository_name, output_file = create_cloc_report(repository_url, repository_branch, executable_name)

    # Email cloc results to specific user
    email_cloc_results(username, password, email_from, email_to, repository_url, repository_branch, repository_name, output_file, creation_time)


if __name__ == "__main__":
    main()