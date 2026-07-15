from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "blender-extension-store"
SCRIPTS = SKILL / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


extensions = load("_blender_extensions")


def _item() -> dict:
    return {
        "id": "sample_extension",
        "name": "Sample Extension",
        "version": "1.2.3",
        "tagline": "Useful node workflow",
        "maintainer": "Example",
        "license": ["SPDX:GPL-3.0-or-later"],
        "tags": ["Node"],
        "type": "add-on",
        "blender_version_min": "4.2.0",
        "archive_hash": "sha256:abc123",
        "website": "https://extensions.blender.org/add-ons/sample-extension/",
    }


def test_search_filters_repository(monkeypatch) -> None:
    monkeypatch.setattr(extensions, "repository", lambda _version=None: {"data": [_item()]})
    result = extensions.search_extensions("node", blender_version="4.2.0")
    assert result[0]["id"] == "sample_extension"


def test_package_descriptor() -> None:
    package = extensions.package_descriptor(_item(), Path("sample.zip"), "abc123")
    assert package["package_id"] == "sample_extension"
    assert package["package_kind"] == "extension"
    assert package["license"] == ["SPDX:GPL-3.0-or-later"]


def test_skill_contract() -> None:
    from dcc_mcp_core import validate_skill

    report = validate_skill(str(SKILL))
    assert not report.has_errors, report
