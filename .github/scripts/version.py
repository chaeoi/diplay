import datetime
import json
import os
import re
import subprocess


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def parse_version(value):
    match = re.fullmatch(r"([2-9][0-9]{3})\.([1-9]|1[0-2])\.([1-9][0-9]*)", value)
    return tuple(map(int, match.groups())) if match else None


def release(path):
    result = subprocess.run(["gh", "api", f"repos/{os.environ['GITHUB_REPOSITORY']}/releases/{path}"], text=True, capture_output=True)
    if result.returncode:
        if "HTTP 404" in result.stderr:
            return None
        raise RuntimeError(result.stderr)
    return json.loads(result.stdout)


def output(version="", released=False, skip=False):
    values = {"version": version, "released": str(released).lower(), "skip": str(skip).lower()}
    with open(os.environ["GITHUB_OUTPUT"], "a") as destination:
        destination.write("".join(f"{name}={value}\n" for name, value in values.items()))


head = os.environ["GITHUB_SHA"]
date = datetime.datetime.fromisoformat(git("show", "-s", "--format=%cI", head)).astimezone(datetime.timezone.utc)
prefix = (date.year, date.month)
tags = []
for line in git("for-each-ref", "--format=%(refname:strip=2) %(objectname) %(*objectname)", "refs/tags").splitlines():
    name, target, *peeled = line.split()
    number = parse_version(name)
    if number:
        tags.append((number, peeled[0] if peeled else target))
assigned = [number for number, target in tags if target == head]
if assigned:
    number = max(assigned)
else:
    # An older queued commit must not acquire a higher version than its successor.
    for target in {target for _, target in tags}:
        result = subprocess.run(["git", "merge-base", "--is-ancestor", head, target])
        if result.returncode == 0:
            output(skip=True)
            print("Skipping an unversioned commit superseded by a newer versioned commit.")
            raise SystemExit(0)
        if result.returncode != 1:
            raise RuntimeError("cannot compare release commit ancestry")
    sequence = max((number[2] for number, _ in tags if number[:2] == prefix), default=0) + 1
    number = (*prefix, sequence)
if not 0 < number[2] <= 4294967295:
    raise RuntimeError("release sequence is out of range")
version = ".".join(map(str, number))
if not assigned:
    subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
    subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], check=True)
    subject = git("show", "-s", "--format=%s", head)
    subprocess.run(["git", "tag", "-a", "--cleanup=verbatim", version, head, "-m", f"## 更新内容\n\n- {subject}\n"], check=True)
    subprocess.run(["git", "push", "origin", f"refs/tags/{version}"], check=True)
existing = release(f"tags/{version}")
output(version, released=bool(existing and not existing["draft"]))
print(f"Release version: {version}")
