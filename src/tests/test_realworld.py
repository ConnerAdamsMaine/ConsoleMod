"""Real-world scenario tests."""

import asyncio
import threading
import time
import pytest
from consolemod.core import TerminalSplitter, Pane, LayoutMode
from consolemod.logging import PaneLogger, LogLevel
from consolemod.ui import ProgressBar, Table, Spinner
from consolemod.utils import CommandHistory, UndoRedoStack


class TestApplicationScenarios:
    """Tests for real-world application scenarios."""

    def test_file_transfer_application(self):
        """Test a file transfer application UI."""
        splitter = TerminalSplitter(fps=30, theme="dark")
        
        # Create panes for different sections
        log_pane = Pane("logs", color="green")
        status_pane = Pane("status", color="blue")
        progress_pane = Pane("progress", color="yellow")
        
        splitter.add_pane(log_pane)
        splitter.add_pane(status_pane)
        splitter.add_pane(progress_pane)
        
        # Create loggers
        log_logger = PaneLogger(log_pane)
        
        # Simulate file transfer
        log_logger.info("Starting file transfer...")
        status_pane.write("Status: Connecting...")
        
        # Simulate progress
        progress = ProgressBar(total=100, width=30)
        for i in range(0, 101, 10):
            progress.increment(10)
            progress_pane.write(progress.render())
            log_logger.info(f"Transferred {i}%")
        
        log_logger.info("Transfer complete!")
        status_pane.write("Status: Complete")
        
        assert len(splitter.get_panes()) == 3

    @pytest.mark.asyncio
    async def test_data_processing_dashboard(self):
        """Test a data processing dashboard."""
        splitter = TerminalSplitter()
        
        # Create dashboard panes
        metrics_pane = Pane("metrics")
        logs_pane = Pane("logs")
        table_pane = Pane("results")
        
        splitter.add_pane(metrics_pane)
        splitter.add_pane(logs_pane)
        splitter.add_pane(table_pane)
        
        logger = PaneLogger(logs_pane)
        
        # Simulate data processing
        logger.info("Starting data processing...")
        metrics_pane.write("Items processed: 0")
        
        table = Table(["ID", "Status", "Result"])
        
        for i in range(10):
            await asyncio.sleep(0.01)
            logger.info(f"Processing item {i}")
            table.add_row(str(i), "Complete", "Success")
            metrics_pane.write(f"Items processed: {i+1}")
        
        table_pane.write(table.render())
        logger.info("Processing complete!")
        
        assert len(splitter.get_panes()) == 3

    def test_server_monitoring_ui(self):
        """Test a server monitoring UI."""
        splitter = TerminalSplitter(enable_metrics=True)
        
        # Create monitoring panes
        servers_pane = Pane("servers")
        events_pane = Pane("events")
        alerts_pane = Pane("alerts")
        
        splitter.add_pane(servers_pane)
        splitter.add_pane(events_pane)
        splitter.add_pane(alerts_pane)
        
        event_logger = PaneLogger(events_pane)
        alert_logger = PaneLogger(alerts_pane)
        
        # Simulate server status
        server_table = Table(["Server", "CPU", "Memory", "Status"])
        server_table.add_row("server1", "45%", "2.3GB", "Healthy")
        server_table.add_row("server2", "78%", "3.8GB", "Warning")
        server_table.add_row("server3", "12%", "1.2GB", "Healthy")
        
        servers_pane.write(server_table.render())
        
        event_logger.info("Server 2 CPU > 75%")
        alert_logger.warning("Server 2 requires attention")
        
        assert len(splitter.get_panes()) == 3

    def test_log_analysis_tool(self):
        """Test a log analysis tool UI."""
        splitter = TerminalSplitter()
        
        raw_logs = Pane("raw_logs")
        analysis = Pane("analysis")
        errors = Pane("errors")
        
        splitter.add_pane(raw_logs)
        splitter.add_pane(analysis)
        splitter.add_pane(errors)
        
        log_logger = PaneLogger(raw_logs)
        error_logger = PaneLogger(errors)
        
        # Simulate log entries
        logs_data = [
            ("INFO", "Application started"),
            ("DEBUG", "Initializing modules"),
            ("INFO", "Module X loaded"),
            ("WARN", "Module Y slow"),
            ("ERROR", "Failed to connect to DB"),
            ("INFO", "Retrying connection"),
            ("INFO", "Connection established"),
        ]
        
        for level, msg in logs_data:
            if level == "ERROR":
                error_logger.error(msg)
            else:
                log_logger.info(f"{level}: {msg}")
        
        # Analysis summary
        analysis.write("Total logs: 7")
        analysis.write("Errors: 1")
        analysis.write("Warnings: 1")
        
        assert len(splitter.get_panes()) == 3


