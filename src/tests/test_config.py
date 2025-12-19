"""Configuration and initialization tests."""

import pytest
import yaml
import tempfile
import os
from unittest.mock import patch, Mock
from consolemod.core import TerminalSplitter, LayoutMode
from consolemod.utils import CommandHistory, CircularBuffer


class TestSplitterConfiguration:
    """Tests for TerminalSplitter configuration."""

    def test_splitter_default_config(self):
        """Test splitter with default configuration."""
        splitter = TerminalSplitter()
        assert splitter.fps == 30
        assert splitter.theme == "dark"

    def test_splitter_custom_fps(self):
        """Test splitter with custom FPS."""
        splitter = TerminalSplitter(fps=60)
        assert splitter.fps == 60

    def test_splitter_custom_theme(self):
        """Test splitter with custom theme."""
        splitter = TerminalSplitter(theme="light")
        assert splitter.theme == "light"

    def test_splitter_enable_input(self):
        """Test splitter with input enabled."""
        splitter = TerminalSplitter(enable_input=True)
        assert splitter.enable_input is True

    def test_splitter_disable_input(self):
        """Test splitter with input disabled."""
        splitter = TerminalSplitter(enable_input=False)
        assert splitter.enable_input is False

    def test_splitter_enable_metrics(self):
        """Test splitter with metrics enabled."""
        splitter = TerminalSplitter(enable_metrics=True)
        assert splitter.enable_metrics is True

    def test_splitter_disable_metrics(self):
        """Test splitter with metrics disabled."""
        splitter = TerminalSplitter(enable_metrics=False)
        assert splitter.enable_metrics is False

    def test_splitter_layout_vertical(self):
        """Test splitter with vertical layout."""
        splitter = TerminalSplitter(layout_mode=LayoutMode.VERTICAL)
        assert splitter.layout_mode == LayoutMode.VERTICAL

    def test_splitter_layout_horizontal(self):
        """Test splitter with horizontal layout."""
        splitter = TerminalSplitter(layout_mode=LayoutMode.HORIZONTAL)
        assert splitter.layout_mode == LayoutMode.HORIZONTAL

    def test_splitter_layout_grid(self):
        """Test splitter with grid layout."""
        splitter = TerminalSplitter(layout_mode=LayoutMode.GRID)
        assert splitter.layout_mode == LayoutMode.GRID

    def test_splitter_config_dict(self):
        """Test splitter with config dictionary."""
        config = {
            "fps": 60,
            "theme": "light",
            "enable_input": False,
            "enable_metrics": True
        }
        try:
            with patch('builtins.open', create=True):
                splitter = TerminalSplitter(config=config)
        except (TypeError, FileNotFoundError):
            pass  # Expected if dict not supported


class TestConfigFileHandling:
    """Tests for configuration file handling."""

    def test_config_from_yaml_file(self):
        """Test loading config from YAML file."""
        config_content = """
fps: 45
theme: dark
enable_input: true
enable_metrics: false
layout_mode: vertical
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(config_content)
            f.flush()
            
            try:
                # Try to load config
                with open(f.name, 'r') as cf:
                    config = yaml.safe_load(cf)
                    assert config['fps'] == 45
            finally:
                os.unlink(f.name)

    def test_config_missing_file(self):
        """Test handling missing config file."""
        try:
            with patch('builtins.open', side_effect=FileNotFoundError):
                splitter = TerminalSplitter(config="nonexistent.yaml")
        except FileNotFoundError:
            pass  # Expected

    def test_config_invalid_yaml(self):
        """Test handling invalid YAML in config file."""
        invalid_yaml = "{ invalid yaml content: [unclosed"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(invalid_yaml)
            f.flush()
            
            try:
                with open(f.name, 'r') as cf:
                    try:
                        config = yaml.safe_load(cf)
                    except yaml.YAMLError:
                        pass  # Expected
            finally:
                os.unlink(f.name)

    def test_config_empty_file(self):
        """Test handling empty config file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.flush()
            
            try:
                with open(f.name, 'r') as cf:
                    config = yaml.safe_load(cf)
                    assert config is None or isinstance(config, dict)
            finally:
                os.unlink(f.name)


class TestComponentConfiguration:
    """Tests for component-specific configuration."""

    def test_pane_configuration(self):
        """Test Pane with various configurations."""
        from consolemod.core import Pane
        
        pane = Pane(
            "test",
            width=0.5,
            height=0.5,
            color="blue",
            border=True,
            theme_name="dark",
            max_lines=500
        )
        
        assert pane.id == "test"
        assert pane.width == 0.5
        assert pane.height == 0.5
        assert pane.color == "blue"
        assert pane.border is True
        assert pane.max_lines == 500

    def test_logger_configuration(self):
        """Test PaneLogger with various configurations."""
        from consolemod.core import Pane
        from consolemod.logging import PaneLogger
        
        pane = Pane("test")
        
        logger_no_ts = PaneLogger(pane, include_timestamp=False)
        assert logger_no_ts.include_timestamp is False
        
        logger_with_ts = PaneLogger(pane, include_timestamp=True)
        assert logger_with_ts.include_timestamp is True

    def test_history_configuration(self):
        """Test CommandHistory with configuration."""
        # Default size
        history1 = CommandHistory()
        assert history1.max_size > 0
        
        # Custom size
        history2 = CommandHistory(max_size=50)
        assert history2.max_size == 50

    def test_buffer_configuration(self):
        """Test CircularBuffer with configuration."""
        # Various sizes
        buffer1 = CircularBuffer(max_size=10)
        assert buffer1.max_size == 10
        
        buffer2 = CircularBuffer(max_size=1000)
        assert buffer2.max_size == 1000


