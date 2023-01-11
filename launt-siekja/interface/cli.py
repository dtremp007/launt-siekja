from .interface import Interface
import inquirer

class CLInterface(Interface):
    def __init__(self):
        self.questions = []
        self.old_answers = {}

    def set_old_answers(self, answers):
        self.old_answers = answers

    def confirm(self, name, message, default: bool):
        self.questions.append(inquirer.Confirm(name, message=message, default=default))
        return self

    def get_input(self, name, message, default):
        if not name in self.old_answers:
            self.questions.append(inquirer.Text(name, message=message, default=default))
        return self

    def select(self, name, message, choices, default):
        if not name in self.old_answers:
            self.questions.append(inquirer.List(name, message=message, choices=choices, default=default))
        return self

    def checklist(self, name, message, choices, default):
        if not name in self.old_answers:
            self.questions.append(inquirer.Checkbox(name, message=message, choices=choices, default=default))
        return self

    def execute(self, handle_input):
        answers = inquirer.prompt(self.questions)
        self.questions = []
        self.old_answers = {}
        handle_input(answers)
