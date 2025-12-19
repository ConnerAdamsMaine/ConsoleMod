# ConsoleMod Project Structure

## Overview

ConsoleMod has been reorganized into a clean, modular structure. Related functionality is grouped into focused packages, making the codebase more maintainable and discoverable.

**Total structure:** 7 main modules + 36 Python files across 17 directories

```
ConsoleMod/
├── core/                    # Core terminal UI functionality
│   ├── __init__.py
│   ├── core.py              # TerminalSplitter class
│   ├── pane.py              # Pane class for content containers
│   └── events.py            # Event system (EventBus, KeyEvent, etc.)
│
├── ui/                      # User interface components
│   ├── __init__.py
│   ├── layout.py            # Layout management (vertical, horizontal, grid)
│   ├── themes.py            # Theme and style definitions
│   └── widgets.py           # UI widgets (ProgressBar, Spinner, Table, Button)
│
├── input/                   # Input handling
│   ├── __init__.py
│   ├── input.py             # Input field components
│   ├── input_handler.py     # Keyboard input handling
│   └── keybindings.py       # Keybinding management
│
├── interaction/             # User interaction components
│   ├── __init__.py
│   ├── forms.py             # Form components
│   ├── dialogs.py           # Dialog windows
│   ├── menus.py             # Menu components
│   └── input.py             # Input-related interaction classes
│
├── logging/                 # Logging functionality
│   ├── __init__.py
│   └── logging.py           # PaneLogger and logging utilities
│
├── monitoring/              # Performance and metrics monitoring
│   ├── __init__.py
│   ├── metrics.py           # PerformanceMonitor, MemoryMonitor
│   └── debounce.py          # Debouncer and throttling utilities
│
├── utils/                   # Utility functions and helpers
│   ├── __init__.py
│   ├── formatter.py         # Text formatting (wrapping, alignment, etc.)
│   ├── config.py            # Configuration management
│   ├── export.py            # Export utilities
│   ├── buffer.py            # CircularBuffer for efficient storage
│   ├── history.py           # History and undo/redo functionality
│   ├── console.py           # Console utilities
│   ├── utils.py             # Miscellaneous utilities
│   └── templates/           # Pre-built templates for common patterns
│       ├── __init__.py
│       ├── logger.py        # LoggerTemplate
│       ├── dashboard.py     # DashboardTemplate
│       ├── monitor.py       # MonitorTemplate
│       ├── progress.py      # ProgressTemplate
│       └── table.py         # TableTemplate
│
└── __init__.py              # Package exports

## Module Descriptions

### core/
The foundation of ConsoleMod, containing the main UI controller and pane management.

**Key Classes:**
- `TerminalSplitter`: Main UI controller for managing panes and rendering
- `Pane`: Content container with circular buffer storage
- `EventBus`: Event system for handling user interactions

### ui/
All visual UI components and styling.

**Key Classes/Functions:**
- `Layout`: Layout manager for pane arrangement
- `Theme`, `Style`: Theming and styling system
- `ProgressBar`, `Spinner`, `Table`, `Button`: UI widgets

### input/
Keyboard and user input handling.

**Key Classes:**
- `InputHandler`: Low-level keyboard input handling
- `InputField`, `SelectField`, `CheckboxField`: Input components
- `KeyBindingManager`: Keybinding configuration and management

### interaction/
High-level interactive components for user dialogs and forms.

**Key Classes:**
- `Form`: Multi-field form component
- `Dialog`, `ConfirmDialog`, `InputDialog`: Dialog windows
- `Menu`, `ContextMenu`: Menu systems

### logging/
Integrated logging system for panes.

**Key Classes:**
- `PaneLogger`: Logger that writes to panes with level coloring
- `LogLevel`: Log level definitions

### monitoring/
Performance and memory monitoring utilities.

**Key Classes:**
- `PerformanceMonitor`: Tracks FPS and frame timing
- `MemoryMonitor`: Tracks memory usage per pane
- `Debouncer`, `Throttler`: Rate limiting utilities

### utils/
General utility functions and helpers.

**Key Functions/Classes:**
- Text formatting: `wrap_text`, `align_text`, `format_bytes`, `create_box`
- `CircularBuffer`: Efficient circular buffer for content storage
- `CommandHistory`: History management with undo/redo
- `PaneExporter`: Export pane content to files
- Templates: Pre-built patterns for common UI layouts

## Import Patterns

### Importing from the main package:
```python
from ConsoleMod import TerminalSplitter, Pane, PaneLogger
from ConsoleMod import wrap_text, format_bytes
from ConsoleMod import ProgressBar, Dialog
```

### Importing from specific modules:
```python
from ConsoleMod.core import TerminalSplitter, Pane
from ConsoleMod.ui import Layout, LayoutMode, Theme
from ConsoleMod.input import InputHandler
from ConsoleMod.logging import PaneLogger, LogLevel
from ConsoleMod.utils import CircularBuffer, CommandHistory
```

## Design Principles

1. **Modular**: Each module has a clear, single responsibility
2. **Organized**: Related functionality is grouped together
3. **Scalable**: Easy to add new features without disrupting existing code
4. **Discoverable**: Clear hierarchy makes it easy to find what you need
5. **Documented**: Each module has clear __init__.py exports

## Future Organization

As the project grows, consider:
- Creating submodules for complex components (e.g., `ui/tables/`, `interaction/forms/`)
- Moving templates to their own top-level package if it grows significantly
- Potentially extracting examples to a separate directory
