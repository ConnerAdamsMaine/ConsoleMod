# Architecture Documentation

## Overview

ConsoleMod is a modern, thread-safe terminal UI library built on Python 3.9+ with async/await support. The architecture emphasizes modularity, thread safety, and performance.

## Core Design Principles

1. **Thread Safety** - All components use RLock-based synchronization
2. **Dual API** - Both sync and async versions of all operations
3. **Modularity** - Independent, composable modules
4. **Performance** - Efficient rendering with configurable frame rates
5. **Extensibility** - Easy to customize themes, widgets, and behaviors

## Module Structure

```
ConsoleMod/
├── core/              # Terminal UI foundation
│   ├── core.py        # TerminalSplitter main controller
│   ├── pane.py        # Pane content containers
│   └── events.py      # Event system and handlers
├── ui/                # Visual components
│   ├── layout.py      # Layout modes and calculations
│   ├── themes.py      # Theme management
│   └── widgets.py     # UI components (Button, ProgressBar, etc.)
├── input/             # Keyboard input handling
│   ├── input.py       # Input capture and processing
│   ├── input_handler.py # Event handler management
│   └── keybindings.py # Keybinding definitions
├── interaction/       # User interaction components
│   ├── dialogs.py     # Modal dialogs
│   ├── forms.py       # Form components
│   └── menus.py       # Menu systems
├── logging/           # Pane-based logging
│   └── logging.py     # PaneLogger and formatters
├── monitoring/        # Performance monitoring
│   ├── metrics.py     # Performance metrics collection
│   └── debounce.py    # Input debouncing utilities
└── utils/             # Utilities and helpers
    ├── buffer.py      # Circular buffer implementation
    ├── config.py      # Configuration management
    ├── formatter.py   # Text formatting utilities
    ├── history.py     # Command history
    ├── console.py     # Console utilities
    ├── export.py      # Content export
    └── templates/     # UI templates
```

## Core Components

### TerminalSplitter

The main controller managing the terminal UI:

```python
class TerminalSplitter:
    - Manages pane collection
    - Handles layout modes (vertical, horizontal, grid)
    - Coordinates rendering loop
    - Manages event system
    - Tracks performance metrics
```

**Key Responsibilities:**
- Orchestrate pane rendering
- Handle layout calculations
- Manage focus and navigation
- Process keyboard input
- Monitor performance

### Pane

Content container with circular buffer storage:

```python
class Pane:
    - Stores lines of text
    - Manages scroll position
    - Handles text formatting
    - Thread-safe operations
    - Configurable max lines
```

**Key Responsibilities:**
- Store and manage content
- Provide scroll functionality
- Render visible content
- Support async writes
- Maintain focus state

### Event System

Keyboard and custom events:

```python
class EventBus:
    - Register event handlers
    - Process keyboard input
    - Support async/sync handlers
    - Multiple handler support
```

**Event Types:**
- KeyEvent - Keyboard input
- CustomEvent - Application events
- FocusEvent - Pane focus changes

## Threading and Concurrency

### Thread Safety Strategy

1. **RLock Protection** - All mutable state protected by RLock
2. **Atomic Operations** - State changes are atomic
3. **Queue-based Communication** - Cross-thread communication via queues
4. **Non-blocking I/O** - Async operations don't block threads

### Thread Model

```
Main Thread (Render Loop)
    └── Updates display
    └── Processes input
    └── Calls event handlers

Worker Threads
    └── Write to panes (thread-safe)
    └── Queue events
    └── Async operations

Input Thread
    └── Captures keyboard input
    └── Pushes to event queue
```

### Synchronization

```python
# Pane-level locking
with pane._lock:
    pane._lines.append(text)

# Splitter-level locking
with splitter._lock:
    splitter._panes[pane_id] = pane
```

## Async/Await Support

### Dual API Pattern

Every operation has both sync and async versions:

```python
# Synchronous
pane.write("Message")
content = pane.get_visible_content(10)

# Asynchronous
await pane.awrite("Message")
content = await pane.aget_visible_content(10)
```

### Event Loop Integration

```python
# Async render loop
async def render_loop():
    while running:
        await process_input()
        await render_frame()
        await asyncio.sleep(frame_time)
```

## Rendering Pipeline

### Frame Rendering Process

1. **Input Phase** - Capture keyboard input
2. **Update Phase** - Process events and updates
3. **Render Phase** - Calculate layout and render panes
4. **Display Phase** - Output to terminal
5. **Sleep Phase** - Wait for next frame

### Layout Calculation

