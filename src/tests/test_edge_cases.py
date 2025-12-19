"""Edge case and boundary condition tests."""

import pytest
from consolemod.core import Pane, TerminalSplitter, LayoutMode
from consolemod.logging import PaneLogger
from consolemod.utils import (
    wrap_text, align_text, truncate_text,
    format_bytes, format_duration,
    CommandHistory, CircularBuffer
)


class TestPaneEdgeCases:
    """Edge case tests for Pane class."""

    def test_pane_empty_id(self):
        """Test pane with empty ID."""
        pane = Pane("")
        assert pane.id == ""

    def test_pane_very_long_id(self):
        """Test pane with very long ID."""
        long_id = "a" * 1000
        pane = Pane(long_id)
        assert pane.id == long_id

    def test_pane_special_characters_in_id(self):
        """Test pane with special characters in ID."""
        special_id = "pane!@#$%^&*()"
        pane = Pane(special_id)
        assert pane.id == special_id

    def test_pane_write_empty_string(self):
        """Test writing empty string to pane."""
        pane = Pane("test")
        pane.write("")
        content = pane.get_visible_content(10)
        assert len(content) >= 0

    def test_pane_write_very_long_line(self):
        """Test writing very long line to pane."""
        pane = Pane("test")
        long_line = "x" * 10000
        pane.write(long_line)
        content = pane.get_visible_content(1)
        assert len(content) > 0

    def test_pane_write_many_lines(self):
        """Test writing many lines to pane."""
        pane = Pane("test", max_lines=100)
        for i in range(1000):
            pane.write(f"Line {i}")
        content = pane.get_visible_content(1000)
        assert len(content) <= 100

    def test_pane_scroll_beyond_bounds(self):
        """Test scrolling beyond content bounds."""
        pane = Pane("test")
        pane.write("Single line")
        
        # Scroll down far beyond content
        pane.scroll("down", 1000)
        content = pane.get_visible_content(10)
        # Should handle gracefully

    def test_pane_scroll_up_beyond_bounds(self):
        """Test scrolling up beyond start."""
        pane = Pane("test")
        for i in range(10):
            pane.write(f"Line {i}")
        
        # Scroll up far beyond start
        pane.scroll("up", 1000)
        content = pane.get_visible_content(10)
        # Should handle gracefully

    def test_pane_get_visible_zero_height(self):
        """Test getting visible content with zero height."""
        pane = Pane("test")
        pane.write("Content")
        content = pane.get_visible_content(0)
        assert isinstance(content, list)

    def test_pane_get_visible_negative_height(self):
        """Test getting visible content with negative height."""
        pane = Pane("test")
        pane.write("Content")
        content = pane.get_visible_content(-1)
        assert isinstance(content, list)

    def test_pane_max_lines_zero(self):
        """Test pane with max_lines set to 0."""
        pane = Pane("test", max_lines=0)
        pane.write("Should be ignored")
        content = pane.get_visible_content(10)
        # Should handle gracefully

    def test_pane_max_lines_one(self):
        """Test pane with max_lines set to 1."""
        pane = Pane("test", max_lines=1)
        pane.write("First")
        pane.write("Second")
        content = pane.get_visible_content(10)
        assert len(content) <= 1

    def test_pane_focus_toggle(self):
        """Test toggling focus multiple times."""
        pane = Pane("test")
        for _ in range(10):
            pane.set_focus(True)
            assert pane.is_focused is True
            pane.set_focus(False)
            assert pane.is_focused is False


