import subprocess
import inquirer
import utils
import sys

def run_update():
    # Check if git is available
    try:
        subprocess.run(['git', '--version'], check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print('Git is not installed or not in the PATH')
        return

    # Check if there are commits on the upstream repository
    remote_head = subprocess.run(['git', 'rev-parse', '@{u}'],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=utils.get_root_dir()).stdout.decode().strip()

    # Get the head of the local branch
    local_head = subprocess.run(['git', 'rev-parse', 'HEAD'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=utils.get_root_dir()).stdout.decode().strip()

    # Check if the local branch is up to date
    if remote_head == local_head:
        return

    # Ask the user if they want to update
    questions = [
        inquirer.Confirm(
            'update', message="There are updates available. Do you want to update?", default=True)
    ]
    answers = inquirer.prompt(questions)
    if not answers['update']:
        return

    # Update the local repository
    subprocess.run(['git', 'pull', '--ff-only', 'origin',
                   'main'], check=True, cwd=utils.get_root_dir())
    subprocess.run(["python", "-c", "requirements.txt"], cwd=utils.get_root_dir())
    print("You are up to date. You can now run 'siekjen.py' again.")
    # Exit the program
    sys.exit(0)
