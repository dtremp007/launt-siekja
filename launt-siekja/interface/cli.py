from .interface import Interface
import inquirer
import yaml
import os

class CLInterface(Interface):
    def __init__(self, user_settings_file):
        user_settings = {}

        if os.path.exists(user_settings_file):
            with open(user_settings_file) as f:
                user_settings = yaml.safe_load(f)

        self.questions = []
        self.cache = user_settings
        self.answers_to_save = []
        self.handlers = []
        self.user_setting_file = user_settings_file

    def cache_answer(self, key, method):
        if key in self.cache:
            return
        else:
            method()

    def confirm(self, name, message, default: bool, save_answer=False):
        if save_answer:
            self.answers_to_save.append(name)
        self.cache_answer(
            name,
            lambda: self.questions.append(inquirer.Confirm(name, message=message, default=default))
        )
        return self

    def get_input(self, name, message, default, save_answer=False):
        self.answers_to_save.append(name)
        self.cache_answer(
            name,
            lambda: self.questions.append(inquirer.Text(name, message=message, default=default))
        )
        return self

    def select(self, name, message, choices, default, save_answer=False):
        if save_answer:
            self.answers_to_save.append(name)
        self.cache_answer(
            name,
            lambda: self.questions.append(inquirer.List(name, message=message, choices=choices, default=default))
        )
        return self

    def checklist(self, name, message, choices, default, save_answer=False):
        if save_answer:
            self.answers_to_save.append(name)
        self.cache_answer(
            name,
            lambda: self.questions.append(inquirer.Checkbox(name, message=message, choices=choices, default=default))
        )
        return self

    def path(self, name, message, default, save_answer=False):
        if save_answer:
            self.answers_to_save.append(name)
        self.cache_answer(
            name,
            lambda: self.questions.append(inquirer.Path(name, message=message, default=default, normalize_to_absolute_path=True))
        )
        return self

    def queue_handler(self, handle_input):
        self.handlers.append(handle_input)
        return self

    def execute(self):
        answers = inquirer.prompt(self.questions, raise_keyboard_interrupt=True)
        self.questions = []
        self.cache.update(answers)
        while len(self.handlers) > 0:
            handle_input = self.handlers.pop()
            handle_input(self.cache)

    def close(self):
        user_settings = {}
        for answer in self.answers_to_save:
            user_settings[answer] = self.cache[answer]

        with open(self.user_setting_file, "w") as f:
            f.write(yaml.dump(user_settings))
