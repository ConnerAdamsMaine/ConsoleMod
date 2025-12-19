"""Integration tests for multi-component interactions."""

import asyncio
import pytest
from consolemod.core import TerminalSplitter, Pane, LayoutMode
from consolemod.logging import PaneLogger, LogLevel
from consolemod.ui import ProgressBar, Table
from consolemod.utils import CommandHistory, UndoRedoStack


class TestMultiPaneIntegration:
    """Tests for multi-pane interactions."""

    def test_multiple_panes_with_logging(self):
        """Test multiple panes with different loggers."""
        splitter = TerminalSplitter()
        
        pane1 = Pane("logs")
        pane2 = Pane("errors")
        pane3 = Pane("status")
        
        splitter.add_pane(pane1)
        splitter.add_pane(pane2)
        splitter.add_pane(pane3)
        
        logger1 = PaneLogger(pane1)
        logger2 = PaneLogger(pane2)
        
        logger1.info("Info message")
        logger2.error("Error message")
        pane3.write("Status: OK")
        
        assert len(splitter.get_panes()) == 3

    def test_focus_switching_between_panes(self):
        """Test switching focus between panes."""
        splitter = TerminalSplitter(enable_input=True)
        
        pane1 = Pane("pane1")
        pane2 = Pane("pane2")
        pane3 = Pane("pane3")
        
        splitter.add_pane(pane1)
        splitter.add_pane(pane2)
        splitter.add_pane(pane3)
        
        initial_focus = splitter.get_focused_pane()
        assert initial_focus is not None

    def test_layout_change_with_panes(self):
        """Test changing layout with populated panes."""
        splitter = TerminalSplitter(layout_mode=LayoutMode.VERTICAL)
        
        for i in range(3):
            pane = Pane(f"pane{i}")
            pane.write(f"Content {i}")
            splitter.add_pane(pane)
        
        splitter.set_layout_mode(LayoutMode.HORIZONTAL)
        assert splitter.layout_mode == LayoutMode.HORIZONTAL
        assert len(splitter.get_panes()) == 3

    def test_concurrent_pane_writes_with_logging(self):
        """Test concurrent writes from different loggers."""
        import threading
        
        pane = Pane("shared")
        logger1 = PaneLogger(pane)
        logger2 = PaneLogger(pane)
        
        def write_logs1():
            for i in range(10):
                logger1.info(f"Logger1 message {i}")
        
        def write_logs2():
            for i in range(10):
                logger2.error(f"Logger2 message {i}")
        
        t1 = threading.Thread(target=write_logs1)
        t2 = threading.Thread(target=write_logs2)
        
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        
        content = pane.get_visible_content(100)
        assert len(content) >= 20

    @pytest.mark.asyncio
    async def test_async_multi_pane_operations(self):
        """Test async operations across multiple panes."""
        splitter = TerminalSplitter()
        
        panes = []
        for i in range(3):
            pane = Pane(f"async_pane{i}")
            await splitter.aadd_pane(pane)
            panes.append(pane)
        
        # Write to all panes concurrently
        await asyncio.gather(
            panes[0].awrite("Message 1"),
            panes[1].awrite("Message 2"),
            panes[2].awrite("Message 3")
        )
        
        retrieved_panes = await splitter.aget_panes()
        assert len(retrieved_panes) == 3


class TestWidgetIntegration:
    """Tests for widget integration with panes."""

    def test_progress_bar_in_pane(self):
        """Test rendering progress bar in pane."""
        pane = Pane("progress")
        progress = ProgressBar(total=100, width=30)
        
        for i in range(100):
            progress.increment(1)
        
        rendered = progress.render()
        pane.write(rendered)
        
        content = pane.get_visible_content(5)
        assert len(content) > 0

    def test_table_in_pane(self):
        """Test rendering table in pane."""
        pane = Pane("table")
        table = Table(["Name", "Score", "Status"])
        
        table.add_row("Task1", "100", "Done")
        table.add_row("Task2", "85", "In Progress")
        table.add_row("Task3", "0", "Pending")
        
        rendered = table.render()
        pane.write(rendered)
        
        content = pane.get_visible_content(10)
        assert len(content) > 0

    def test_multiple_widgets_same_pane(self):
        """Test multiple widgets in same pane."""
        pane = Pane("widgets")
        
        progress = ProgressBar(total=50, width=20)
        progress.increment(25)
        
        table = Table(["Col1", "Col2"])
        table.add_row("A", "B")
        
        pane.write(progress.render())
        pane.write("---")
        pane.write(table.render())
        
        content = pane.get_visible_content(20)
        assert len(content) >= 3