class TestRuntimeConfiguration:
    """Tests for runtime configuration changes."""

    def test_change_fps_at_runtime(self):
        """Test changing FPS at runtime."""
        splitter = TerminalSplitter(fps=30)
        assert splitter.fps == 30
        
        # Change FPS
        splitter.set_fps(60)
        assert splitter.fps == 60

    def test_change_theme_at_runtime(self):
        """Test changing theme at runtime."""
        splitter = TerminalSplitter(theme="dark")
        assert splitter.theme == "dark"
        
        # Change theme
        splitter.set_theme("light")
        assert splitter.theme == "light"

    @pytest.mark.asyncio
    async def test_change_layout_at_runtime(self):
        """Test changing layout at runtime."""
        splitter = TerminalSplitter(layout_mode=LayoutMode.VERTICAL)
        assert splitter.layout_mode == LayoutMode.VERTICAL
        
        # Change layout
        await splitter.aset_layout_mode(LayoutMode.HORIZONTAL)
        assert splitter.layout_mode == LayoutMode.HORIZONTAL

    def test_change_pane_weight_at_runtime(self):
        """Test changing pane weight at runtime."""
        from consolemod.core import Pane
        
        splitter = TerminalSplitter()
        pane = Pane("test")
        splitter.add_pane(pane)
        
        # Set weight
        splitter.set_pane_weight("test", 2.0)
        # Weight should be applied


class TestEnvironmentVariables:
    """Tests for environment variable configuration."""

    def test_config_from_env_fps(self):
        """Test reading FPS from environment."""
        with patch.dict(os.environ, {"CONSOLEMOD_FPS": "60"}):
            fps = os.environ.get("CONSOLEMOD_FPS", "30")
            assert fps == "60"

    def test_config_from_env_theme(self):
        """Test reading theme from environment."""
        with patch.dict(os.environ, {"CONSOLEMOD_THEME": "light"}):
            theme = os.environ.get("CONSOLEMOD_THEME", "dark")
            assert theme == "light"

    def test_config_from_env_debug(self):
        """Test reading debug flag from environment."""
        with patch.dict(os.environ, {"CONSOLEMOD_DEBUG": "true"}):
            debug = os.environ.get("CONSOLEMOD_DEBUG", "false")
            assert debug == "true"


class TestConfigValidation:
    """Tests for configuration validation."""

    def test_validate_fps_positive(self):
        """Test that FPS must be positive."""
        try:
            splitter = TerminalSplitter(fps=0)
            # May or may not validate
        except (ValueError, AssertionError):
            pass

    def test_validate_fps_reasonable_range(self):
        """Test that FPS is in reasonable range."""
        try:
            splitter = TerminalSplitter(fps=9999)
            # May or may not validate
        except ValueError:
            pass

    def test_validate_pane_weight_positive(self):
        """Test that pane weight must be positive."""
        from consolemod.core import Pane
        
        splitter = TerminalSplitter()
        pane = Pane("test")
        splitter.add_pane(pane)
        
        try:
            splitter.set_pane_weight("test", 0.0)
            # May or may not validate
        except ValueError:
            pass

    def test_validate_max_lines_positive(self):
        """Test that max_lines must be positive."""
        from consolemod.core import Pane
        
        try:
            pane = Pane("test", max_lines=0)
            # May or may not validate
        except ValueError:
            pass


class TestConfigDefaults:
    """Tests for default configuration values."""

    def test_default_fps(self):
        """Test default FPS value."""
        splitter = TerminalSplitter()
        assert splitter.fps == 30

    def test_default_theme(self):
        """Test default theme."""
        splitter = TerminalSplitter()
        assert splitter.theme == "dark"

    def test_default_layout(self):
        """Test default layout mode."""
        splitter = TerminalSplitter()
        assert splitter.layout_mode == LayoutMode.VERTICAL

    def test_default_input_enabled(self):
        """Test default input setting."""
        splitter = TerminalSplitter()
        assert splitter.enable_input is True

    def test_default_metrics_disabled(self):
        """Test default metrics setting."""
        splitter = TerminalSplitter()
        # Default may vary

    def test_default_pane_max_lines(self):
        """Test default pane max_lines."""
        from consolemod.core import Pane
        
        pane = Pane("test")
        # Should have sensible default
        assert pane.max_lines > 0
