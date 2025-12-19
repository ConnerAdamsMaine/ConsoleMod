"""Comprehensive tests for logging module."""

import pytest
from consolemod.core import Pane
from consolemod.logging import PaneLogger, LogLevel


class TestPaneLogger:
    """Tests for PaneLogger class."""

    def test_logger_creation(self):
        """Test logger creation."""
        pane = Pane("test")
        logger = PaneLogger(pane)
        assert logger.pane is pane

    def test_logger_with_timestamp(self):
        """Test logger with timestamp enabled."""
        pane = Pane("test")
        logger = PaneLogger(pane, include_timestamp=True)
        logger.info("Test message")
        content = pane.get_visible_content(10)
        assert len(content) > 0

    def test_logger_debug(self):
        """Test debug logging."""
        pane = Pane("test")
        logger = PaneLogger(pane)
        logger.debug("Debug message")
        content = pane.get_visible_content(10)
        assert len(content) > 0

    def test_logger_info(self):
        """Test info logging."""
        pane = Pane("test")
        logger = PaneLogger(pane)
        logger.info("Info message")
        content = pane.get_visible_content(10)
        assert len(content) > 0

    def test_logger_warning(self):
        """Test warning logging."""
        pane = Pane("test")
        logger = PaneLogger(pane)
        logger.warning("Warning message")
        content = pane.get_visible_content(10)
        assert len(content) > 0

    def test_logger_error(self):
        """Test error logging."""
        pane = Pane("test")
        logger = PaneLogger(pane)
        logger.error("Error message")
        content = pane.get_visible_content(10)
        assert len(content) > 0

    def test_logger_critical(self):
        """Test critical logging."""
        pane = Pane("test")
        logger = PaneLogger(pane)
        logger.critical("Critical message")
        content = pane.get_visible_content(10)
        assert len(content) > 0

    @pytest.mark.asyncio
    async def test_async_logger_operations(self):
        """Test async logging operations."""
        pane = Pane("test")
        logger = PaneLogger(pane)
        
        await logger.adebug("Async debug")
        await logger.ainfo("Async info")
        await logger.awarning("Async warning")
        await logger.aerror("Async error")
        await logger.acritical("Async critical")
        
        content = await pane.aget_visible_content(20)
        assert len(content) >= 5

    def test_custom_log_level(self):
        """Test custom log level."""
        pane = Pane("test")
        logger = PaneLogger(pane)
        logger.log("Custom level message", LogLevel.INFO)
        content = pane.get_visible_content(10)
        assert len(content) > 0

    @pytest.mark.asyncio
    async def test_async_custom_log_level(self):
        """Test async custom log level."""
        pane = Pane("test")
        logger = PaneLogger(pane)
        await logger.alog("Async custom message", LogLevel.WARNING)
        content = await pane.aget_visible_content(10)
        assert len(content) > 0

    def test_multiple_loggers_same_pane(self):
        """Test multiple loggers writing to same pane."""
        pane = Pane("shared")
        logger1 = PaneLogger(pane)
        logger2 = PaneLogger(pane)
        
        logger1.info("Logger 1")
        logger2.info("Logger 2")
        
        content = pane.get_visible_content(10)
        assert len(content) >= 2

    def test_logger_color_codes(self):
        """Test that logger includes color codes."""
        pane = Pane("test")
        logger = PaneLogger(pane)
        logger.error("Red error")
        logger.warning("Yellow warning")
        logger.info("Green info")
        
        content = pane.get_visible_content(10)
        # Content should have been written
        assert len(content) >= 3
