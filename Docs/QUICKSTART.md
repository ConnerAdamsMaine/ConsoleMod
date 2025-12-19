# ConsoleMod Quick Start Guide

Get up and running with ConsoleMod in 5 minutes.

**License:** 404_CM-v1.0 | **Support:** consolemode@404development.dev

---

## Installation

### Option 1: Direct Import
```python
import sys
sys.path.insert(0, '/path/to/ConsoleMod')
```

### Option 2: Install in Development Mode
```bash
cd /path/to/ConsoleMod
pip install -e .
```

---

## Your First App (2 minutes)

```python
import asyncio
from ConsoleMod import TerminalSplitter, Pane, PaneLogger

async def main():
    # 1. Create the UI controller
    splitter = TerminalSplitter(fps=30, theme="dark")
    
    # 2. Create panes
    logs = Pane("logs", color="green")
    status = Pane("status", color="blue")
    
    # 3. Add panes
    splitter.add_pane(logs)
    splitter.add_pane(status)
    
    # 4. Log messages
    logger = PaneLogger(logs)
    logger.info("App started!")
    
    # 5. Update status
    status.write("Ready to go!")
    
    # 6. Run
    await splitter.render_loop()

asyncio.run(main())
```

**Run it:**
```bash
python your_script.py
```

**Exit:** Press `Ctrl+C`

---

## Common Patterns

### Write to Pane
```python
# Sync
pane.write("Message")

# Async
await pane.awrite("Message")
```

### Log with Levels
```python
logger = PaneLogger(pane)
logger.debug("Debug")
logger.info("Info")
logger.warning("Warning")
logger.error("Error")
logger.critical("Critical")
```

### Handle Keyboard
```python
@splitter.event_bus.on_key
async def handle_key(event):
    if event.key == KeyCode.UP:
        print("Up pressed")
```

### Control Layout
```python
# Change layout
await splitter.aset_layout_mode(LayoutMode.HORIZONTAL)

# Set pane sizes
splitter.set_pane_weight("main", 2.0)
splitter.set_pane_weight("side", 1.0)
```

### Format Text
```python
from ConsoleMod import format_bytes, format_duration

size = format_bytes(1048576)      # "1.0 MB"
time = format_duration(3661)      # "1.0h"
```

---

## Module Quick Reference

| Module | Purpose |
|--------|---------|
| `core` | TerminalSplitter, Pane, EventBus |
| `ui` | Layout, Themes, Widgets |
| `input` | Keyboard input, KeyBindings |
| `interaction` | Forms, Dialogs, Menus |
| `logging` | PaneLogger, LogLevel |
| `monitoring` | Metrics, Performance, Debouncer |
| `utils` | Formatting, Config, Templates |

---

## Key Classes

### TerminalSplitter
Main UI controller - manages panes and rendering.

```python
splitter = TerminalSplitter(
    fps=30,                           # Update frequency
    theme="dark",                     # "dark", "light", "solarized"
    enable_input=True,                # Enable keyboard
    layout_mode=LayoutMode.VERTICAL,  # Layout type
    enable_metrics=False              # Performance tracking
)
```

### Pane
Content container - stores and displays text.

```python
pane = Pane(
    id="name",           # Unique ID
    color="green",       # Default color
    max_lines=1000       # Maximum lines to keep
)
```

### PaneLogger
Structured logging to panes.

```python
logger = PaneLogger(
    pane,                    # Target pane
    include_timestamp=True   # Show time
)
```

---

## Keyboard Controls (Default)

| Key | Action |
|-----|--------|
| Tab | Next pane |
| Shift+Tab | Previous pane |
| Up/Down | Scroll pane |
| Ctrl+C | Exit |

---

## Theming

### Built-in Themes
```python
splitter = TerminalSplitter(theme="dark")      # Default
splitter = TerminalSplitter(theme="light")     # Light
splitter = TerminalSplitter(theme="solarized") # Solarized
```

### Custom Styles
```python
from ConsoleMod import Style, Theme

style = Style(color="red", bold=True)

theme = Theme(
    name="custom",
    pane_border=style,
    pane_focus=style,
    # ... other styles
)
```

---

## Async/Sync Methods

Most methods have both sync and async versions:

```python
# Synchronous (blocks)
pane.write("Message")
pane.scroll(1, 5)

# Asynchronous (non-blocking)
await pane.awrite("Message")
await pane.ascroll(1, 5)
```

Use async versions in async contexts, sync versions otherwise.

---

## Tips & Tricks

### Keep Things Organized
```python
# Use descriptive pane IDs
logs_pane = Pane("logs")
status_pane = Pane("status")
debug_pane = Pane("debug")
```

