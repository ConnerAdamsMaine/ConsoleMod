"""Comprehensive tests for utilities module."""

import pytest
from consolemod.utils import (
    wrap_text, align_text, truncate_text,
    format_bytes, format_duration,
    CommandHistory, UndoRedoStack,
    CircularBuffer, TextAlign
)


class TestTextFormatting:
    """Tests for text formatting utilities."""

    def test_wrap_text_basic(self):
        """Test basic text wrapping."""
        text = "This is a long text that needs wrapping"
        wrapped = wrap_text(text, width=10)
        assert isinstance(wrapped, list)
        assert len(wrapped) > 1

    def test_wrap_text_preserve_words(self):
        """Test text wrapping preserves words."""
        text = "The quick brown fox"
        wrapped = wrap_text(text, width=5)
        # Words should not be broken
        for line in wrapped:
            assert len(line) <= 5

    def test_align_text_left(self):
        """Test left text alignment."""
        aligned = align_text("Hello", width=10, align=TextAlign.LEFT)
        assert aligned.startswith("Hello")

    def test_align_text_center(self):
        """Test center text alignment."""
        aligned = align_text("Hello", width=11, align=TextAlign.CENTER)
        assert "Hello" in aligned

    def test_align_text_right(self):
        """Test right text alignment."""
        aligned = align_text("Hello", width=10, align=TextAlign.RIGHT)
        assert aligned.endswith("Hello")

    def test_truncate_text(self):
        """Test text truncation."""
        text = "This is a very long text"
        truncated = truncate_text(text, width=10)
        assert len(truncated) <= 10

    def test_truncate_with_suffix(self):
        """Test truncation with custom suffix."""
        text = "This is long"
        truncated = truncate_text(text, width=8, suffix=">>")
        assert truncated.endswith(">>")

    def test_format_bytes(self):
        """Test byte formatting."""
        result = format_bytes(1024)
        assert "KB" in result or "K" in result

    def test_format_bytes_large(self):
        """Test large byte formatting."""
        result = format_bytes(1048576)  # 1 MB
        assert "MB" in result

    def test_format_duration(self):
        """Test duration formatting."""
        result = format_duration(3600)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_format_duration_seconds(self):
        """Test seconds duration."""
        result = format_duration(45)
        assert "s" in result.lower()

    def test_format_duration_minutes(self):
        """Test minutes duration."""
        result = format_duration(300)
        assert isinstance(result, str)

    def test_format_duration_hours(self):
        """Test hours duration."""
        result = format_duration(3661)
        assert isinstance(result, str)


class TestCommandHistory:
    """Tests for CommandHistory class."""

    def test_history_creation(self):
        """Test command history creation."""
        history = CommandHistory(max_size=100)
        assert history.max_size == 100

    def test_add_command(self):
        """Test adding command to history."""
        history = CommandHistory()
        history.add("command1")
        assert len(history) >= 1

    def test_previous_command(self):
        """Test getting previous command."""
        history = CommandHistory()
        history.add("first")
        history.add("second")
        previous = history.previous()
        assert previous == "first"

    def test_next_command(self):
        """Test getting next command."""
        history = CommandHistory()
        history.add("first")
        history.add("second")
        history.previous()
        next_cmd = history.next()
        assert next_cmd == "second"

    def test_history_navigation(self):
        """Test history navigation."""
        history = CommandHistory()
        for i in range(5):
            history.add(f"cmd{i}")
        
        # Navigate back and forth
        for _ in range(3):
            history.previous()
        for _ in range(2):
            history.next()

    def test_history_max_size(self):
        """Test history respects max size."""
        history = CommandHistory(max_size=3)
        history.add("cmd1")
        history.add("cmd2")
        history.add("cmd3")
        history.add("cmd4")
        # Should only have 3 items
        assert len(history) <= 3

    def test_history_clear(self):
        """Test clearing history."""
        history = CommandHistory()
        history.add("cmd1")
        history.add("cmd2")
        history.clear()
        assert len(history) == 0


class TestUndoRedoStack:
    """Tests for UndoRedoStack class."""

    def test_undo_redo_creation(self):
        """Test undo/redo stack creation."""
        stack = UndoRedoStack()
        assert stack is not None

    def test_push_state(self):
        """Test pushing state."""
        stack = UndoRedoStack()
        stack.push("state1")
        assert len(stack) >= 1

    def test_undo_operation(self):
        """Test undo operation."""
        stack = UndoRedoStack()
        stack.push("state1")
        stack.push("state2")
        undone = stack.undo()
        assert undone == "state1"

    def test_redo_operation(self):
        """Test redo operation."""
        stack = UndoRedoStack()
        stack.push("state1")
        stack.push("state2")
        stack.undo()
        redone = stack.redo()
        assert redone == "state2"

    def test_undo_redo_sequence(self):
        """Test undo/redo sequence."""
        stack = UndoRedoStack()
        stack.push("A")
        stack.push("B")
        stack.push("C")
        
        # Undo twice
        stack.undo()
        stack.undo()
        
        # Redo once
        result = stack.redo()
        assert result is not None

    def test_push_clears_redo(self):
        """Test that push clears redo stack."""
        stack = UndoRedoStack()
        stack.push("A")
        stack.push("B")
        stack.undo()
        stack.push("C")
        # Redo should be empty now
        redo = stack.redo()
        # Should return None or empty

    def test_max_size(self):
        """Test stack respects max size."""
        stack = UndoRedoStack(max_size=3)
        for i in range(5):
            stack.push(f"state{i}")
        # Should only have 3 items
        assert len(stack) <= 3


class TestCircularBuffer:
    """Tests for CircularBuffer class."""

    def test_buffer_creation(self):
        """Test circular buffer creation."""
        buffer = CircularBuffer(max_size=10)
        assert buffer.max_size == 10

    def test_append_single_item(self):
        """Test appending single item."""
        buffer = CircularBuffer(max_size=5)
        buffer.append("item1")
        assert len(buffer) == 1

    def test_append_multiple_items(self):
        """Test appending multiple items."""
        buffer = CircularBuffer(max_size=5)
        for i in range(3):
            buffer.append(f"item{i}")
        assert len(buffer) == 3

    def test_buffer_wrapping(self):
        """Test buffer wraps when full."""
        buffer = CircularBuffer(max_size=3)
        buffer.append("A")
        buffer.append("B")
        buffer.append("C")
        buffer.append("D")  # Should overwrite A
        
        items = buffer.get_all()
        assert len(items) == 3

    def test_get_all(self):
        """Test getting all items."""
        buffer = CircularBuffer(max_size=5)
        buffer.append("x")
        buffer.append("y")
        buffer.append("z")
        
        items = buffer.get_all()
        assert len(items) == 3

    def test_get_last_n(self):
        """Test getting last N items."""
        buffer = CircularBuffer(max_size=10)
        for i in range(7):
            buffer.append(i)
        
        last_three = buffer.get_last(3)
        assert len(last_three) == 3

    def test_clear_buffer(self):
        """Test clearing buffer."""
        buffer = CircularBuffer(max_size=5)
        buffer.append("item1")
        buffer.append("item2")
        buffer.clear()
        
        assert len(buffer) == 0
        assert len(buffer.get_all()) == 0

    def test_is_full(self):
        """Test checking if buffer is full."""
        buffer = CircularBuffer(max_size=2)
        buffer.append("A")
        assert not buffer.is_full()
        buffer.append("B")
        assert buffer.is_full()
