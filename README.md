# DCC-MCP Blender Extensions

Search and download checksum-verified add-on packages from the official
[Blender Extensions](https://extensions.blender.org/) repository.

This provider does not modify Blender. Its `blender_extension_package` output
is consumed by the bundled `blender-extensions` host skill.

## Install

```bash
dcc-mcp-cli marketplace add dcc-mcp/dcc-asset-blender-extensions
dcc-mcp-cli marketplace install dcc-asset-blender-extensions
```

## Tools

- `search_blender_extensions`
- `inspect_blender_extension`
- `download_blender_extension`