class TestLoggingIntegration:
    """Tests for logging across components."""

    def test_logger_with_history(self):
        """Test logger with command history."""
        pane = Pane("log_history")
        logger = PaneLogger(pane)
        history = CommandHistory(max_size=50)
        
        commands = ["start", "process", "pause", "resume", "stop"]
        
        for cmd in commands:
            history.add(cmd)
            logger.info(f"Executed: {cmd}")
        
        content = pane.get_visible_content(10)
        assert len(content) >= len(commands)

    def test_logger_with_undo_redo(self):
        """Test logger with undo/redo stack."""
        pane = Pane("undo_redo_log")
        logger = PaneLogger(pane)
        stack = UndoRedoStack()
        
        states = ["State A", "State B", "State C"]
        
        for state in states:
            stack.push(state)
            logger.info(f"Pushed: {state}")
        
        # Undo
        undone = stack.undo()
        logger.warning(f"Undone: {undone}")
        
        # Redo
        redone = stack.redo()
        logger.info(f"Redone: {redone}")
        
        content = pane.get_visible_content(20)
        assert len(content) > 0

    def test_multi_logger_coordination(self):
        """Test multiple loggers with different panes."""
        pane_logs = Pane("app_logs")
        pane_errors = Pane("errors")
        pane_debug = Pane("debug")
        
        logger_main = PaneLogger(pane_logs)
        logger_error = PaneLogger(pane_errors)
        logger_debug = PaneLogger(pane_debug)
        
        logger_main.info("Application started")
        logger_debug.debug("Debug enabled")
        logger_error.error("Sample error")
        logger_main.info("Processing...")
        logger_debug.debug("Step 1 complete")
        logger_main.info("Done")
        
        assert len(pane_logs.get_visible_content(10)) > 0
        assert len(pane_errors.get_visible_content(10)) > 0
        assert len(pane_debug.get_visible_content(10)) > 0


class TestSplitterIntegration:
    """Tests for complex splitter scenarios."""

    def test_dynamic_pane_addition(self):
        """Test adding panes dynamically."""
        splitter = TerminalSplitter()
        
        # Start with no panes
        assert len(splitter.get_panes()) == 0
        
        # Add panes one by one
        for i in range(5):
            pane = Pane(f"dynamic_pane{i}")
            pane.write(f"Pane {i}")
            splitter.add_pane(pane)
            assert len(splitter.get_panes()) == i + 1

    def test_pane_removal_and_readd(self):
        """Test removing and re-adding panes."""
        splitter = TerminalSplitter()
        
        pane = Pane("removable")
        pane.write("Original content")
        splitter.add_pane(pane)
        
        retrieved = splitter.get_pane("removable")
        assert retrieved is not None

    def test_theme_application_to_all_panes(self):
        """Test applying theme to multiple panes."""
        splitter = TerminalSplitter(theme="dark")
        
        for i in range(3):
            pane = Pane(f"themed_pane{i}")
            pane.write(f"Content {i}")
            splitter.add_pane(pane)
        
        splitter.set_theme("light")
        panes = splitter.get_panes()
        assert len(panes) == 3

    @pytest.mark.asyncio
    async def test_async_pane_operations_sequence(self):
        """Test sequence of async pane operations."""
        splitter = TerminalSplitter()
        pane = Pane("async_test")
        await splitter.aadd_pane(pane)
        
        # Write multiple messages
        for i in range(5):
            await pane.awrite(f"Async message {i}")
        
        # Get content
        content = await pane.aget_visible_content(10)
        
        # Clear
        await pane.aclear()
        
        empty = await pane.aget_visible_content(10)
        assert len(empty) == 0


class TestPerformanceIntegration:
    """Tests for performance under integrated workloads."""

    def test_high_volume_logging(self):
        """Test handling high volume of log messages."""
        pane = Pane("high_volume", max_lines=1000)
        logger = PaneLogger(pane)
        
        for i in range(500):
            logger.info(f"Log message {i}")
        
        content = pane.get_visible_content(100)
        assert len(content) > 0

    def test_many_panes_high_volume(self):
        """Test many panes with high volume writes."""
        splitter = TerminalSplitter(enable_metrics=True)
        
        # Create 10 panes
        for i in range(10):
            pane = Pane(f"pane{i}", max_lines=100)
            splitter.add_pane(pane)
            
            # Write 50 lines to each
            for j in range(50):
                pane.write(f"Line {j}")
        
        panes = splitter.get_panes()
        assert len(panes) == 10

    @pytest.mark.asyncio
    async def test_concurrent_async_writes(self):
        """Test many concurrent async writes."""
        pane = Pane("concurrent", max_lines=1000)
        
        async def write_task(task_id, count):
            for i in range(count):
                await pane.awrite(f"Task {task_id} - Message {i}")
        
        # 5 concurrent tasks, 20 writes each
        await asyncio.gather(
            write_task(1, 20),
            write_task(2, 20),
            write_task(3, 20),
            write_task(4, 20),
            write_task(5, 20)
        )
        
        content = await pane.aget_visible_content(100)
        assert len(content) > 0
