from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

REPOSITORY_URL = "https://extensions.blender.org/api/v1/extensions/"
HEADERS = {"User-Agent": "dcc-mcp-blender-extensions/0.1"}
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_]*$")


def _request(url: str, timeout: int = 30):
    return urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=timeout)


def repository(blender_version: Optional[str] = None) -> Dict[str, Any]:
    params = {"blender_version": blender_version} if blender_version else {}
    url = REPOSITORY_URL
    if params:
        url += "?" + urllib.parse.urlencode(params)
    with _request(url) as response:
        return json.loads(response.read().decode("utf-8"))


def _validate_id(extension_id: str) -> str:
    extension_id = extension_id.strip().lower()
    if not ID_PATTERN.fullmatch(extension_id):
        raise ValueError(f"Invalid Blender extension ID: {extension_id!r}")
    return extension_id


def _deduplicate(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    result = []
    for item in items:
        extension_id = item.get("id")
        if extension_id in seen:
            continue
        seen.add(extension_id)
        result.append(item)
    return result


def search_extensions(
    query: str,
    blender_version: Optional[str] = None,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    query = query.strip().lower()
    if not query:
        raise ValueError("query must not be empty")
    matches = []
    for item in _deduplicate(repository(blender_version).get("data", [])):
        searchable = " ".join(
            [
                str(item.get("id", "")),
                str(item.get("name", "")),
                str(item.get("tagline", "")),
                str(item.get("maintainer", "")),
                " ".join(item.get("tags") or []),
            ]
        ).lower()
        if query not in searchable:
            continue
        matches.append(
            {
                "id": item.get("id"),
                "name": item.get("name"),
                "version": item.get("version"),
                "tagline": item.get("tagline"),
                "maintainer": item.get("maintainer"),
                "license": item.get("license", []),
                "tags": item.get("tags", []),
                "blender_version_min": item.get("blender_version_min"),
                "blender_version_max": item.get("blender_version_max"),
                "source_url": item.get("website"),
            }
        )
        if len(matches) >= max(1, min(limit, 50)):
            break
    return matches


def inspect_extension(
    extension_id: str,
    version: Optional[str] = None,
    blender_version: Optional[str] = None,
) -> Dict[str, Any]:
    extension_id = _validate_id(extension_id)
    matches = [
        item
        for item in repository(blender_version).get("data", [])
        if item.get("id") == extension_id and (not version or item.get("version") == version)
    ]
    if not matches:
        constraint = f" version {version}" if version else ""
        raise ValueError(f"Blender extension not found: {extension_id}{constraint}")
    item = dict(matches[0])
    item["repository_url"] = REPOSITORY_URL
    return item


def package_descriptor(item: Dict[str, Any], path: Path, sha256: str) -> Dict[str, Any]:
    expected = str(item.get("archive_hash") or "")
    if expected.startswith("sha256:"):
        expected = expected[len("sha256:") :]
    if not expected or expected.lower() != sha256.lower():
        raise ValueError(f"Extension checksum mismatch: expected {expected}, got {sha256}")
    return {
        "package_id": item["id"],
        "archive_path": str(path),
        "sha256": sha256,
        "package_kind": "extension",
        "version": item.get("version"),
        "blender_version_min": item.get("blender_version_min"),
        "blender_version_max": item.get("blender_version_max"),
        "license": item.get("license", []),
        "maintainer": item.get("maintainer"),
        "permissions": item.get("permissions", {}),
        "source_url": item.get("website"),
        "repository_url": REPOSITORY_URL,
    }


def download_extension(item: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
    url = str(item.get("archive_url") or "")
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != "extensions.blender.org":
        raise ValueError(f"Unexpected Blender extension download URL: {url}")
    target_dir = Path(output_dir).expanduser().resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / Path(parsed.path).name
    temporary = target.with_suffix(target.suffix + ".part")
    digest = hashlib.sha256()
    try:
        with _request(url, timeout=180) as response, temporary.open("wb") as stream:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                digest.update(chunk)
                stream.write(chunk)
        package = package_descriptor(item, target, digest.hexdigest())
        temporary.replace(target)
        return package
    finally:
        if temporary.exists():
            temporary.unlink()
