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

## Key Features

- **Safe Save:** The extension automatically detects if a simulation is playing (Timeline is active) and **skips saving**. This prevents your USD file from accidentally persisting mid-motion robot poses as the new default state.
- **Smart Cooldown:** 5-second settle time ensures it doesn't spam saves during active dragging or property changes.
- **Dirty-State Aware:** Only saves if the stage actually has unsaved changes.

## Install

Clone this repo and add the extension path to Omniverse:

```bash
git clone https://github.com/ammarjmahmood/isaacsim_autosave.git ~/omni-autosave
```

Then in Isaac Sim or any Omniverse app:

1. Go to **Window > Extensions**
2. Click the **Gear Icon** (Settings)
3. Add the path to `~/omni-autosave/exts` as an extension search path
4. Search "AutoSave" and enable it

It auto-loads on every launch after that.

### Troubleshooting (Isaac Sim 5.1+)

If the extension doesn't load automatically after adding the path:

1. **Check your config:** In Isaac Sim 5.1, the search paths are stored in `user.config.json` under `"app": { "exts": { "folders": [...] } }`. 
2. **Immediate Enable (without restart):** Run this in the Isaac Sim Script Editor to force it to load immediately:

```python
import omni.kit.app
ext_manager = omni.kit.app.get_app().get_extension_manager()
# Add the path manually for this session
ext_manager.add_path("/home/USER/omni-autosave/exts")
# Enable it immediately
ext_manager.set_extension_enabled_immediate("omni.autosave", True)
```

3. **Stage URL:** AutoSave only triggers if the stage has already been saved to a file (it skips "Untitled" stages).

## How it works

One update loop subscription. Every tick it checks if 5 seconds have passed since the last save, then checks if the USD root layer is dirty (has unsaved changes) and if the timeline is NOT playing. If all are true, it calls `save_stage()` which is identical to Ctrl+S.

Two files total: `config/extension.toml` and `omni/autosave/extension.py`. ~40 lines of logic.
