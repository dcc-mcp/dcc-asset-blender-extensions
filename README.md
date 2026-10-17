# DCC-MCP Blender Extensions

<p align="center">
  <img src="docs/assets/dcc-asset-blender-extensions.svg" alt="DCC-MCP · BLENDER-EXTENSIONS" width="600">
</p>

## Agent workflow

AI agents should use installed package skills through the shared gateway. IDE
users may continue to use the MCP endpoint.

### Install or update the CLI

`dcc-mcp-cli` is the preferred control path for every shell-capable agent. If
it is missing, ask the user before installing the latest official release:

On Linux/macOS, download and inspect the installer:

```bash
curl -fL https://raw.githubusercontent.com/dcc-mcp/dcc-mcp-core/main/scripts/install-cli.sh -o install-cli.sh
cat install-cli.sh
```

After completing the inspection and obtaining the user's permission to install:

```bash
sh ./install-cli.sh
```

On Windows PowerShell, download and inspect the installer:

```powershell
Invoke-WebRequest https://raw.githubusercontent.com/dcc-mcp/dcc-mcp-core/main/scripts/install-cli.ps1 -OutFile .\install-cli.ps1
Get-Content -Raw .\install-cli.ps1
```

After completing the inspection and obtaining the user's permission to install,
run the reviewed local installer under the current execution policy:

```powershell
& .\install-cli.ps1
```

Keep an official build current through the release manifest:

```bash
dcc-mcp-cli update check
```

Only after the user explicitly confirms the update:

```bash
dcc-mcp-cli update apply --yes
```

`update apply` downloads and stages the latest CLI for the next launch. It
does not update a running `dcc-mcp-server`; update that server in its own
environment.

Use `--require-gateway` for task calls so Gateway audit/stats records them.
This fails closed instead of falling back to direct MCP. Choose one stable
`<task-id>` and pass it to every tool call with `--agent-session-id`. This sets
`_meta.agent_context.session_id`; reuse the same ID in `stats --session-id`
after the task.

```bash
dcc-mcp-cli dcc-types
dcc-mcp-cli list
dcc-mcp-cli search --query "<task>" --dcc-type <host>
dcc-mcp-cli describe <tool-slug>
dcc-mcp-cli call <tool-slug> --require-gateway --agent-session-id "<task-id>" --json '{"key":"value"}'
```

If the package skill is not active, call
`dcc-mcp-cli load-skill <skill-name> --dcc-type <host>`. After the task,
query `dcc-mcp-cli stats --range "<task-window>" --session-id "<task-id>"` and pass only
bounded evidence to the `review_skill_improvement` prompt from
`dcc-mcp-skills-creator`.
Choose a supported `--range` covering the full task start-to-review window;
see `dcc-mcp-cli stats --help`.


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
