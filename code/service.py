import os
print("::debug:: get Model Name")
var = os.environ.get("INPUT_MODEL_NAME", default=None)
print("Modelname: " + var)