### Prevent Text Overflow
```python
from ConsoleMod import wrap_text

lines = wrap_text(long_text, width=40)
for line in lines:
    pane.write(line)
```

### Format Sizes
```python
from ConsoleMod import format_bytes, format_duration

print(format_bytes(2_147_483_648))  # "2.0 GB"
print(format_duration(7322.5))       # "2.0h"
```

### Track Progress
```python
from ConsoleMod import ProgressBar

progress = ProgressBar(total=100)
for i in range(101):
    progress.increment(1)
    pane.write(progress.render())
```

### Get Performance Data
```python
metrics = splitter.get_performance_metrics()
print(f"FPS: {metrics['fps']}")
print(f"Avg frame: {metrics['avg_frame_time_ms']}ms")
```

---

## Common Issues

### "Module not found"
```python
# Make sure to install or add to path
import sys
sys.path.insert(0, '/path/to/ConsoleMod')
import ConsoleMod
```

### App won't respond
```python
# Use async properly
async def main():
    await splitter.render_loop()

asyncio.run(main())
```

### Text not showing
```python
# Add pane to splitter
splitter.add_pane(pane)

# Write text
pane.write("Message")
```

### Layout not updating
```python
# Use async setter
await splitter.aset_layout_mode(LayoutMode.HORIZONTAL)
```

---

## Next Steps

1. **Run Examples:** Check `example.py`, `advanced_example.py`
2. **Read Docs:** See [README.md](README.md) for full API
3. **Explore Modules:** See [STRUCTURE.md](STRUCTURE.md)
4. **Try Templates:** Use pre-built UI patterns
5. **Get Help:** Email consolemode@404development.dev

---

## Full API Reference

For complete API documentation, see [README.md](README.md)

Key sections:
- API Reference
- Widget Library
- Keyboard Shortcuts
- Thread Safety

---

## Common Recipes

### Multi-Pane Logger
```python
async def main():
    splitter = TerminalSplitter()
    
    info = Pane("info", color="green")
    warn = Pane("warning", color="yellow")
    err = Pane("error", color="red")
    
    splitter.add_pane(info)
    splitter.add_pane(warn)
    splitter.add_pane(err)
    
    info_log = PaneLogger(info)
    warn_log = PaneLogger(warn)
    err_log = PaneLogger(err)
    
    await splitter.render_loop()
```

### Status Dashboard
```python
async def main():
    splitter = TerminalSplitter(layout_mode=LayoutMode.HORIZONTAL)
    
    status = Pane("status")
    details = Pane("details")
    
    splitter.add_pane(status)
    splitter.add_pane(details)
    
    splitter.set_pane_weight("status", 1.0)
    splitter.set_pane_weight("details", 2.0)
    
    await splitter.render_loop()
```

### Keyboard Interaction
```python
async def main():
    splitter = TerminalSplitter(enable_input=True)
    pane = Pane("main")
    splitter.add_pane(pane)
    
    @splitter.event_bus.on_key
    async def handle_keys(event):
        pane.write(f"Key: {event.key}")
    
    await splitter.render_loop()
```

---

## Performance Tips

1. **Limit line count:** Set `max_lines` on panes
2. **Use debouncing:** For frequent updates
3. **Lower FPS:** If CPU is high
4. **Clear panes:** Remove old content
5. **Use circular buffer:** Automatic with Pane

---

## Debugging

### Show metrics
```python
splitter = TerminalSplitter(enable_metrics=True)
metrics = splitter.get_performance_metrics()
print(metrics)
```

### Enable async debugging
```python
import asyncio
asyncio.run(main(), debug=True)
```

### Print pane state
```python
pane = splitter.get_pane("logs")
print(f"Lines: {len(pane.content)}")
```

---

## Support

**Having issues?** Contact: consolemode@404development.dev

**Check these first:**
1. Have you installed ConsoleMod?
2. Are you in an async context?
3. Did you add panes to the splitter?
4. Is your Python version 3.7+?

---

## License

ConsoleMod is licensed under **404_CM-v1.0** (Hobby Software License)

**Key rules:**
- ✓ Use for hobby/personal projects
- ✓ Modify and expand
- ✗ No commercial use
- ✗ Cannot profit
- ✓ Must credit contributors

See [404_CM-v1.0](404_CM-v1.0) for full license.

---

## Resources

- **Main README:** [README.md](README.md)
- **Module Guide:** [STRUCTURE.md](STRUCTURE.md)
- **License:** [404_CM-v1.0](404_CM-v1.0)
- **Contributors:** [CONTRIBUTORS.md](CONTRIBUTORS.md)
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)
- **Support:** consolemode@404development.dev

---

*Happy coding! ConsoleMod is a hobby project built by the community.*  
*License: 404_CM-v1.0 | Support: consolemode@404development.dev*
