"""
class to interact with config files .ini (Initialization) format

Config file general format. options and values are all string format
Convert accordingly

[section1]
option1 = value1
option2 = value2

[section2]
option1 = value1
option2 = value2
"""

from configparser import ConfigParser


class ConfigHelper:
    """
    Helper class to work with config files
    """

    @staticmethod
    def get_sections(filepath: str) -> list:
        """Get All Sections for config file"""
        config = ConfigParser()
        config.read(filepath)
        print(config.sections())
        return config.sections()

    @staticmethod
    def get_section_data(filepath: str, section_name: str) -> dict:
        """Get data in a particular section in a dictionary format"""
        config = ConfigParser()
        config.read(filepath)
        data = dict(config.items())
        try:
            return dict(data[section_name])
        except KeyError:
            print("section does not exist")
            return None

    @staticmethod
    def add_section(filepath: str, section_name: str) -> None:
        """Adds a new section and overwrites file"""
        config = ConfigParser()
        config.read(filepath)
        if not config.has_section(section_name):
            config.add_section(section_name)
            print(f"section {section_name} added")
            with open(filepath, "w", encoding="utf-8") as file:
                config.write(file)
                print("file overwritten")
        else:
            print(f"section '{section_name}' already exists")

    @staticmethod
    def delete_section(filepath: str, section_name: str) -> None:
        """Deletes an existing section and overwrites file"""
        config = ConfigParser()
        config.read(filepath)
        if config.has_section(section_name):
            config.remove_section(section_name)
            print(f"section {section_name} deleted")
            with open(filepath, "w", encoding="utf-8") as file:
                config.write(file)
                print("file overwritten")
        else:
            print(f"section '{section_name}' does not exist")

    @staticmethod
    def add_data(filepath: str, section_name: str, option: str, value: str) -> None:
        """
        Adds option (key) to an existing section
        will not add option if it already exists
        use modify data below instead
        """
        config = ConfigParser()
        config.read(filepath)
        if config.has_section(section_name):
            if not config.has_option(section_name, option):
                config.set(section_name, option, value)
                print(f"data added to {section_name}")
                with open(filepath, "w", encoding="utf-8") as file:
                    config.write(file)
                    print("file overwritten")
            else:
                print(f"option '{option}' already exists in section {section_name}")
        else:
            print(f"section '{section_name}' does not exist")

    @staticmethod
    def delete_data(filepath: str, section_name: str, option: str) -> None:
        """
        Deletes option (key) from an existing section
        """
        config = ConfigParser()
        config.read(filepath)
        if config.has_section(section_name):
            if config.has_option(section_name, option):
                config.remove_option(section_name, option)
                print(f"option {option} deleted from section {section_name}")
                with open(filepath, "w", encoding="utf-8") as file:
                    config.write(file)
                    print("file overwritten")
            else:
                print(f"section '{section_name}' does not have option '{option}'")
        else:
            print(f"section '{section_name}' does not exist")

    @staticmethod
    def modify_data(filepath: str, section_name: str, option: str, value: str) -> None:
        """modifies data from an existing section and option"""
        config = ConfigParser()
        config.read(filepath)
        if config.has_section(section_name):
            if config.has_option(section_name, option):
                config.set(section_name, option, value)
                print(f"data modified for section {section_name} and option {option}")
                with open(filepath, "w", encoding="utf-8") as file:
                    config.write(file)
                    print("file overwritten")
            else:
                print(f"option '{option}' does not exist please create first")
        else:
            print(f"section '{section_name}' does not exist")


if __name__ == "__main__":
    pass

    # path = "C:/Users/EdgarTan/Documents/Github/python/config/others/emails/email_credentials.ini"

    # sections = ConfigHelper.get_sections(path)
    # print("sections here")
    # print(sections)

    # section_data = ConfigHelper.get_section_data(path, "otc_report")
    # print("section data here")
    # print(section_data)

    # ConfigHelper.add_section(path, "bnb-params")
    # ConfigHelper.delete_section(path, "bnb-params")

    # ConfigHelper.add_data(path, "bnb-params", "option2", "value1")
    # ConfigHelper.delete_data(path, "bnb-params", "option1")

    # ConfigHelper.modify_data(path, "bnb-params", "option2", "test")
