# omni-autosave

Automatic Ctrl+S for NVIDIA Omniverse and Isaac Sim. Install it once and never lose work again.

Listens for any stage modification, waits 5 seconds for edits to settle, then saves. No UI, no config, no setup. It just works.

## What it saves

Everything. The extension checks the USD root layer's dirty flag, which is set by any modification to the stage. This includes:

- Prim transforms (position, rotation, scale)
- Camera position and orientation
- Camera properties (focal length, aperture, clipping range)
- Adding, removing, or renaming prims
- Material and shader changes
- Light intensity, color, temperature
- Physics properties (mass, friction, joint drives)
- Render settings
- Custom attributes and metadata
- Referenced/payloaded asset changes
- Anything that would put an asterisk in the title bar

If Ctrl+S would save it, this extension saves it.

## Install

Clone this repo and add the extension path to Omniverse:

```
git clone https://github.com/ammarjmahmood/isaacsim_autosave.git
```

Then in Isaac Sim or any Omniverse app:

1. Go to **Window > Extensions**
2. Click the gear icon
3. Add the path to `isaacsim_autosave/exts` as an extension search path
4. Search "AutoSave" and enable it

It auto loads on every launch after that.

### Or just drop it in

Copy the `omni.autosave` folder into your Omniverse extensions directory:

```
cp -r exts/omni.autosave ~/.local/share/ov/pkg/isaac-sim-*/exts/
```

Done. It runs next time you launch.

### Install and test with an AI assistant

If you use Claude, Cursor, or Gemini CLI, paste this prompt directly into the chat and it will handle the full install and verify it's working:

```
I want to install the omni-autosave extension for Isaac Sim so it survives
updates and works regardless of where Isaac Sim is installed.

1. Clone the repo somewhere permanent (it needs to stay here):
   git clone https://github.com/ammarjmahmood/isaacsim_autosave.git ~/omni-autosave

2. Find my Isaac Sim installation. Check these locations in order and tell me
   which one exists:
   - ~/.local/share/ov/pkg/isaac-sim-*/
   - ~/isaac-sim/
   - /opt/isaac-sim/
   - $(python3 -c "import isaacsim; import os; print(os.path.dirname(isaacsim.__file__))" 2>/dev/null)
   Use whichever exists. If none found, ask me for the path.

3. Find the Isaac Sim user preferences folder where extension search paths are stored:
   - Linux: ~/.local/share/ov/data/Kit/Isaac-Sim/*/user.config.json
   - Windows: %USERPROFILE%\AppData\Local\ov\data\Kit\Isaac-Sim\*\user.config.json
   Show me the current contents of that file.

4. Add ~/omni-autosave/exts to the extension search paths in user.config.json
   so Isaac Sim finds the extension on every launch, including after updates.
   The key to add/append to is: "exts/folders"

5. Verify the three extension files exist at:
   ~/omni-autosave/exts/omni.autosave/config/extension.toml
   ~/omni-autosave/exts/omni.autosave/omni/autosave/extension.py
   ~/omni-autosave/exts/omni.autosave/omni/autosave/__init__.py

6. Confirm extension.toml contains `autoload = true` under
   [settings.exts."omni.autosave"].

7. Tell me the Isaac Sim path found, the preferences file updated, and confirm
   the install is complete.
```

Run that, then launch Isaac Sim. The extension loads automatically — no enabling required, survives Isaac Sim updates, works at any install path.

## How it works

One update loop subscription. Every tick it checks if 5 seconds have passed since the last save, then checks if the USD root layer is dirty (has unsaved changes). If both are true, it calls `save_stage()` which is identical to Ctrl+S. If you haven't saved the file yet (no file path exists), it skips.

Two files total: `config/extension.toml` and `omni/autosave/extension.py`. ~35 lines of logic.

## Using with Isaac Sim MCP + Claude

If you're using the [Isaac Sim MCP server](https://github.com/omni-mcp/isaac-sim-mcp) to control Isaac Sim through Claude or Cursor, this extension pairs perfectly with it. Every change the MCP server makes — spawning robots, moving prims, adjusting lights, changing camera focal length, running scripts — gets auto saved without you having to think about it.

### Setup

1. Install omni-autosave using either method above

2. Clone the Isaac Sim MCP server:

```
git clone https://github.com/omni-mcp/isaac-sim-mcp.git
cd isaac-sim-mcp
```

3. Launch Isaac Sim with both extensions loaded:

```
cd ~/.local/share/ov/pkg/isaac-sim-4.2.0
./isaac-sim.sh \
    --ext-folder /path/to/isaac-sim-mcp/ \
    --ext-folder /path/to/isaacsim_autosave/exts/ \
    --enable isaac.sim.mcp_extension \
    --enable omni.autosave
```

4. Start the MCP server:

```
uv pip install "mcp[cli]"
uv run /path/to/isaac-sim-mcp/isaac_mcp/server.py
```

5. Add the MCP server to Claude Desktop (`~/.config/claude/claude_desktop_config.json`):

```json
{
    "mcpServers": {
        "isaac-sim": {
            "command": "uv",
            "args": ["run", "--directory", "/path/to/isaac-sim-mcp", "nvidia-isaac-mcp"]
        }
    }
}
```

Or for Cursor, add it in Cursor preferences under MCP.

Now when Claude adds robots, changes lighting, moves objects, adjusts camera settings, or runs any simulation command through the MCP server, omni-autosave catches the stage change and saves it automatically. You get a full history of your work without ever hitting Ctrl+S.

## License

MIT
