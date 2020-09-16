import os
import json

print("::debug:: GETTING VARIABLES")
workspace_name = os.environ.get("INPUT_WORKSPACE_NAME", default=None)
resource_group = os.environ.get("INPUT_RESOURCE_GROUP", default=None)


workspace_dict = {
    'name'           : workspace_name,
    'resource_group' : resource_group
}

f = json.dumps(workspace_dict)
print(f"::set-output name=workspace::{f}")