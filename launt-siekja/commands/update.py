import subprocess
import inquirer
import utils

def run_update():
  # Check if git is available
  try:
    subprocess.run(['git', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  except subprocess.CalledProcessError:
    print('Git is not installed or not in the PATH')
    return

  # Check if there are commits on the upstream repository
  result = subprocess.run(['git', 'rev-list', '--count', '@{u}..'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=utils.get_root_dir())
  num_commits = int(result.stdout)
  if num_commits == 0:
    return

  # Ask the user if they want to update
  questions = [
    inquirer.Confirm('update', message='There are {} commits on the upstream repository. Do you want to update?'.format(num_commits))
  ]
  answers = inquirer.prompt(questions)
  if not answers['update']:
    return

  # Update the local repository
  subprocess.run(['git', 'pull', '--ff-only', 'upstream', 'main'], check=True, cwd=utils.get_root_dir())
  print("You are up to date. You can now run 'siekjen' again.")
