from .interface import Interface
import inquirer
import yaml
import os
import argparse

class CLInterface(Interface):
    def __init__(self, user_settings_file):
        user_settings = {}

        if os.path.exists(user_settings_file):
            with open(user_settings_file) as f:
                user_settings = yaml.safe_load(f)

        self.questions = []
        self.cache = user_settings
        self.do_not_save = []
        self.handlers = []
        self.user_setting_file = user_settings_file

    def cache_answer(self, key, method):
        if key in self.cache:
            return
        else:
            method()

    def confirm(self, name, message, default: bool, save_answer=False):
        if not save_answer:
            self.do_not_save.append(name)
        self.cache_answer(
            name,
            lambda: self.questions.append(inquirer.Confirm(name, message=message, default=default))
        )
        return self

    def get_input(self, name, message, default, save_answer=False):
        self.do_not_save.append(name)
        self.cache_answer(
            name,
            lambda: self.questions.append(inquirer.Text(name, message=message, default=default))
        )
        return self

    def select(self, name, message, choices, default, save_answer=False):
        if not save_answer:
            self.do_not_save.append(name)
        self.cache_answer(
            name,
            lambda: self.questions.append(inquirer.List(name, message=message, choices=choices, default=default))
        )
        return self

    def checklist(self, name, message, choices, default, save_answer=False):
        if not save_answer:
            self.do_not_save.append(name)
        self.cache_answer(
            name,
            lambda: self.questions.append(inquirer.Checkbox(name, message=message, choices=choices, default=default))
        )
        return self

    def path(self, name, message, default, save_answer=False):
        if not save_answer:
            self.do_not_save.append(name)
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

    def add_value(self, key, value):
        self.cache[key] = value

    def get_value(self, key):
        return self.cache[key]

    def parse_args(self):
            parser = argparse.ArgumentParser(
                            prog = 'launt-siekja',
                            description = 'Scrape websites and export data',
            )
            parser.add_argument("-w", "--website", help="The website to scrape.")
            parser.add_argument("-f", "--format", help="The format to export the data in.")
            parser.add_argument("-o", "--output_directory", help="The output file to export the data to.")
            parser.add_argument("-g", "--google_sheets_id", help="Google Sheet ID you want to export to.")
            parser.add_argument("-r", "--sheet_name", help="Specify range you want to export to.")
            args = parser.parse_args()
            for arg in vars(args):
                value = getattr(args, arg)
                if value is not None:
                    self.add_value(arg, value)
            return self

    def close(self):
        user_settings = {k:v for k, v in self.cache.items() if k not in self.do_not_save}

        with open(self.user_setting_file, "w") as f:
            f.write(yaml.dump(user_settings))
