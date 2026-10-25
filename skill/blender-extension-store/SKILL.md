---
name: blender-extension-store
description: Search, inspect, and download add-ons from the official Blender Extensions repository.
license: MIT
compatibility: "dcc-mcp-core 0.19+, Python 3.9+"
metadata:
  dcc-mcp:
    version: v0.1.1
    dcc: blender
    layer: domain
    lifecycle: experimental
    tags:
      - asset
      - blender
      - extension
      - addon
      - download
    search-hint: "Blender Extensions official addon repository search download"
    produces: [blender_extension_package]
    tools: tools.yaml
---

# Blender Extension Store

Use this skill for the official `extensions.blender.org` repository. It returns
a checksum-verified package but does not modify Blender. Pass the `package` to
the bundled `blender-extensions` skill to plan and install it.
