import json
import os
import subprocess

repository = os.environ["GITHUB_REPOSITORY"]
version = os.environ["VERSION"]
result = subprocess.run(["gh", "api", f"repos/{repository}/releases/tags/{version}"], text=True, capture_output=True)
if result.returncode and "HTTP 404" not in result.stderr:
    raise RuntimeError(result.stderr)
released = not result.returncode and not json.loads(result.stdout)["draft"]
with open(os.environ["GITHUB_OUTPUT"], "a") as destination:
    destination.write(f"released={str(released).lower()}\n")
