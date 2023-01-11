class Interface:
    def confirm(self, name, message, default):
        raise NotImplementedError

    def get_input(self, name, message, default):
        raise NotImplementedError

    def select(self, name, message, choices, default):
        raise NotImplementedError

    def checklist(self, name, message, choices, default):
        raise NotImplementedError

    def execute(self, handle_input):
        raise NotImplementedError