class TestCommandLineToolScenarios:
    """Tests for command-line tool scenarios."""

    def test_interactive_cli_tool(self):
        """Test an interactive CLI tool."""
        splitter = TerminalSplitter(enable_input=True)
        
        output = Pane("output")
        status = Pane("status")
        
        splitter.add_pane(output)
        splitter.add_pane(status)
        
        logger = PaneLogger(output)
        history = CommandHistory(max_size=100)
        
        # Simulate user interactions
        commands = [
            "connect",
            "query users",
            "delete user 123",
            "export data",
        ]
        
        for cmd in commands:
            history.add(cmd)
            logger.info(f"> {cmd}")
            logger.info("Command executed")
        
        status.write(f"Commands in history: {len(history)}")
        
        assert len(history) == len(commands)

    def test_task_runner_ui(self):
        """Test a task runner UI."""
        splitter = TerminalSplitter()
        
        tasks_pane = Pane("tasks")
        output_pane = Pane("output")
        
        splitter.add_pane(tasks_pane)
        splitter.add_pane(output_pane)
        
        logger = PaneLogger(output_pane)
        
        # Define tasks
        tasks = [
            {"name": "build", "duration": 5},
            {"name": "test", "duration": 3},
            {"name": "deploy", "duration": 2},
        ]
        
        # Display tasks
        task_table = Table(["Task", "Duration", "Status"])
        for task in tasks:
            task_table.add_row(task["name"], f"{task['duration']}s", "Pending")
        
        tasks_pane.write(task_table.render())
        
        # Simulate execution
        for task in tasks:
            logger.info(f"Running {task['name']}...")
            logger.info(f"{task['name']} completed")
        
        assert len(splitter.get_panes()) == 2


