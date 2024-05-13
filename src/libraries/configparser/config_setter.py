"""
class to interact with config files .ini (Initialization) format


[staff-otc]  # sections
id = -911624131 # option(key) and values - both must be string
"""

from configparser import ConfigParser


class configSetter:
    """
    Class to work with config files
    """

    def __init__(self, filepath: str):
        """
        initialize with config filepath
        .../config.ini
        """
        self.filepath = filepath

        self.config = ConfigParser()
        self.config.read(filepath)

    def get_sections(self):
        """get config sections"""
        sections = self.config.sections()
        return sections

    def get_section_data(self, section_name: str):
        """get data in a particular section"""
        data = dict(self.config.items())
        section_data = data[section_name]
        return dict(section_data)

    def add_section(self, section_name: str):
        """adds a new section"""
        if not self.config.has_section(section_name):
            self.config.add_section(section_name)
            print(f"section {section_name} added")
        else:
            print(f"section {section_name} already exists")

    def delete_section(self, section_name: str):
        """deletes an existing section"""
        if self.config.has_section(section_name):
            self.config.remove_section(section_name)
            print(f"section {section_name} deleted")
        else:
            print(f"section {section_name} does not exist")

    def add_data(self, section_name: str, option: str, value: str):
        """adds option (key) to an existing section
        will not add option if it already exists
        use modify data below instead
        """
        if self.config.has_section(section_name):
            if not self.config.has_option(section_name, option):
                self.config.set(section_name, option, value)
                print(f"data added to {section_name}")
            else:
                print(f"option {option} already exists in section {section_name}")
        else:
            print(f"section {section_name} does not exist")

    def delete_data(self, section_name: str, option: str):
        """deletes option (key) from an existing section"""
        if self.config.has_section(section_name):
            if self.config.has_option(section_name, option):
                self.config.remove_option(section_name, option)
                print(f"option {option} deleted from section {section_name}")
            else:
                print(f"section {section_name} does not have option {option}")
        else:
            print(f"section {section_name} does not exist")

    def modify_data(self, section_name: str, option: str, value: str):
        """modifies data from an existing section and option"""
        if self.config.has_section(section_name):
            if self.config.has_option(section_name, option):
                self.config.set(section_name, option, value)
                print(f"data modified for section {section_name} and option {option}")
            else:
                print(f"option {option} does not exist please create first")
        else:
            print(f"section {section_name} does not exist")

    def overwrite_file(self):
        """overwrites config file to save changes"""
        # write over file
        with open(self.filepath, "w", encoding="utf-8") as file:
            self.config.write(file)
            print("file overwritten")


if __name__ == "__main__":
    filepath = "C:/Users/Administrator/OneDrive/Github/python/src/libraries/configparser/config.ini"
    cfg = configSetter(filepath)

    sections = cfg.get_sections()
    print(sections)

    section_data = cfg.get_section_data("trading_params")
    print(section_data)

    # cfg.add_section("trading_params")
    # cfg.add_data("trading_params", "quote_ticker", "USDT")

    # cfg.delete_data("trading_params", "quote_ticker")

    # cfg.modify_data("trading_params", "quote_ticker", "USDC")

    # cfg.overwrite_file()
