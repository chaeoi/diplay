import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time


def gh(*args):
    return subprocess.check_output(["gh", *args], text=True).strip()


def number(tag):
    if re.fullmatch(r"[2-9][0-9]{3}\.([1-9]|1[0-2])\.[1-9][0-9]*", tag):
        return tuple(map(int, tag.split(".")))
    return None


def releases():
    pages = json.loads(gh("api", "--paginate", "--slurp", f"repos/{repository}/releases?per_page=100&cachebust={time.time_ns()}"))
    return [release for page in pages for release in page]


def refreshed_releases(version, published=False):
    for attempt in range(6):
        items = releases()
        current = next((item for item in items if item["tag_name"] == version), None)
        if current and (not published or not current["draft"]):
            return items
        if attempt < 5:
            time.sleep(min(2 ** attempt, 8))
    raise RuntimeError(f"release {version} is not yet visible in the GitHub API")


def published_versions(items):
    return [
        number(item["tag_name"])
        for item in items
        if not item["draft"] and not item["prerelease"] and number(item["tag_name"])
    ]


def validate_assets(release, local=False):
    assets = {asset["name"]: asset for asset in release["assets"]}
    if set(assets) != set(files) or len(release["assets"]) != len(files):
        raise RuntimeError("release attachments are incomplete")
    for name, asset in assets.items():
        if asset["state"] != "uploaded" or asset["size"] <= 0:
            raise RuntimeError(f"release attachment is not ready: {name}")
        if local and asset["digest"] != "sha256:" + hashlib.sha256(Path("dist", name).read_bytes()).hexdigest():
            raise RuntimeError(f"release attachment checksum mismatch: {name}")


repository = os.environ["GITHUB_REPOSITORY"]
version = os.environ["VERSION"]
product = os.environ["PRODUCT_NAME"]
files = os.environ.get("RELEASE_ASSETS", "").split()
if subprocess.check_output(["git", "rev-parse", f"refs/tags/{version}^{{commit}}"], text=True).strip() != os.environ["GITHUB_SHA"]:
    raise RuntimeError("release tag belongs to another commit")
all_releases = releases()
existing = next((item for item in all_releases if item["tag_name"] == version), None)
if not existing or existing["draft"]:
    for name in files:
        if not Path("dist", name).is_file():
            raise RuntimeError(f"missing release artifact: {name}")
    notes = subprocess.check_output(["git", "for-each-ref", "--format=%(contents)", f"refs/tags/{version}"], text=True).strip()
    notes += "\n\n## 安装与升级\n\n"
    documentation = f"https://github.com/{repository}/blob/{version}/README.md"
    notes += f"[安装与使用说明]({documentation})。\n"
    images = os.environ.get("RELEASE_IMAGES", "").split()
    if images:
        notes += "\n" + "".join(f"- 镜像：`{image}:{version}`\n" for image in images)
    if files:
        notes += "\n## 下载\n\n| 文件 | 下载 |\n|---|---|\n"
        for name in files:
            notes += f"| {name} | [下载](https://github.com/{repository}/releases/download/{version}/{name}) |\n"
        notes += "\n## SHA-256\n\n下载附件 `SHA256SUMS` 后，可用 `sha256sum --check --ignore-missing SHA256SUMS` 校验。\n\n```text\n"
        notes += Path("dist/SHA256SUMS").read_text() + "```\n"
    previous = max((value for value in published_versions(all_releases) if value < number(version)), default=None)
    if previous:
        previous_tag = ".".join(map(str, previous))
        generated = json.loads(gh("api", "--method", "POST", f"repos/{repository}/releases/generate-notes", "-f", f"tag_name={version}", "-f", f"previous_tag_name={previous_tag}"))
        notes += "\n" + generated["body"] + "\n"
    notes_file = Path(os.environ["RUNNER_TEMP"], "release-notes.md")
    notes_file.write_text(notes)
    if existing:
        gh("release", "edit", version, "--title", f"{product} {version}", "--notes-file", str(notes_file))
    else:
        gh("release", "create", version, "--draft", "--verify-tag", "--title", f"{product} {version}", "--notes-file", str(notes_file))
    # Draft attachments can be replaced; published attachments are never uploaded again.
    if files:
        gh("release", "upload", version, *(f"dist/{name}" for name in files), "--clobber")
    existing = next(item for item in refreshed_releases(version) if item["tag_name"] == version)
    validate_assets(existing, local=True)
    gh("release", "edit", version, "--draft=false", "--latest=false")
else:
    validate_assets(existing)

# Failed-job reruns reuse earlier job outputs, so decide latest here from published releases.
all_releases = refreshed_releases(version, published=True)
promote = number(version) == max(published_versions(all_releases))
if promote:
    latest = subprocess.run(["gh", "api", f"repos/{repository}/releases/latest"], text=True, capture_output=True)
    if latest.returncode and "HTTP 404" not in latest.stderr:
        raise RuntimeError(latest.stderr)
    if latest.returncode or json.loads(latest.stdout)["tag_name"] != version:
        gh("release", "edit", version, "--latest")
with open(os.environ["GITHUB_OUTPUT"], "a") as destination:
    destination.write(f"latest={str(promote).lower()}\n")
print(f"Published {version}; latest={str(promote).lower()}")
