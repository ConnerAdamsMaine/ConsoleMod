"""Stress tests for high-load scenarios."""

import asyncio
import threading
import time
import pytest
from consolemod.core import Pane, TerminalSplitter
from consolemod.logging import PaneLogger
from consolemod.utils import CircularBuffer, CommandHistory


class TestHighVolumeOperations:
    """Tests for high-volume operations."""

    def test_extreme_pane_writes(self):
        """Test extreme volume of pane writes."""
        pane = Pane("stress", max_lines=10000)
        
        start = time.time()
        for i in range(10000):
            pane.write(f"Message {i}")
        elapsed = time.time() - start
        
        throughput = 10000 / elapsed
        assert throughput > 100  # Should handle 100+ writes/sec
        
        content = pane.get_visible_content(100)
        assert len(content) > 0

    def test_extreme_buffer_operations(self):
        """Test extreme buffer operations."""
        buffer = CircularBuffer(max_size=10000)
        
        start = time.time()
        for i in range(100000):
            buffer.append(f"Item {i}")
        elapsed = time.time() - start
        
        throughput = 100000 / elapsed
        assert throughput > 1000
        
        items = buffer.get_all()
        assert len(items) <= 10000

    def test_extreme_history_operations(self):
        """Test extreme history operations."""
        history = CommandHistory(max_size=5000)
        
        start = time.time()
        for i in range(10000):
            history.add(f"command_{i}")
        elapsed = time.time() - start
        
        assert len(history) <= 5000

    def test_extreme_pane_scrolling(self):
        """Test extreme scrolling operations."""
        pane = Pane("scroll", max_lines=1000)
        
        for i in range(1000):
            pane.write(f"Line {i}")
        
        start = time.time()
        for _ in range(1000):
            pane.scroll("down", 1)
        elapsed = time.time() - start
        
        assert elapsed < 5.0


