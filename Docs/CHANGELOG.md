# ConsoleMod Changelog

All notable changes to ConsoleMod are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

**Project:** ConsoleMod - Terminal UI Library  
**License:** 404_CM-v1.0 (Hobby Software License)  
**Support:** consolemode@404development.dev

---

## [Unreleased]

### Planned Features

- [ ] Remote UI support (over network)
- [ ] Plugin system for extensions
- [ ] Built-in debugger/profiler
- [ ] Additional widget library
- [ ] Configuration file support (JSON/YAML)
- [ ] Mouse input support (partial)
- [ ] Terminal recording/playback
- [ ] Extended color palette support

---

## [0.2.0] - 2025-12-19

### Added

#### Build & Packaging

- pyproject.toml with full project metadata and dependencies
- Version management with VERSION file and ConsoleMod/__version__.py
- CI/CD workflow with GitHub Actions (.github/workflows/ci.yml)
  - Multi-platform testing (Ubuntu, Windows, macOS)
  - Multi-version Python testing (3.7-3.11)
  - Linting with flake8
  - Type checking with mypy
  - Code formatting with black
  - Build distribution and artifact upload

#### Testing Infrastructure

- Test directory structure (tests/)
- pytest configuration in conftest.py
- pytest and pytest-asyncio in dev dependencies

### Changed

- Improved project structure with standardized packaging
- Enhanced development workflow with automated CI/CD

---

## [0.1.0] - 2025-12-19

### Added

#### Core Framework

- Initial TerminalSplitter implementation with multi-pane support
- Thread-safe pane management with RLock synchronization
- Async/sync dual API for all public methods
- Circular buffer storage for efficient memory usage
- Dynamic pane creation and management

#### UI System

- Layout system with VERTICAL, HORIZONTAL, and GRID modes
- Per-pane weight control for flexible sizing
- Dynamic layout mode switching at runtime
- Theming engine with pre-built themes (Dark, Light, Solarized)
- Style system with comprehensive formatting options
- Rich text formatting and markup support

#### Keyboard & Input

- Non-blocking async keyboard input handling
- Comprehensive key mapping and event handling
- KeyCode enumeration for all standard keys
- Keyboard event bus with async/sync handlers
- Keybinding manager for custom key mappings
- Tab navigation between panes
- Arrow key scrolling

#### Widgets

- ProgressBar with percentage display
- Spinner with animation
- Table with column alignment
- Button with click callbacks
- InputField with text input
- SelectField for selections
- CheckboxField for boolean input

#### Logging System

- PaneLogger with automatic level coloring
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Timestamp support
- Integration with Python logging module
- StdoutPaneAdapter for stream redirection
- Async and sync logging methods

#### Formatting Utilities

- Text wrapping with custom width
- Text alignment (left, center, right)
- Text truncation with custom suffixes
- Human-readable byte formatting
- Duration formatting (seconds to human readable)
- Box drawing with styles
- Syntax highlighting support

#### Performance Monitoring

- FPS tracking and reporting
- Frame timing metrics (average, max)
- Per-pane memory monitoring
- Performance metrics collection
- Memory usage breakdown

#### Utility Features

- CommandHistory with navigation
- UndoRedoStack for state management
- Debouncer and Throttler for rate limiting
- PaneExporter for content export
- CircularBuffer implementation
- Configuration management

#### Templates

- LoggerTemplate for logging UIs
- DashboardTemplate for status displays
- MonitorTemplate for monitoring systems
- ProgressTemplate for progress tracking
- TableTemplate for data display

#### Documentation

- Comprehensive README with examples
- Module structure documentation (STRUCTURE.md)
- API reference documentation
- Quick start guide
- Multiple usage examples
- Architecture documentation

#### Licensing & Attribution

- Custom 404_CM-v1.0 hobby software license
- Contributors file for attribution
- License enforcement and documentation
- Clear terms for hobby vs commercial use

#### Code Organization

- 7 main module packages
- 36 Python source files
- Clean import structure
- Proper module hierarchy
- Documentation for each module

### Changed

- Organized codebase from flat structure to modular packages
- Improved import organization and module discovery
- Enhanced documentation clarity

### Fixed

- Resolved circular import issues
- Fixed relative imports across modules
- Corrected template import paths

