"""Performance and benchmark tests."""

import asyncio
import time
import threading
import pytest
from consolemod.core import Pane, TerminalSplitter, LayoutMode
from consolemod.logging import PaneLogger
from consolemod.ui import ProgressBar, Table
from consolemod.utils import CircularBuffer, CommandHistory


class TestRenderingPerformance:
    """Tests for rendering performance."""

    def test_single_pane_write_throughput(self):
        """Test write throughput for single pane."""
        pane = Pane("test")
        
        start = time.time()
        for i in range(1000):
            pane.write(f"Message {i}")
        elapsed = time.time() - start
        
        assert elapsed > 0  # Should complete quickly
        throughput = 1000 / elapsed
        assert throughput > 100  # Should handle >100 writes/sec

    def test_multi_pane_write_throughput(self):
        """Test write throughput across multiple panes."""
        splitter = TerminalSplitter()
        panes = [Pane(f"pane{i}") for i in range(10)]
        
        for pane in panes:
            splitter.add_pane(pane)
        
        start = time.time()
        for i in range(1000):
            panes[i % 10].write(f"Message {i}")
        elapsed = time.time() - start
        
        throughput = 1000 / elapsed
        assert throughput > 50  # Multi-pane should still be fast

    def test_pane_content_retrieval_speed(self):
        """Test speed of retrieving visible content."""
        pane = Pane("test", max_lines=1000)
        
        # Fill pane
        for i in range(500):
            pane.write(f"Line {i}")
        
        start = time.time()
        for _ in range(100):
            content = pane.get_visible_content(50)
        elapsed = time.time() - start
        
        # Should be very fast
        avg_time = elapsed / 100
        assert avg_time < 0.01  # <10ms per retrieval


class TestMemoryUsage:
    """Tests for memory efficiency."""

    def test_pane_memory_bounded(self):
        """Test that pane memory is bounded by max_lines."""
        pane = Pane("test", max_lines=100)
        
        # Write 10x the max_lines
        for i in range(1000):
            pane.write(f"Line {i}")
        
        content = pane.get_visible_content(1000)
        assert len(content) <= 100

    def test_circular_buffer_memory_bounded(self):
        """Test circular buffer memory is bounded."""
        buffer = CircularBuffer(max_size=50)
        
        # Add 10x max_size
        for i in range(500):
            buffer.append(f"Item {i}")
        
        items = buffer.get_all()
        assert len(items) <= 50

    def test_history_memory_bounded(self):
        """Test history memory is bounded."""
        history = CommandHistory(max_size=100)
        
        # Add 10x max_size
        for i in range(1000):
            history.add(f"command_{i}")
        
        assert len(history) <= 100