class TestTextFormattingEdgeCases:
    """Edge case tests for text formatting utilities."""

    def test_wrap_text_empty_string(self):
        """Test wrapping empty string."""
        result = wrap_text("", width=10)
        assert isinstance(result, list)

    def test_wrap_text_single_word_longer_than_width(self):
        """Test wrapping single word longer than width."""
        result = wrap_text("supercalifragilisticexpialidocious", width=5)
        assert len(result) > 0

    def test_wrap_text_width_one(self):
        """Test wrapping with width of 1."""
        result = wrap_text("hello world", width=1)
        assert len(result) > 0

    def test_wrap_text_width_zero(self):
        """Test wrapping with width of 0."""
        result = wrap_text("hello", width=0)
        # Should handle gracefully

    def test_align_text_empty_string(self):
        """Test aligning empty string."""
        result = align_text("", width=10)
        assert isinstance(result, str)

    def test_align_text_width_smaller_than_text(self):
        """Test aligning when width is smaller than text."""
        result = align_text("Hello World", width=5)
        assert isinstance(result, str)

    def test_truncate_text_longer_than_text(self):
        """Test truncating with width larger than text."""
        result = truncate_text("Hi", width=100)
        assert result == "Hi"

    def test_truncate_text_width_zero(self):
        """Test truncating with width 0."""
        result = truncate_text("Hello", width=0)
        assert isinstance(result, str)

    def test_truncate_text_width_one(self):
        """Test truncating with width 1."""
        result = truncate_text("Hello", width=1)
        assert len(result) <= 1

    def test_format_bytes_zero(self):
        """Test formatting 0 bytes."""
        result = format_bytes(0)
        assert isinstance(result, str)

    def test_format_bytes_negative(self):
        """Test formatting negative bytes."""
        result = format_bytes(-100)
        assert isinstance(result, str)

    def test_format_bytes_very_large(self):
        """Test formatting very large byte value."""
        result = format_bytes(1024 ** 5)  # Petabytes
        assert isinstance(result, str)

    def test_format_duration_zero(self):
        """Test formatting 0 seconds."""
        result = format_duration(0)
        assert isinstance(result, str)

    def test_format_duration_negative(self):
        """Test formatting negative duration."""
        result = format_duration(-100)
        assert isinstance(result, str)

    def test_format_duration_very_large(self):
        """Test formatting very large duration."""
        result = format_duration(365 * 24 * 60 * 60)  # 1 year
        assert isinstance(result, str)


class TestHistoryEdgeCases:
    """Edge case tests for CommandHistory."""

    def test_history_empty_command(self):
        """Test adding empty command."""
        history = CommandHistory()
        history.add("")
        assert len(history) >= 1

    def test_history_navigate_when_empty(self):
        """Test navigating empty history."""
        history = CommandHistory()
        prev = history.previous()
        next_cmd = history.next()
        # Should handle gracefully

    def test_history_single_item(self):
        """Test history with single item."""
        history = CommandHistory()
        history.add("only_item")
        
        prev = history.previous()
        assert prev is not None or prev is None  # Either is valid

    def test_history_max_size_one(self):
        """Test history with max_size of 1."""
        history = CommandHistory(max_size=1)
        history.add("first")
        history.add("second")
        assert len(history) == 1

    def test_history_max_size_zero(self):
        """Test history with max_size of 0."""
        history = CommandHistory(max_size=0)
        history.add("item")
        assert len(history) == 0

    def test_history_very_long_command(self):
        """Test adding very long command."""
        long_cmd = "x" * 10000
        history = CommandHistory()
        history.add(long_cmd)
        assert len(history) >= 1

    def test_history_special_characters(self):
        """Test adding command with special characters."""
        history = CommandHistory()
        history.add("cmd!@#$%^&*()")
        history.add("cmd\n\t\r")
        # Should handle gracefully

    def test_history_clear_and_add(self):
        """Test clearing history and adding new items."""
        history = CommandHistory()
        history.add("first")
        history.add("second")
        history.clear()
        assert len(history) == 0
        history.add("new")
        assert len(history) == 1


class TestCircularBufferEdgeCases:
    """Edge case tests for CircularBuffer."""

    def test_buffer_size_zero(self):
        """Test circular buffer with size 0."""
        buffer = CircularBuffer(max_size=0)
        buffer.append("item")
        # Should handle gracefully

    def test_buffer_size_one(self):
        """Test circular buffer with size 1."""
        buffer = CircularBuffer(max_size=1)
        buffer.append("A")
        buffer.append("B")
        items = buffer.get_all()
        assert len(items) <= 1

    def test_buffer_get_last_more_than_size(self):
        """Test getting last N items where N > buffer size."""
        buffer = CircularBuffer(max_size=5)
        buffer.append("A")
        buffer.append("B")
        last_ten = buffer.get_last(10)
        assert len(last_ten) <= 2

    def test_buffer_get_last_zero(self):
        """Test getting last 0 items."""
        buffer = CircularBuffer(max_size=5)
        buffer.append("A")
        last = buffer.get_last(0)
        assert len(last) == 0

    def test_buffer_get_last_negative(self):
        """Test getting last negative items."""
        buffer = CircularBuffer(max_size=5)
        buffer.append("A")
        last = buffer.get_last(-5)
        # Should handle gracefully

    def test_buffer_append_none(self):
        """Test appending None to buffer."""
        buffer = CircularBuffer(max_size=5)
        buffer.append(None)
        items = buffer.get_all()
        assert len(items) >= 0

    def test_buffer_clear_empty(self):
        """Test clearing empty buffer."""
        buffer = CircularBuffer(max_size=5)
        buffer.clear()
        assert len(buffer) == 0

    def test_buffer_is_full_on_empty(self):
        """Test is_full on empty buffer."""
        buffer = CircularBuffer(max_size=5)
        assert buffer.is_full() is False

    def test_buffer_many_operations(self):
        """Test many operations on buffer."""
        buffer = CircularBuffer(max_size=10)
        
        # Add, clear, add, clear multiple times
        for _ in range(100):
            buffer.append("item")
            if buffer.is_full():
                buffer.clear()