class TestManyPanesHighVolume:
    """Tests for many panes with high volume."""

    def test_100_panes_concurrent_writes(self):
        """Test 100 panes with concurrent writes."""
        splitter = TerminalSplitter()
        panes = []
        
        # Create 100 panes
        for i in range(100):
            pane = Pane(f"pane{i}", max_lines=100)
            splitter.add_pane(pane)
            panes.append(pane)
        
        start = time.time()
        
        # Write to all panes
        for i in range(100):
            for pane in panes:
                pane.write(f"Message {i}")
        
        elapsed = time.time() - start
        
        assert len(splitter.get_panes()) == 100
        assert elapsed < 10.0

    def test_many_panes_layout_changes(self):
        """Test layout changes with many panes."""
        from consolemod.core import LayoutMode
        
        splitter = TerminalSplitter()
        
        for i in range(50):
            pane = Pane(f"pane{i}")
            splitter.add_pane(pane)
        
        start = time.time()
        
        for _ in range(10):
            splitter.set_layout_mode(LayoutMode.HORIZONTAL)
            splitter.set_layout_mode(LayoutMode.VERTICAL)
        
        elapsed = time.time() - start
        
        assert elapsed < 2.0

    def test_many_loggers_concurrent_writes(self):
        """Test many loggers writing concurrently."""
        pane = Pane("shared", max_lines=10000)
        loggers = [PaneLogger(pane) for _ in range(10)]
        
        def log_task(logger_id, count):
            for i in range(count):
                loggers[logger_id].info(f"Logger {logger_id} - Message {i}")
        
        start = time.time()
        
        threads = [
            threading.Thread(target=log_task, args=(i, 100))
            for i in range(10)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        elapsed = time.time() - start
        content = pane.get_visible_content(100)
        assert len(content) > 0


class TestConcurrentStress:
    """Tests for concurrent stress scenarios."""

    def test_high_concurrency_pane_writes(self):
        """Test high concurrency pane writes."""
        pane = Pane("concurrent", max_lines=50000)
        
        def write_task(task_id, count):
            for i in range(count):
                pane.write(f"Task {task_id} - Message {i}")
        
        start = time.time()
        
        threads = [
            threading.Thread(target=write_task, args=(i, 100))
            for i in range(20)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        elapsed = time.time() - start
        content = pane.get_visible_content(1000)
        assert len(content) > 0
        assert elapsed < 10.0

    def test_high_concurrency_read_write(self):
        """Test high concurrency read/write mix."""
        pane = Pane("rw", max_lines=10000)
        
        def reader_task():
            for _ in range(100):
                pane.get_visible_content(50)
        
        def writer_task():
            for i in range(100):
                pane.write(f"Message {i}")
        
        start = time.time()
        
        threads = []
        for _ in range(5):
            threads.append(threading.Thread(target=reader_task))
        for _ in range(5):
            threads.append(threading.Thread(target=writer_task))
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        elapsed = time.time() - start
        assert elapsed < 5.0

    def test_concurrent_splitter_operations(self):
        """Test concurrent splitter operations."""
        splitter = TerminalSplitter()
        
        def pane_ops():
            for i in range(50):
                pane = Pane(f"temp_{threading.current_thread().ident}_{i}")
                splitter.add_pane(pane)
                pane.write("test")
        
        threads = [threading.Thread(target=pane_ops) for _ in range(3)]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        panes = splitter.get_panes()
        assert len(panes) > 0


class TestAsyncStress:
    """Tests for async stress scenarios."""

    @pytest.mark.asyncio
    async def test_high_volume_async_writes(self):
        """Test high volume async writes."""
        pane = Pane("async", max_lines=50000)
        
        async def write_task(msg_id, count):
            for i in range(count):
                await pane.awrite(f"Message {msg_id}-{i}")
        
        start = time.time()
        
        # 50 concurrent tasks, 50 messages each
        await asyncio.gather(*[
            write_task(i, 50) for i in range(50)
        ])
        
        elapsed = time.time() - start
        content = await pane.aget_visible_content(1000)
        assert len(content) > 0
        assert elapsed < 10.0

    @pytest.mark.asyncio
    async def test_concurrent_async_panes(self):
        """Test concurrent async pane operations."""
        panes = [Pane(f"pane{i}", max_lines=1000) for i in range(10)]
        
        async def pane_task(pane, count):
            for i in range(count):
                await pane.awrite(f"Message {i}")
        
        start = time.time()
        
        await asyncio.gather(*[
            pane_task(pane, 100) for pane in panes
        ])
        
        elapsed = time.time() - start
        assert elapsed < 5.0

    @pytest.mark.asyncio
    async def test_mixed_async_operations(self):
        """Test mixed async operations."""
        pane = Pane("mixed", max_lines=10000)
        logger = PaneLogger(pane)
        
        async def write_task():
            for i in range(100):
                await pane.awrite(f"Write {i}")
        
        async def log_task():
            for i in range(100):
                logger.info(f"Log {i}")
        
        async def read_task():
            for _ in range(100):
                await pane.aget_visible_content(50)
        
        start = time.time()
        
        await asyncio.gather(
            write_task(),
            write_task(),
            log_task(),
            read_task(),
            read_task()
        )
        
        elapsed = time.time() - start
        assert elapsed < 5.0


class TestMemoryStress:
    """Tests for memory stress scenarios."""

    def test_large_pane_content(self):
        """Test pane with very large content."""
        pane = Pane("large", max_lines=5000)
        
        large_msg = "x" * 1000  # 1KB message
        
        for i in range(5000):
            pane.write(large_msg)
        
        content = pane.get_visible_content(100)
        assert len(content) > 0

    def test_many_small_messages(self):
        """Test many small messages."""
        pane = Pane("many", max_lines=50000)
        
        for i in range(50000):
            pane.write(f"M{i}")
        
        content = pane.get_visible_content(1000)
        assert len(content) > 0

    def test_buffer_memory_efficiency(self):
        """Test buffer memory efficiency under stress."""
        buffer = CircularBuffer(max_size=5000)
        
        for i in range(100000):
            buffer.append(f"Item {i}")
        
        items = buffer.get_all()
        assert len(items) <= 5000


class TestLongRunningOperations:
    """Tests for long-running operations."""

    def test_sustained_write_throughput(self):
        """Test sustained write throughput over time."""
        pane = Pane("sustained", max_lines=20000)
        
        writes_per_second = []
        
        for second in range(5):
            start = time.time()
            for i in range(200):
                pane.write(f"Message {second}-{i}")
            elapsed = time.time() - start
            
            throughput = 200 / elapsed
            writes_per_second.append(throughput)
        
        # Should maintain throughput
        avg_throughput = sum(writes_per_second) / len(writes_per_second)
        assert avg_throughput > 50

    @pytest.mark.asyncio
    async def test_sustained_async_operations(self):
        """Test sustained async operations."""
        pane = Pane("sustained_async", max_lines=20000)
        
        async def sustained_writes():
            for i in range(1000):
                await pane.awrite(f"Message {i}")
                if i % 100 == 0:
                    await asyncio.sleep(0.01)
        
        start = time.time()
        await sustained_writes()
        elapsed = time.time() - start
        
        assert elapsed < 10.0

    def test_long_running_concurrent_stress(self):
        """Test long-running concurrent stress."""
        pane = Pane("long_stress", max_lines=50000)
        stop_event = threading.Event()
        
        write_count = [0]
        lock = threading.Lock()
        
        def write_task():
            while not stop_event.is_set():
                pane.write("Message")
                with lock:
                    write_count[0] += 1
        
        threads = [threading.Thread(target=write_task) for _ in range(5)]
        
        for t in threads:
            t.start()
        
        time.sleep(2)  # Run for 2 seconds
        stop_event.set()
        
        for t in threads:
            t.join()
        
        # Should have handled many writes
        assert write_count[0] > 1000


class TestResourceExhaustion:
    """Tests for resource exhaustion scenarios."""

    def test_many_panes_limit(self):
        """Test creating many panes."""
        splitter = TerminalSplitter()
        
        try:
            for i in range(1000):
                pane = Pane(f"pane{i}")
                splitter.add_pane(pane)
        except (MemoryError, RuntimeError):
            pass
        
        panes = splitter.get_panes()
        assert len(panes) > 0

    def test_large_message_handling(self):
        """Test handling very large messages."""
        pane = Pane("large_msg", max_lines=100)
        
        huge_msg = "x" * 1000000  # 1MB message
        
        try:
            pane.write(huge_msg)
            content = pane.get_visible_content(1)
            assert len(content) > 0
        except (MemoryError, RuntimeError):
            pass

    def test_many_history_items(self):
        """Test history with many items."""
        history = CommandHistory(max_size=100000)
        
        for i in range(100000):
            history.add(f"cmd_{i}")
        
        assert len(history) == 100000


class TestErrorRecoveryUnderStress:
    """Tests for error recovery under stress."""

    def test_recovery_after_bulk_errors(self):
        """Test recovery after many errors."""
        pane = Pane("error_recovery", max_lines=1000)
        
        for i in range(100):
            try:
                if i % 10 == 0:
                    pane.write(None)  # May error
                else:
                    pane.write(f"Message {i}")
            except (TypeError, AttributeError):
                pass
        
        # Should still be functional
        pane.write("Recovery test")
        content = pane.get_visible_content(10)
        assert len(content) > 0

    def test_concurrent_error_handling(self):
        """Test concurrent error handling."""
        pane = Pane("concurrent_errors", max_lines=5000)
        
        def task_with_errors(task_id):
            for i in range(100):
                try:
                    if i % 20 == 0:
                        pane.write(None)
                    else:
                        pane.write(f"Task {task_id} - {i}")
                except (TypeError, AttributeError):
                    pass
        
        threads = [
            threading.Thread(target=task_with_errors, args=(i,))
            for i in range(5)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        content = pane.get_visible_content(100)
        assert len(content) > 0