class TestConcurrentWorkflowScenarios:
    """Tests for concurrent workflow scenarios."""

    @pytest.mark.asyncio
    async def test_parallel_download_ui(self):
        """Test parallel download UI."""
        splitter = TerminalSplitter()
        
        progress_pane = Pane("progress")
        log_pane = Pane("logs")
        
        splitter.add_pane(progress_pane)
        splitter.add_pane(log_pane)
        
        logger = PaneLogger(log_pane)
        
        async def download_file(file_id, size):
            progress = ProgressBar(total=size, width=20)
            logger.info(f"Starting download {file_id}")
            
            for i in range(0, size + 1, 10):
                progress.increment(10)
                await asyncio.sleep(0.01)
            
            logger.info(f"Completed download {file_id}")
        
        # Download 3 files concurrently
        await asyncio.gather(
            download_file("file1", 100),
            download_file("file2", 100),
            download_file("file3", 100)
        )
        
        assert len(splitter.get_panes()) == 2

    def test_multi_worker_processing(self):
        """Test multi-worker processing scenario."""
        splitter = TerminalSplitter()
        
        status = Pane("status")
        results = Pane("results")
        
        splitter.add_pane(status)
        splitter.add_pane(results)
        
        logger = PaneLogger(results)
        
        processed = []
        lock = threading.Lock()
        
        def worker_task(worker_id, items):
            for item in items:
                logger.info(f"Worker {worker_id} processing {item}")
                with lock:
                    processed.append(item)
        
        # Create worker threads
        items = list(range(20))
        threads = [
            threading.Thread(target=worker_task, args=(i, items[i::3]))
            for i in range(3)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        status.write(f"Processed {len(processed)} items")
        assert len(processed) == 20


class TestErrorHandlingInRealWorld:
    """Tests for error handling in real-world scenarios."""

    def test_graceful_error_recovery(self):
        """Test graceful error recovery."""
        splitter = TerminalSplitter()
        
        output = Pane("output")
        errors = Pane("errors")
        
        splitter.add_pane(output)
        splitter.add_pane(errors)
        
        logger = PaneLogger(output)
        error_logger = PaneLogger(errors)
        
        logger.info("Starting operation")
        
        # Simulate operation with errors
        operations = ["step1", "step2", "step3", "step4", "step5"]
        for op in operations:
            try:
                logger.info(f"Executing {op}")
                if op == "step3":
                    error_logger.error(f"Failed: {op}")
                    logger.warning(f"Retrying {op}")
                logger.info(f"Completed {op}")
            except Exception as e:
                error_logger.error(str(e))
        
        logger.info("Operation finished with errors handled")
        
        assert len(splitter.get_panes()) == 2

    def test_long_operation_timeout_handling(self):
        """Test timeout handling for long operations."""
        splitter = TerminalSplitter()
        
        status = Pane("status")
        logs = Pane("logs")
        
        splitter.add_pane(status)
        splitter.add_pane(logs)
        
        logger = PaneLogger(logs)
        
        logger.info("Starting long operation")
        status.write("Status: Running (timeout: 5s)")
        
        start = time.time()
        timeout = 5
        
        # Simulate long operation
        spinner = Spinner("Processing...")
        while time.time() - start < 2:  # Run for 2 seconds
            status.write(spinner.next_frame())
            time.sleep(0.1)
        
        if time.time() - start < timeout:
            logger.info("Operation completed within timeout")
        else:
            logger.error("Operation exceeded timeout")
        
        status.write("Status: Complete")


class TestStateManagementScenarios:
    """Tests for state management scenarios."""

    def test_editor_with_undo_redo(self):
        """Test editor application with undo/redo."""
        splitter = TerminalSplitter()
        
        editor = Pane("editor")
        history_pane = Pane("history")
        
        splitter.add_pane(editor)
        splitter.add_pane(history_pane)
        
        undo_stack = UndoRedoStack()
        states = []
        
        # Simulate editing
        edits = ["type 'hello'", "add ' world'", "delete word", "capitalize"]
        
        for edit in edits:
            state = f"Text: {len(edits)}"
            undo_stack.push(state)
            states.append(state)
            editor.write(edit)
            history_pane.write(f"Edit: {edit}")
        
        # Undo
        undone = undo_stack.undo()
        history_pane.write(f"Undone: {undone}")
        
        # Redo
        redone = undo_stack.redo()
        history_pane.write(f"Redone: {redone}")
        
        assert len(states) == len(edits)

    def test_command_palette_with_history(self):
        """Test command palette with command history."""
        splitter = TerminalSplitter(enable_input=True)
        
        palette = Pane("palette")
        results = Pane("results")
        
        splitter.add_pane(palette)
        splitter.add_pane(results)
        
        history = CommandHistory(max_size=100)
        logger = PaneLogger(results)
        
        # Simulate command entry
        commands = [
            "open file",
            "search text",
            "replace all",
            "go to line",
            "format document",
        ]
        
        for cmd in commands:
            history.add(cmd)
            logger.info(f"Executed: {cmd}")
        
        # Navigate history
        prev_cmd = history.previous()
        next_cmd = history.next()
        
        palette.write(f"History size: {len(history)}")
        
        assert len(history) == len(commands)


class TestPerformanceUnderRealWorldLoad:
    """Tests for performance under real-world load."""

    def test_large_dataset_display(self):
        """Test displaying large dataset."""
        splitter = TerminalSplitter()
        
        table_pane = Pane("table", max_lines=1000)
        splitter.add_pane(table_pane)
        
        # Create large table
        table = Table(["ID", "Name", "Email", "Status", "Score"])
        
        start = time.time()
        for i in range(1000):
            table.add_row(
                str(i),
                f"User {i}",
                f"user{i}@example.com",
                "Active" if i % 2 == 0 else "Inactive",
                str(100 - (i % 100))
            )
        elapsed_create = time.time() - start
        
        start = time.time()
        rendered = table.render()
        elapsed_render = time.time() - start
        
        table_pane.write(rendered)
        
        # Should handle large table
        assert elapsed_create < 5.0
        assert elapsed_render < 1.0

    @pytest.mark.asyncio
    async def test_high_frequency_updates(self):
        """Test high-frequency updates."""
        splitter = TerminalSplitter()
        
        metrics = Pane("metrics")
        splitter.add_pane(metrics)
        
        async def update_metrics():
            for i in range(1000):
                metrics.write(f"Update {i}: {time.time()}")
                if i % 100 == 0:
                    await asyncio.sleep(0)
        
        start = time.time()
        await update_metrics()
        elapsed = time.time() - start
        
        # Should handle 1000 updates quickly
        assert elapsed < 5.0

    def test_responsive_ui_under_load(self):
        """Test UI responsiveness under load."""
        splitter = TerminalSplitter(fps=30)
        
        main = Pane("main")
        sidebar = Pane("sidebar")
        
        splitter.add_pane(main)
        splitter.add_pane(sidebar)
        
        # Simulate background work
        def background_work():
            for i in range(1000):
                main.write(f"Message {i}")
        
        # Simulate user input while background work happens
        thread = threading.Thread(target=background_work)
        thread.start()
        
        # Simulate responsive UI updates
        for i in range(100):
            sidebar.write(f"Status: {i}%")
            time.sleep(0.01)  # UI update interval
        
        thread.join()
        
        # Both panes should have content
        assert len(main.get_visible_content(100)) > 0
        assert len(sidebar.get_visible_content(100)) > 0
