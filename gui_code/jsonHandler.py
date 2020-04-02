import json


with open("gui_code/settings.json", "r") as read_file:
  data = json.load(read_file)


def get_component_settings(component_name):
  settings = data[component_name]
  return settings[0]

print(get_component_settings('downloader')['number_of_scene'])
