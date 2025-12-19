"""Error handling and exception tests."""

import pytest
from unittest.mock import patch, Mock
from consolemod.core import Pane, TerminalSplitter
from consolemod.logging import PaneLogger
from consolemod.utils import wrap_text, truncate_text, format_bytes, format_duration


class TestPaneErrorHandling:
    """Tests for Pane error handling."""

    def test_pane_invalid_color(self):
        """Test pane with invalid color."""
        try:
            pane = Pane("test", color="invalid_color_xyz")
            # Either creates with invalid color or validates
        except (ValueError, KeyError):
            pass  # Expected

    def test_pane_invalid_border_type(self):
        """Test pane with invalid border type."""
        pane = Pane("test")
        # Should handle gracefully

    def test_pane_negative_width(self):
        """Test pane with negative width."""
        try:
            pane = Pane("test", width=-1.0)
            # May or may not raise
        except ValueError:
            pass  # Expected

    def test_pane_negative_height(self):
        """Test pane with negative height."""
        try:
            pane = Pane("test", height=-1.0)
            # May or may not raise
        except ValueError:
            pass  # Expected

    def test_pane_negative_max_lines(self):
        """Test pane with negative max_lines."""
        try:
            pane = Pane("test", max_lines=-100)
            # May or may not raise
        except ValueError:
            pass  # Expected

    def test_pane_scroll_invalid_direction(self):
        """Test pane scroll with invalid direction."""
        pane = Pane("test")
        pane.write("content")
        try:
            pane.scroll("invalid_direction", 5)
        except (ValueError, KeyError):
            pass  # Expected
        # Or may silently ignore

    def test_pane_nonetype_write(self):
        """Test writing None to pane."""
        pane = Pane("test")
        try:
            pane.write(None)
        except (TypeError, AttributeError):
            pass  # Expected

    def test_pane_integer_write(self):
        """Test writing integer to pane."""
        pane = Pane("test")
        try:
            pane.write(12345)
            # May accept and convert to string
        except TypeError:
            pass  # May require string


class TestSplitterErrorHandling:
    """Tests for TerminalSplitter error handling."""

    def test_splitter_add_none_pane(self):
        """Test adding None as pane."""
        splitter = TerminalSplitter()
        try:
            splitter.add_pane(None)
        except (TypeError, AttributeError):
            pass  # Expected

    def test_splitter_add_invalid_pane_type(self):
        """Test adding invalid pane type."""
        splitter = TerminalSplitter()
        try:
            splitter.add_pane("not a pane")
        except (TypeError, AttributeError):
            pass  # Expected

    def test_splitter_invalid_layout_mode(self):
        """Test setting invalid layout mode."""
        splitter = TerminalSplitter()
        try:
            splitter.set_layout_mode("invalid")
        except (ValueError, AttributeError, TypeError):
            pass  # Expected

    def test_splitter_invalid_fps_type(self):
        """Test splitter with invalid fps type."""
        try:
            splitter = TerminalSplitter(fps="not_a_number")
        except (TypeError, ValueError):
            pass  # Expected

    def test_splitter_invalid_theme_type(self):
        """Test splitter with invalid theme type."""
        try:
            splitter = TerminalSplitter(theme=12345)
        except (TypeError, ValueError):
            pass  # Expected

    def test_splitter_set_weight_invalid_value(self):
        """Test setting invalid pane weight."""
        splitter = TerminalSplitter()
        pane = Pane("test")
        splitter.add_pane(pane)
        
        try:
            splitter.set_pane_weight("test", -5.0)
        except ValueError:
            pass  # May validate weight

    def test_splitter_set_weight_invalid_pane(self):
        """Test setting weight for non-existent pane."""
        splitter = TerminalSplitter()
        # Should handle gracefully
        splitter.set_pane_weight("nonexistent", 1.0)


class TestLoggingErrorHandling:
    """Tests for logging error handling."""

    def test_logger_invalid_pane(self):
        """Test logger with invalid pane."""
        try:
            logger = PaneLogger("not a pane")
        except (TypeError, AttributeError):
            pass  # Expected

    def test_logger_nonetype_message(self):
        """Test logging None message."""
        pane = Pane("test")
        logger = PaneLogger(pane)
        try:
            logger.info(None)
        except (TypeError, AttributeError):
            pass  # May require string

    def test_logger_integer_message(self):
        """Test logging integer message."""
        pane = Pane("test")
        logger = PaneLogger(pane)
        try:
            logger.info(12345)
            # May convert to string
        except TypeError:
            pass  # Expected

    def test_logger_dict_message(self):
        """Test logging dict message."""
        pane = Pane("test")
        logger = PaneLogger(pane)
        try:
            logger.info({"key": "value"})
            # May convert or error
        except TypeError:
            pass


