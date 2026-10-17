from __future__ import annotations

import os

from test_blender_extensions import (
    extensions,
    test_package_descriptor,
    test_skill_contract,
)


def main() -> None:
    test_package_descriptor()
    test_skill_contract()
    if os.environ.get("RUN_LIVE_API_SMOKE") == "true":
        data = extensions.repository("4.2.0")
        assert data.get("data")
        assert data["data"][0].get("archive_hash", "").startswith("sha256:")
    else:
        print("skip live Blender Extensions API smoke")


if __name__ == "__main__":
    main()
