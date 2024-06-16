from promptflow.client import load_flow

flow_path = "."
directory = "638530437990000000"

f = load_flow(source=flow_path)
result = f(directory=directory)

print(result)