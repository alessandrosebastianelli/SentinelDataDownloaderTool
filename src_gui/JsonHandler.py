import json


class JsonHandler:

  def __init__(self):
    self.settings_file_path = "gui_code/settings.json"
    with open(self.settings_file_path, "r") as read_file:
      self.json_data = json.load(read_file)
  
  def get_component_settings(self, component_name):
    settings = self.json_data[component_name]
    return settings[0]