### Developer Experience

- Clear module organization for navigation
- Comprehensive examples for all features
- Detailed docstrings throughout codebase
- Support email for questions

---

## Version Comparison

### v0.1.0 Features Summary

| Feature             | Status | Type       |
| ------------------- | ------ | ---------- |
| Multi-pane UI       | ✓      | Core       |
| Async/Sync API      | ✓      | Core       |
| Thread Safety       | ✓      | Core       |
| Theming System      | ✓      | UI         |
| Keyboard Input      | ✓      | Input      |
| Logging             | ✓      | Logging    |
| Widgets             | ✓      | UI         |
| Performance Metrics | ✓      | Monitoring |
| Templates           | ✓      | Utils      |
| Documentation       | ✓      | Docs       |
| Examples            | ✓      | Docs       |

---

## Breaking Changes

None (Initial Release)

---

## Migration Guide

None required for v0.1.0 (Initial Release)

---

## Known Issues

### Current Limitations

- Mouse input not yet supported
- Limited to terminal capabilities of host system
- Some Unicode characters may not render on all terminals
- Performance depends on terminal capabilities

### Potential Issues

- Very large panes (>10000 lines) may impact memory
- Rapid updates may exceed rendering capacity on slow systems
- Custom fonts/colors depend on terminal support

---

## Performance Notes

### Optimization Status

- ✓ Circular buffers for memory efficiency
- ✓ Debouncing for rapid updates
- ✓ Non-blocking I/O
- ✓ Minimal rendering overhead
- ⚠ GPU acceleration not supported
- ⚠ Very large datasets need optimization

### Benchmarks

- Default FPS: 30 (configurable 1-60)
- Average frame time: ~33ms
- Memory per pane: ~2MB (1000 lines)
- Startup time: <100ms

---

## Dependencies

### Required

- Python 3.7+
- Rich library (for rendering)

### Standard Library

- asyncio (async support)
- threading (thread safety)
- logging (standard logging)
- collections (CircularBuffer)

### Optional

- readchar (for some input handling)

---

## Credits

### Project

- **Original Developer:** 404Development LLC
- **Project Coordinator:** Conner Adams

### Framework

- Built with Python standard library
- Rendering powered by Rich library

### Contributors

See [CONTRIBUTORS.md](CONTRIBUTORS.md) for detailed credits.

---

## Future Roadmap

### Phase 2 (Planned)

- Extended widget library
- Network UI support
- Plugin system
- Configuration file support
- Mouse input
- Terminal recording

### Phase 3 (Proposed)

- Remote UI
- Debugger integration
- Performance profiler
- Extended color support
- Terminal themes

### Phase 4 (Vision)

- Web-based UI
- Multi-terminal support
- Advanced graphics
- Full GUI feature parity

---

## Support

For issues, questions, or suggestions regarding versioning or changes:

- **Email:** consolemode@404development.dev
- **License:** 404_CM-v1.0

---

## How to Report Issues

When reporting issues, please include:

1. **Version:** ConsoleMod version (e.g., 0.1.0)
2. **Python Version:** Your Python version
3. **OS/Terminal:** Your operating system and terminal
4. **Description:** Clear description of the issue
5. **Reproduction:** Steps to reproduce the problem
6. **Expected:** What should happen
7. **Actual:** What actually happens

Email: consolemode@404development.dev

---

## Release Schedule

- **v0.1.0:** December 19, 2025 (Initial Release)
- **v0.2.0:** December 19, 2025 (Build & packaging infrastructure)
- **v1.0.0:** TBD (Stable release)

This is a hobby project without fixed release schedules.

---

## License Information

All versions of ConsoleMod are released under the 404_CM-v1.0 license.

**Key Points:**

- Hobby use only
- No commercial use allowed
- Attribution required
- Modifications allowed
- Distribution allowed (for hobby use)

See [404_CM-v1.0](404_CM-v1.0) for complete license terms.

---

## Acknowledgments

Thank you to:

- The Python community
- Rich library developers
- All users and testers
- Contributors and supporters

Your feedback helps make ConsoleMod better for everyone!

---

_This changelog is maintained as part of the ConsoleMod project._  
_Last Updated: December 19, 2025_  
_License: 404_CM-v1.0_
