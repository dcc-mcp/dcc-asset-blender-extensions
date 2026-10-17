from __future__ import annotations

from typing import Any, Optional

from _blender_extensions import inspect_extension
from dcc_mcp_core.skill import skill_entry, skill_exception, skill_success


@skill_entry
def main(
    extension_id: str,
    version: Optional[str] = None,
    blender_version: Optional[str] = None,
    **_: Any,
) -> dict[str, Any]:
    try:
        extension = inspect_extension(extension_id, version, blender_version)
        return skill_success("Official Blender extension inspected", extension=extension)
    except Exception as exc:  # noqa: BLE001 - Skill boundary returns a structured error for any failure.
        return skill_exception(exc, message="Failed to inspect official Blender extension")


if __name__ == "__main__":
    from dcc_mcp_core.skill import run_main

    run_main(main)
