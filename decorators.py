import inquirer

questions = [inquirer.Path("path", message="Specified path")]
answers = inquirer.prompt(questions)
print(answers["path"])
