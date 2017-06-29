import json
from types import SimpleNamespace as Namespace

def json_to_namespace(data):
	return json.loads(data, object_hook=lambda d: Namespace(**d))

def load_describe_file(file):
	if file:
		with open(file) as f:
			data = f.read()
	return data

data = load_describe_file("Gateway.km")
print(dir(json_to_namespace(data)))