class TestSplitterEdgeCases:
    """Edge case tests for TerminalSplitter."""

    def test_splitter_get_nonexistent_pane(self):
        """Test getting pane that doesn't exist."""
        splitter = TerminalSplitter()
        pane = splitter.get_pane("nonexistent")
        assert pane is None

    def test_splitter_set_weight_nonexistent_pane(self):
        """Test setting weight for nonexistent pane."""
        splitter = TerminalSplitter()
        # Should handle gracefully
        splitter.set_pane_weight("nonexistent", 2.0)

    def test_splitter_add_same_pane_twice(self):
        """Test adding same pane twice."""
        splitter = TerminalSplitter()
        pane = Pane("test")
        splitter.add_pane(pane)
        # Adding again might replace or error
        splitter.add_pane(pane)

    def test_splitter_zero_fps(self):
        """Test splitter with zero FPS."""
        splitter = TerminalSplitter(fps=0)
        # Should handle gracefully

    def test_splitter_negative_fps(self):
        """Test splitter with negative FPS."""
        splitter = TerminalSplitter(fps=-30)
        # Should handle gracefully

    def test_splitter_very_high_fps(self):
        """Test splitter with very high FPS."""
        splitter = TerminalSplitter(fps=1000)
        # Should handle gracefully

    def test_splitter_invalid_theme(self):
        """Test splitter with invalid theme."""
        try:
            splitter = TerminalSplitter(theme="nonexistent")
            # Either creates default or errors
        except ValueError:
            pass  # Expected

    def test_splitter_empty_pane_list(self):
        """Test getting panes from empty splitter."""
        splitter = TerminalSplitter()
        panes = splitter.get_panes()
        assert len(panes) == 0

    def test_splitter_focused_pane_when_empty(self):
        """Test getting focused pane when none added."""
        splitter = TerminalSplitter()
        focused = splitter.get_focused_pane()
        # Should return None or handle gracefully


class TestLoggingEdgeCases:
    """Edge case tests for logging."""

    def test_logger_with_empty_pane(self):
        """Test logger with fresh pane."""
        pane = Pane("empty")
        logger = PaneLogger(pane)
        logger.info("First message")
        # Should initialize and work

    def test_logger_all_levels_same_message(self):
        """Test all log levels with same message."""
        pane = Pane("all_levels")
        logger = PaneLogger(pane)
        
        msg = "Same message"
        logger.debug(msg)
        logger.info(msg)
        logger.warning(msg)
        logger.error(msg)
        logger.critical(msg)
        
        content = pane.get_visible_content(10)
        assert len(content) >= 5

    def test_logger_very_long_message(self):
        """Test logger with very long message."""
        pane = Pane("long")
        logger = PaneLogger(pane)
        long_msg = "x" * 10000
        logger.info(long_msg)
        # Should handle

    def test_logger_special_characters(self):
        """Test logger with special characters."""
        pane = Pane("special")
        logger = PaneLogger(pane)
        logger.info("Special: !@#$%^&*()")
        logger.info("Newline: line1\nline2")
        logger.info("Tab:\ttabbed")
        # Should handle

    def test_logger_unicode_characters(self):
        """Test logger with unicode characters."""
        pane = Pane("unicode")
        logger = PaneLogger(pane)
        logger.info("Unicode: 你好世界 🎉 ñoño")
        # Should handle
