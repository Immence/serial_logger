import configparser
import sys
from os import path

class SettingsFileHandler:

    settings_file_path : str = path.abspath(path.join(sys.argv[0], path.pardir, 'files', 'settings.ini'))

    sections_options_and_types = {
        "GENERAL": {
            "mode": str,
            "program_version_number": str
        },
        "FILES": {
            "default_output_path" : str,
            "gif_resources_path" : str,
            "icon_resources_path" : str
        }
    }

    def __init__(self):
        self._validate_file()
        self.config = configparser.ConfigParser()
        self.config.read(self.settings_file_path)

    def _validate_file(self):
        # Check that the file exists
        if not path.exists(self.settings_file_path):
            raise Exception(f'File "{self.settings_file_path} does not exist')
        # Validate that the file is configured correctly
        config = configparser.ConfigParser()
        config.read(self.settings_file_path)
        for section in self.sections_options_and_types:
            # Validate that the section exists
            if not config.has_section(section):
                raise Exception(f'{self.settings_file_path} missing section [{section}]')
            # Validate that the section has all required options
            for option_item in self.sections_options_and_types.get(section).items():
                option = option_item[0]
                option_type = option_item[1]
                if not config.get(section, option):
                    raise Exception(f'{self.settings_file_path} is missing option "{option}" under section [{section}]')
                try:
                    # Validate that the option is of correct type
                    option_type = self.sections_options_and_types.get(section).get(option)
                    if option_type is str:
                        config.get(section, option)
                    if option_type is bool:
                        config.getboolean(section, option)
                    if option_type is int:
                        config.getint(section, option)
                    if option_type is float:
                        config.getfloat(section, option)
                except ValueError:
                    raise Exception(
                        f'Invalid value in {self.settings_file_path} under section [{section}] for option "{option}". Must be of type {option_type}')

    def update_mode(self, mode : str):
        self.config["GENERAL"]["mode"] = mode
        with open(self.settings_file_path, "w") as config_file:
            self.config.write(config_file)

    def get_version(self) -> str:
        return self.config.get("GENERAL", "program_version_number")
    
    def get_program_mode(self) -> str:
        return self.config.get("GENERAL", "mode")

    def get_gif_resources_path(self) -> str:
        return self.config.get("FILES", "gif_resources_path")

    def get_icon_resources_path(self) -> str:
        return self.config.get("FILES", "icon_resources_path")

    def get_default_output_path(self) -> str:
        return self.config.get("FILES", "default_output_path")