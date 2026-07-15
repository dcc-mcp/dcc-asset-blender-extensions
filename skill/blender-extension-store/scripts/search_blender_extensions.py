from __future__ import annotations

from typing import Any, Dict, Optional

from dcc_mcp_core.skill import skill_entry, skill_exception, skill_success

from _blender_extensions import search_extensions


@skill_entry
def main(
    query: str,
    blender_version: Optional[str] = None,
    limit: int = 10,
    **_: Any,
) -> Dict[str, Any]:
    try:
        extensions = search_extensions(query, blender_version, limit)
        return skill_success(
            "Official Blender extensions found", extensions=extensions, count=len(extensions)
        )
    except Exception as exc:
        return skill_exception(exc, message="Failed to search official Blender extensions")


if __name__ == "__main__":
    from dcc_mcp_core.skill import run_main

    run_main(main)