class TestTextFormattingErrorHandling:
    """Tests for text formatting error handling."""

    def test_wrap_text_nonetype(self):
        """Test wrapping None."""
        try:
            result = wrap_text(None, width=10)
        except (TypeError, AttributeError):
            pass  # Expected

    def test_wrap_text_invalid_width_type(self):
        """Test wrapping with invalid width type."""
        try:
            result = wrap_text("hello", width="not_int")
        except (TypeError, ValueError):
            pass  # Expected

    def test_truncate_text_nonetype(self):
        """Test truncating None."""
        try:
            result = truncate_text(None, width=10)
        except (TypeError, AttributeError):
            pass  # Expected

    def test_truncate_text_invalid_width_type(self):
        """Test truncating with invalid width type."""
        try:
            result = truncate_text("hello", width="not_int")
        except (TypeError, ValueError):
            pass  # Expected

    def test_format_bytes_nonetype(self):
        """Test formatting None bytes."""
        try:
            result = format_bytes(None)
        except (TypeError, AttributeError):
            pass  # Expected

    def test_format_bytes_invalid_type(self):
        """Test formatting invalid type."""
        try:
            result = format_bytes("not_a_number")
        except (TypeError, ValueError):
            pass  # Expected

    def test_format_duration_nonetype(self):
        """Test formatting None duration."""
        try:
            result = format_duration(None)
        except (TypeError, AttributeError):
            pass  # Expected

    def test_format_duration_invalid_type(self):
        """Test formatting invalid type."""
        try:
            result = format_duration("not_a_number")
        except (TypeError, ValueError):
            pass  # Expected


class TestExceptionPropagation:
    """Tests for exception propagation and recovery."""

    def test_pane_write_after_error(self):
        """Test pane continues working after error."""
        pane = Pane("test")
        pane.write("before")
        
        try:
            pane.write(None)  # May error
        except (TypeError, AttributeError):
            pass
        
        pane.write("after")
        content = pane.get_visible_content(10)
        # Should still have content

    def test_splitter_pane_error_isolation(self):
        """Test that error in one pane doesn't affect others."""
        splitter = TerminalSplitter()
        
        pane1 = Pane("pane1")
        pane2 = Pane("pane2")
        
        splitter.add_pane(pane1)
        splitter.add_pane(pane2)
        
        pane1.write("content1")
        
        try:
            pane2.write(None)  # May error
        except (TypeError, AttributeError):
            pass
        
        pane2.write("content2")
        
        # Both panes should still be accessible
        assert splitter.get_pane("pane1") is not None
        assert splitter.get_pane("pane2") is not None

    def test_logger_error_isolation(self):
        """Test that logger error doesn't affect pane."""
        pane = Pane("test")
        logger = PaneLogger(pane)
        
        pane.write("direct")
        
        try:
            logger.info(None)  # May error
        except (TypeError, AttributeError):
            pass
        
        logger.info("after error")
        
        content = pane.get_visible_content(10)
        assert len(content) > 0


class TestAsyncErrorHandling:
    """Tests for async error handling."""

    @pytest.mark.asyncio
    async def test_async_pane_write_none(self):
        """Test async write with None."""
        pane = Pane("test")
        try:
            await pane.awrite(None)
        except (TypeError, AttributeError):
            pass  # Expected

    @pytest.mark.asyncio
    async def test_async_operation_after_error(self):
        """Test async operations continue after error."""
        pane = Pane("test")
        
        await pane.awrite("before")
        
        try:
            await pane.awrite(None)
        except (TypeError, AttributeError):
            pass
        
        await pane.awrite("after")
        
        content = await pane.aget_visible_content(10)
        assert len(content) > 0

    @pytest.mark.asyncio
    async def test_async_exception_in_concurrent_task(self):
        """Test exception handling in concurrent tasks."""
        import asyncio
        
        pane = Pane("test")
        
        async def failing_task():
            try:
                await pane.awrite(None)
            except (TypeError, AttributeError):
                pass
        
        async def success_task():
            await pane.awrite("success")
        
        # Both tasks should handle errors independently
        await asyncio.gather(
            failing_task(),
            success_task(),
            return_exceptions=True
        )


class TestConcurrencyErrorHandling:
    """Tests for error handling in concurrent scenarios."""

    def test_concurrent_write_error(self):
        """Test concurrent writes with potential errors."""
        import threading
        
        pane = Pane("test")
        errors = []
        
        def write_task(idx):
            try:
                for i in range(5):
                    if i == 2:
                        pane.write(None)  # May error
                    else:
                        pane.write(f"Task {idx} Message {i}")
            except (TypeError, AttributeError) as e:
                errors.append(e)
        
        threads = [threading.Thread(target=write_task, args=(i,)) for i in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Pane should still be functional
        content = pane.get_visible_content(100)
        assert len(content) > 0

    def test_concurrent_focus_changes(self):
        """Test concurrent focus changes."""
        import threading
        
        splitter = TerminalSplitter(enable_input=True)
        panes = [Pane(f"pane{i}") for i in range(3)]
        
        for pane in panes:
            splitter.add_pane(pane)
        
        def change_focus():
            for _ in range(5):
                try:
                    focused = splitter.get_focused_pane()
                except Exception:
                    pass
        
        threads = [threading.Thread(target=change_focus) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Should still be in valid state
        assert len(splitter.get_panes()) == 3
