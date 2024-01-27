from tools import ini_to_dict


class Config:

    def __init__(self, config_file, database_path):
        self.config_data = ini_to_dict(config_file)
        self.database_path = database_path

    @property
    def echo_mode(self):
        return True if self.config_data['DATABASE']['echo'] == 'True' else False

    @property
    def debug_mode(self):
        return True if self.config_data['APPLICATION']['debug_mode'] == 'True' else False

    @property
    def db_uri(self):
        return '{}:///{}'.format(
            self.config_data['DATABASE']['dialect'],
            self.database_path
        )
