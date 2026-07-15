from __future__ import annotations

from typing import Any, Dict, Optional

from dcc_mcp_core.skill import skill_entry, skill_exception, skill_success

from _blender_extensions import inspect_extension


@skill_entry
def main(
    extension_id: str,
    version: Optional[str] = None,
    blender_version: Optional[str] = None,
    **_: Any,
) -> Dict[str, Any]:
    try:
        extension = inspect_extension(extension_id, version, blender_version)
        return skill_success("Official Blender extension inspected", extension=extension)
    except Exception as exc:
        return skill_exception(exc, message="Failed to inspect official Blender extension")


if __name__ == "__main__":
    from dcc_mcp_core.skill import run_main

    run_main(main)
