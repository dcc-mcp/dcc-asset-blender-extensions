# DCC-MCP Blender Extensions

<p align="center">
  <img src="docs/assets/dcc-asset-blender-extensions.svg" alt="DCC-MCP · BLENDER-EXTENSIONS" width="600">
</p>

## Agent workflow

AI agents should use installed package skills through the shared gateway. IDE
users may continue to use the MCP endpoint.

```bash
dcc-mcp-cli dcc-types
dcc-mcp-cli list
dcc-mcp-cli search --query "<task>" --dcc-type <host>
dcc-mcp-cli describe <tool-slug>
dcc-mcp-cli call <tool-slug> --json '{"key":"value"}'
```

If the package skill is not active, call
`dcc-mcp-cli load-skill <skill-name> --dcc-type <host>`. After the task,
query `dcc-mcp-cli stats --range 24h --session-id <task-id>` and pass only
bounded evidence to the `review_skill_improvement` prompt from
`dcc-mcp-skills-creator`.


![Workflow showcase](docs/images/dcc-asset-blender-extensions-showcase.webp)

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
