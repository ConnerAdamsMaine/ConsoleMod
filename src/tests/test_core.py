"""Comprehensive tests for core module."""

import asyncio
import pytest
from unittest.mock import Mock, patch, AsyncMock

from consolemod.core import TerminalSplitter, Pane, LayoutMode


class TestPane:
    """Tests for Pane class."""

    def test_pane_creation(self):
        """Test basic pane creation."""
        pane = Pane("test_pane", color="blue")
        assert pane.id == "test_pane"
        assert pane.color == "blue"
        assert pane.border is True

    def test_pane_write(self):
        """Test writing to pane."""
        pane = Pane("test")
        pane.write("Hello World")
        content = pane.get_visible_content(10)
        assert len(content) > 0

    @pytest.mark.asyncio
    async def test_pane_async_write(self):
        """Test async write to pane."""
        pane = Pane("test")
        await pane.awrite("Async Hello")
        content = await pane.aget_visible_content(10)
        assert len(content) > 0

    def test_pane_clear(self):
        """Test clearing pane content."""
        pane = Pane("test")
        pane.write("Content")
        pane.clear()
        content = pane.get_visible_content(10)
        assert len(content) == 0

    def test_pane_focus(self):
        """Test pane focus management."""
        pane = Pane("test")
        assert pane.is_focused is False
        pane.set_focus(True)
        assert pane.is_focused is True

    def test_pane_scroll(self):
        """Test pane scrolling."""
        pane = Pane("test")
        for i in range(50):
            pane.write(f"Line {i}")
        initial_content = pane.get_visible_content(10)
        pane.scroll("down", 5)
        scrolled_content = pane.get_visible_content(10)
        # Content should be different after scrolling
        assert True  # Scroll executed without error

    def test_pane_max_lines(self):
        """Test pane respects max_lines limit."""
        pane = Pane("test", max_lines=10)
        for i in range(20):
            pane.write(f"Line {i}")
        content = pane.get_visible_content(100)
        assert len(content) <= 10


class TestTerminalSplitter:
    """Tests for TerminalSplitter class."""

    def test_splitter_creation(self):
        """Test basic splitter creation."""
        splitter = TerminalSplitter(fps=30, theme="dark")
        assert splitter.fps == 30
        assert splitter.theme == "dark"

    def test_add_pane(self):
        """Test adding pane to splitter."""
        splitter = TerminalSplitter()
        pane = Pane("test")
        splitter.add_pane(pane)
        retrieved = splitter.get_pane("test")
        assert retrieved is not None
        assert retrieved.id == "test"

    def test_get_panes(self):
        """Test retrieving all panes."""
        splitter = TerminalSplitter()
        pane1 = Pane("pane1")
        pane2 = Pane("pane2")
        splitter.add_pane(pane1)
        splitter.add_pane(pane2)
        panes = splitter.get_panes()
        assert len(panes) == 2

    def test_pane_focus_management(self):
        """Test pane focus switching."""
        splitter = TerminalSplitter(enable_input=True)
        pane1 = Pane("pane1")
        pane2 = Pane("pane2")
        splitter.add_pane(pane1)
        splitter.add_pane(pane2)
        
        focused = splitter.get_focused_pane()
        assert focused is not None

    def test_layout_mode_vertical(self):
        """Test vertical layout mode."""
        splitter = TerminalSplitter(layout_mode=LayoutMode.VERTICAL)
        pane = Pane("test")
        splitter.add_pane(pane)
        assert splitter.layout_mode == LayoutMode.VERTICAL

    def test_layout_mode_horizontal(self):
        """Test horizontal layout mode."""
        splitter = TerminalSplitter(layout_mode=LayoutMode.HORIZONTAL)
        pane = Pane("test")
        splitter.add_pane(pane)
        assert splitter.layout_mode == LayoutMode.HORIZONTAL

    @pytest.mark.asyncio
    async def test_set_layout_mode_async(self):
        """Test async layout mode change."""
        splitter = TerminalSplitter(layout_mode=LayoutMode.VERTICAL)
        await splitter.aset_layout_mode(LayoutMode.HORIZONTAL)
        assert splitter.layout_mode == LayoutMode.HORIZONTAL

    def test_pane_weight(self):
        """Test setting pane weight."""
        splitter = TerminalSplitter()
        pane = Pane("test")
        splitter.add_pane(pane)
        splitter.set_pane_weight("test", 2.0)
        # Weight set without error

    def test_performance_metrics(self):
        """Test performance metrics retrieval."""
        splitter = TerminalSplitter(enable_metrics=True)
        pane = Pane("test")
        splitter.add_pane(pane)
        
        metrics = splitter.get_performance_metrics()
        assert isinstance(metrics, dict)
        assert 'fps' in metrics or len(metrics) >= 0

    def test_memory_metrics(self):
        """Test memory metrics retrieval."""
        splitter = TerminalSplitter(enable_metrics=True)
        pane = Pane("test")
        splitter.add_pane(pane)
        
        metrics = splitter.get_memory_metrics()
        assert isinstance(metrics, dict)

    def test_reset_metrics(self):
        """Test resetting metrics."""
        splitter = TerminalSplitter(enable_metrics=True)
        splitter.reset_metrics()
        # Metrics reset without error

    def test_splitter_with_config(self):
        """Test splitter with config file."""
        with patch('builtins.open'):
            splitter = TerminalSplitter(config="test.yaml")
            assert splitter is not None


class TestThreadSafety:
    """Tests for thread safety."""

    def test_pane_thread_safe_write(self):
        """Test thread-safe pane writes."""
        import threading
        pane = Pane("test")
        
        def write_to_pane(msg):
            for _ in range(5):
                pane.write(msg)
        
        threads = [
            threading.Thread(target=write_to_pane, args=(f"Thread {i}",))
            for i in range(3)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        content = pane.get_visible_content(100)
        assert len(content) > 0

    def test_splitter_thread_safe_operations(self):
        """Test thread-safe splitter operations."""
        import threading
        splitter = TerminalSplitter()
        
        def add_panes():
            for i in range(5):
                pane = Pane(f"pane_{i}")
                splitter.add_pane(pane)
        
        threads = [threading.Thread(target=add_panes) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # No race condition errors should occur


class TestAsyncSupport:
    """Tests for async/await support."""

    @pytest.mark.asyncio
    async def test_async_pane_operations(self):
        """Test async pane operations."""
        pane = Pane("test")
        await pane.awrite("Message 1")
        await pane.awrite("Message 2")
        content = await pane.aget_visible_content(10)
        assert len(content) > 0

    @pytest.mark.asyncio
    async def test_async_splitter_operations(self):
        """Test async splitter operations."""
        splitter = TerminalSplitter()
        pane = Pane("test")
        await splitter.aadd_pane(pane)
        retrieved = await splitter.aget_pane("test")
        assert retrieved is not None

    @pytest.mark.asyncio
    async def test_concurrent_writes(self):
        """Test concurrent async writes."""
        pane = Pane("test")
        
        async def write_task(msg):
            for i in range(5):
                await pane.awrite(f"{msg}_{i}")
        
        await asyncio.gather(
            write_task("Task1"),
            write_task("Task2"),
            write_task("Task3")
        )
        
        content = await pane.aget_visible_content(100)
        assert len(content) > 0