```python
def calculate_layout(panes, mode, size):
    if mode == VERTICAL:
        return calculate_vertical(panes, size)
    elif mode == HORIZONTAL:
        return calculate_horizontal(panes, size)
    elif mode == GRID:
        return calculate_grid(panes, size)
```

## Memory Management

### Circular Buffer Strategy

```python
class CircularBuffer:
    - Fixed max_size
    - Overwrites oldest when full
    - O(1) append and access
    - Efficient memory usage
```

### Per-Pane Management

- Each pane has configurable max_lines
- Old content automatically discarded
- Memory usage bounded and predictable

## Event Handling

### Event Flow

```
Keyboard Input
    ↓
Input Handler
    ↓
Event Bus
    ↓
Registered Handlers (sync/async)
    ↓
Update State / Render
```

### Handler Registration

```python
@splitter.event_bus.on_key
async def handle_key(event):
    if event.key == KeyCode.UP:
        await pane.ascroll("up", 1)
```

## Performance Optimization

### Frame Timing

```python
target_fps = 30
frame_time = 1.0 / target_fps  # ~33ms

loop:
    start = time.time()
    render_frame()
    elapsed = time.time() - start
    sleep_time = max(0, frame_time - elapsed)
    sleep(sleep_time)
```

### Metrics Collection

```python
class PerformanceMetrics:
    - FPS tracking
    - Frame time measurement
    - Render time breakdown
    - Memory usage tracking
```

## Theme System

### Theme Structure

```python
class Theme:
    primary: Color
    secondary: Color
    background: Color
    accent: Color
    styles: Dict[str, Style]
```

### Theme Application

```python
# Apply theme globally
splitter.set_theme("dark")

# Apply style to specific element
pane.apply_style(Style(color="red", bold=True))
```

## Configuration Management

### Config File Support

```yaml
# config.yaml
fps: 30
theme: dark
layout: vertical
max_pane_lines: 1000
enable_metrics: true
```

### Runtime Configuration

```python
splitter.set_fps(60)
await splitter.aset_theme("light")
```

## Error Handling

### Exception Strategy

1. **Validate Input** - Check parameters early
2. **Fail Fast** - Raise errors immediately
3. **Cleanup Resources** - Always cleanup on error
4. **Log Errors** - Record errors for debugging

### Error Recovery

```python
try:
    await operation()
except OperationError as e:
    log_error(e)
    handle_error(e)
finally:
    cleanup()
```

## Testing Strategy

### Test Coverage

- Unit tests for all components
- Integration tests for interactions
- Thread safety tests
- Async operation tests
- Performance benchmarks

### Test Organization

```
tests/
├── test_core.py      # Core components
├── test_ui.py        # UI widgets
├── test_logging.py   # Logging functionality
└── test_utils.py     # Utilities
```

## Extension Points

### Custom Widgets

```python
class CustomWidget(Widget):
    def render(self) -> str:
        return "Custom content"
```

### Custom Themes

```python
custom_theme = Theme(
    name="custom",
    primary="blue",
    secondary="cyan"
)
```

### Custom Event Handlers

```python
@splitter.event_bus.on_key
async def custom_handler(event):
    # Custom handling
    pass
```

## Compatibility

### Python Versions

- Python 3.9+
- Full type hints support
- Modern async/await syntax

### Operating Systems

- Linux (Ubuntu, Fedora, etc.)
- macOS
- Windows (with appropriate terminal)

## Dependency Graph

```
consolemod/
├── core
│   ├── ui (layout, themes)
│   ├── input (keybindings)
│   └── monitoring (metrics)
├── logging
│   └── core (Pane)
├── interaction
│   ├── ui (widgets)
│   └── input (keybindings)
└── utils
    └── [no internal dependencies]
```

## Performance Characteristics

### Time Complexity

- Pane write: O(1)
- Pane scroll: O(1)
- Layout calculation: O(n) where n = number of panes
- Render frame: O(n * m) where n = panes, m = lines visible

### Space Complexity

- Pane storage: O(max_lines)
- Total memory: O(panes * max_lines)
- Bounded and configurable

## Future Architecture Improvements

1. **Plugin System** - Allow plugins for custom components
2. **State Management** - Redux-like state management
3. **Networking** - Remote pane synchronization
4. **Visualization** - Graphics/chart components
5. **Mobile Support** - Mobile terminal support

## References

- [Design Patterns](https://refactoring.guru/design-patterns)
- [Async IO](https://docs.python.org/3/library/asyncio.html)
- [Threading](https://docs.python.org/3/library/threading.html)