class TestConcurrentPerformance:
    """Tests for concurrent operation performance."""

    def test_concurrent_write_performance(self):
        """Test performance of concurrent writes."""
        pane = Pane("test", max_lines=10000)
        
        start = time.time()
        
        def write_task(task_id, count):
            for i in range(count):
                pane.write(f"Task{task_id}-Msg{i}")
        
        # 10 concurrent writers, 100 messages each
        threads = [
            threading.Thread(target=write_task, args=(i, 100))
            for i in range(10)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        elapsed = time.time() - start
        total_writes = 1000
        throughput = total_writes / elapsed
        
        assert throughput > 50  # Should handle >50 concurrent writes/sec

    def test_concurrent_read_write_performance(self):
        """Test concurrent read/write performance."""
        pane = Pane("test", max_lines=1000)
        
        start = time.time()
        
        def write_task():
            for i in range(100):
                pane.write(f"Message {i}")
        
        def read_task():
            for _ in range(100):
                content = pane.get_visible_content(50)
        
        threads = [
            threading.Thread(target=write_task),
            threading.Thread(target=write_task),
            threading.Thread(target=read_task),
            threading.Thread(target=read_task),
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        elapsed = time.time() - start
        assert elapsed < 5  # Should complete quickly


class TestAsyncPerformance:
    """Tests for async operation performance."""

    @pytest.mark.asyncio
    async def test_async_write_throughput(self):
        """Test async write throughput."""
        pane = Pane("test")
        
        start = time.time()
        for i in range(500):
            await pane.awrite(f"Message {i}")
        elapsed = time.time() - start
        
        throughput = 500 / elapsed
        assert throughput > 50  # Should handle >50 async writes/sec

    @pytest.mark.asyncio
    async def test_concurrent_async_writes(self):
        """Test concurrent async writes."""
        pane = Pane("test", max_lines=5000)
        
        async def write_task(task_id):
            for i in range(100):
                await pane.awrite(f"Task{task_id}-Msg{i}")
        
        start = time.time()
        
        # 10 concurrent async tasks
        await asyncio.gather(*[write_task(i) for i in range(10)])
        
        elapsed = time.time() - start
        total_writes = 1000
        throughput = total_writes / elapsed
        
        assert throughput > 100  # Async should be faster


class TestLoggingPerformance:
    """Tests for logging performance."""

    def test_logging_throughput(self):
        """Test logging throughput."""
        pane = Pane("test", max_lines=5000)
        logger = PaneLogger(pane)
        
        start = time.time()
        for i in range(1000):
            logger.info(f"Log message {i}")
        elapsed = time.time() - start
        
        throughput = 1000 / elapsed
        assert throughput > 50  # Should log >50 messages/sec

    def test_logging_with_timestamp_overhead(self):
        """Test logging performance impact of timestamps."""
        pane_no_ts = Pane("no_ts", max_lines=5000)
        pane_ts = Pane("with_ts", max_lines=5000)
        
        logger_no_ts = PaneLogger(pane_no_ts, include_timestamp=False)
        logger_ts = PaneLogger(pane_ts, include_timestamp=True)
        
        # Test without timestamp
        start = time.time()
        for i in range(500):
            logger_no_ts.info(f"Message {i}")
        time_no_ts = time.time() - start
        
        # Test with timestamp
        start = time.time()
        for i in range(500):
            logger_ts.info(f"Message {i}")
        time_with_ts = time.time() - start
        
        # Timestamp shouldn't add too much overhead
        ratio = time_with_ts / time_no_ts
        assert ratio < 2.0  # Timestamp shouldn't be more than 2x slower


class TestWidgetPerformance:
    """Tests for widget performance."""

    def test_progress_bar_render_speed(self):
        """Test progress bar rendering speed."""
        progress = ProgressBar(total=1000, width=50)
        
        start = time.time()
        for i in range(100):
            progress.increment(10)
            rendered = progress.render()
        elapsed = time.time() - start
        
        # Should render quickly
        avg_time = elapsed / 100
        assert avg_time < 0.01  # <10ms per render

    def test_table_render_speed(self):
        """Test table rendering speed."""
        table = Table(["Col1", "Col2", "Col3", "Col4"])
        
        # Fill with rows
        for i in range(100):
            table.add_row(f"Row{i}", f"Data{i}", f"Value{i}", f"Status{i}")
        
        start = time.time()
        for _ in range(100):
            rendered = table.render()
        elapsed = time.time() - start
        
        # Should render quickly even with many rows
        avg_time = elapsed / 100
        assert avg_time < 0.05  # <50ms per render


class TestLayoutPerformance:
    """Tests for layout calculation performance."""

    def test_layout_calculation_many_panes(self):
        """Test layout calculation with many panes."""
        splitter = TerminalSplitter()
        
        # Add many panes
        for i in range(50):
            pane = Pane(f"pane{i}")
            splitter.add_pane(pane)
        
        start = time.time()
        
        # Change layout multiple times
        for _ in range(10):
            splitter.set_layout_mode(LayoutMode.HORIZONTAL)
            splitter.set_layout_mode(LayoutMode.VERTICAL)
        
        elapsed = time.time() - start
        
        # Layout changes should be fast
        assert elapsed < 1.0

    def test_weight_adjustment_performance(self):
        """Test pane weight adjustment performance."""
        splitter = TerminalSplitter()
        
        # Create panes
        panes = [Pane(f"pane{i}") for i in range(10)]
        for pane in panes:
            splitter.add_pane(pane)
        
        start = time.time()
        
        # Adjust weights many times
        for _ in range(100):
            for i in range(10):
                splitter.set_pane_weight(f"pane{i}", float(i + 1))
        
        elapsed = time.time() - start
        
        # Should handle many adjustments
        assert elapsed < 1.0


class TestScrollingPerformance:
    """Tests for scrolling performance."""

    def test_scroll_performance_large_content(self):
        """Test scrolling performance with large content."""
        pane = Pane("test", max_lines=1000)
        
        # Fill pane
        for i in range(1000):
            pane.write(f"Line {i}")
        
        start = time.time()
        
        # Scroll many times
        for _ in range(100):
            pane.scroll("down", 10)
            pane.scroll("up", 5)
        
        elapsed = time.time() - start
        
        # Should scroll quickly
        assert elapsed < 1.0

    def test_scroll_then_render_performance(self):
        """Test scroll followed by render."""
        pane = Pane("test", max_lines=500)
        
        for i in range(500):
            pane.write(f"Line {i}")
        
        start = time.time()
        
        for _ in range(50):
            pane.scroll("down", 5)
            content = pane.get_visible_content(20)
        
        elapsed = time.time() - start
        
        # Combined operation should be fast
        avg_time = elapsed / 50
        assert avg_time < 0.05  # <50ms per scroll+render


class TestDataStructurePerformance:
    """Tests for data structure performance."""

    def test_circular_buffer_append_performance(self):
        """Test circular buffer append performance."""
        buffer = CircularBuffer(max_size=1000)
        
        start = time.time()
        for i in range(10000):
            buffer.append(f"Item {i}")
        elapsed = time.time() - start
        
        throughput = 10000 / elapsed
        assert throughput > 1000  # Should append >1000/sec

    def test_command_history_navigation_performance(self):
        """Test history navigation performance."""
        history = CommandHistory(max_size=1000)
        
        # Fill history
        for i in range(500):
            history.add(f"command_{i}")
        
        start = time.time()
        
        # Navigate many times
        for _ in range(100):
            for _ in range(50):
                history.previous()
            for _ in range(50):
                history.next()
        
        elapsed = time.time() - start
        
        # Navigation should be very fast
        assert elapsed < 0.1
