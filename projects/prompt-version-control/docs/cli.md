# CLI Reference

## Global Options

All commands support the `--json` flag to output results as JSON for machine-readable parsing.

## Commands

### `pv save`

Save a new version of a prompt.

```bash
pv save <name> --content "Your prompt text here"
pv save <name> --file path/to/prompt.txt
pv save <name> --content "Prompt" --meta model=gpt-4 --meta temperature=0.7
```

**Arguments:**
- `name` — Name of the prompt (required).

**Options:**
- `--content, -c` — Prompt content as a string.
- `--file, -f` — Path to a file containing the prompt content.
- `--meta, -m` — Metadata as key=value pairs (can be repeated).
- `--json` — Output the saved version as JSON.

**Notes:**
- Either `--content` or `--file` must be provided, but not both.
- Version numbers are auto-incremented starting from `1.0`.

### `pv get`

Retrieve a prompt version.

```bash
pv get <name>
pv get <name> --version 1.0
pv get <name> --tag production
```

**Arguments:**
- `name` — Name of the prompt (required).

**Options:**
- `--version, -v` — Specific version number to retrieve.
- `--tag, -t` — Retrieve the version associated with a tag.
- `--json` — Output the version as JSON.

**Notes:**
- Without `--version` or `--tag`, returns the latest version.

### `pv list`

List all prompts or all versions of a specific prompt.

```bash
pv list
pv list --name greeting
```

**Options:**
- `--name, -n` — List versions of a specific prompt instead of all prompts.
- `--json` — Output as JSON.

### `pv tag`

Tag a specific version of a prompt.

```bash
pv tag <name> <version> <tag_name>
```

**Arguments:**
- `name` — Name of the prompt (required).
- `version` — Version number to tag (required).
- `tag_name` — Tag name (required).

**Options:**
- `--json` — Output the tag details as JSON.

**Notes:**
- If the tag already exists, it will be updated to point to the new version.

### `pv diff`

Show a unified diff between two versions of a prompt.

```bash
pv diff <name> <v1> <v2>
```

**Arguments:**
- `name` — Name of the prompt (required).
- `v1` — First version number (required).
- `v2` — Second version number (required).

### `pv delete`

Delete all versions of a prompt.

```bash
pv delete <name>
```

**Arguments:**
- `name` — Name of the prompt to delete (required).

**Options:**
- `--json` — Output deletion confirmation as JSON.

## Exit Codes

| Code | Meaning     |
|------|-------------|
| 0    | Success     |
| 1    | Not found   |
| 2    | Error       |
