import os
import yaml

def find_config():
	if 'HACKBOT_CONFIG' in os.environ:
		return os.environ['HACKBOT_CONFIG']
	else:
		return os.path.join(os.getcwd(), 'config.yaml')

config = {}

def reload():
	config.update(yaml.load(open(find_config())))
reload()
