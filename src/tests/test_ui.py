"""Comprehensive tests for UI module."""

import pytest
from consolemod.ui import (
    ProgressBar, Spinner, Table, Button,
    InputField, SelectField, CheckboxField,
    Theme, Style
)


class TestProgressBar:
    """Tests for ProgressBar widget."""

    def test_progress_bar_creation(self):
        """Test progress bar creation."""
        pb = ProgressBar(total=100, width=30)
        assert pb.total == 100
        assert pb.width == 30

    def test_progress_bar_increment(self):
        """Test progress bar increment."""
        pb = ProgressBar(total=100, width=30)
        pb.increment(10)
        assert pb.current >= 10

    def test_progress_bar_render(self):
        """Test progress bar rendering."""
        pb = ProgressBar(total=100, width=30)
        pb.increment(50)
        render = pb.render()
        assert isinstance(render, str)
        assert len(render) > 0

    def test_progress_bar_completion(self):
        """Test progress bar completion."""
        pb = ProgressBar(total=100, width=30)
        for _ in range(100):
            pb.increment(1)
        # Bar should be complete


class TestSpinner:
    """Tests for Spinner widget."""

    def test_spinner_creation(self):
        """Test spinner creation."""
        spinner = Spinner("Loading")
        assert spinner.label == "Loading"

    def test_spinner_next_frame(self):
        """Test spinner frame animation."""
        spinner = Spinner("Loading")
        frame1 = spinner.next_frame()
        frame2 = spinner.next_frame()
        # Frames should be strings
        assert isinstance(frame1, str)
        assert isinstance(frame2, str)

    def test_spinner_reset(self):
        """Test spinner reset."""
        spinner = Spinner("Loading")
        spinner.next_frame()
        spinner.next_frame()
        spinner.reset()
        # Spinner reset successfully


class TestTable:
    """Tests for Table widget."""

    def test_table_creation(self):
        """Test table creation."""
        table = Table(["Name", "Age", "Status"])
        assert len(table.columns) == 3

    def test_table_add_row(self):
        """Test adding row to table."""
        table = Table(["Col1", "Col2"])
        table.add_row("Val1", "Val2")
        assert len(table.rows) == 1

    def test_table_add_multiple_rows(self):
        """Test adding multiple rows."""
        table = Table(["Name", "Score"])
        table.add_row("Alice", "95")
        table.add_row("Bob", "87")
        table.add_row("Charlie", "92")
        assert len(table.rows) == 3

    def test_table_render(self):
        """Test table rendering."""
        table = Table(["Name", "Status"])
        table.add_row("Task1", "Done")
        table.add_row("Task2", "Pending")
        render = table.render()
        assert isinstance(render, str)
        assert len(render) > 0

    def test_table_clear(self):
        """Test clearing table."""
        table = Table(["Col1", "Col2"])
        table.add_row("Val1", "Val2")
        table.clear()
        assert len(table.rows) == 0


class TestButton:
    """Tests for Button widget."""

    def test_button_creation(self):
        """Test button creation."""
        def callback():
            pass
        button = Button("Click Me", callback)
        assert button.label == "Click Me"

    def test_button_click(self):
        """Test button click."""
        clicked = []
        def callback():
            clicked.append(True)
        button = Button("Click", callback)
        button.click()
        assert len(clicked) == 1

    def test_button_render(self):
        """Test button rendering."""
        button = Button("Test Button", lambda: None)
        render = button.render()
        assert isinstance(render, str)


class TestInputField:
    """Tests for InputField widget."""

    def test_input_field_creation(self):
        """Test input field creation."""
        field = InputField(placeholder="Enter text")
        assert field.placeholder == "Enter text"

    def test_input_field_set_value(self):
        """Test setting input field value."""
        field = InputField()
        field.set_value("test input")
        assert field.value == "test input"

    def test_input_field_get_value(self):
        """Test getting input field value."""
        field = InputField()
        field.set_value("hello")
        assert field.get_value() == "hello"

    def test_input_field_clear(self):
        """Test clearing input field."""
        field = InputField()
        field.set_value("content")
        field.clear()
        assert field.value == ""

    def test_input_field_with_validator(self):
        """Test input field with validator."""
        def is_numeric(val):
            return val.isdigit()
        field = InputField(validator=is_numeric)
        assert field.validator is not None


class TestSelectField:
    """Tests for SelectField widget."""

    def test_select_field_creation(self):
        """Test select field creation."""
        options = ["Option 1", "Option 2", "Option 3"]
        field = SelectField(options)
        assert len(field.options) == 3

    def test_select_field_select_option(self):
        """Test selecting option."""
        options = ["A", "B", "C"]
        field = SelectField(options)
        field.select(1)
        assert field.selected_index == 1

    def test_select_field_get_selected(self):
        """Test getting selected option."""
        options = ["First", "Second", "Third"]
        field = SelectField(options)
        field.select(2)
        assert field.get_selected() == "Third"


class TestCheckboxField:
    """Tests for CheckboxField widget."""

    def test_checkbox_creation(self):
        """Test checkbox creation."""
        checkbox = CheckboxField("Accept terms")
        assert checkbox.label == "Accept terms"

    def test_checkbox_toggle(self):
        """Test checkbox toggle."""
        checkbox = CheckboxField("Test")
        initial = checkbox.is_checked
        checkbox.toggle()
        assert checkbox.is_checked != initial

    def test_checkbox_set_checked(self):
        """Test setting checkbox checked state."""
        checkbox = CheckboxField("Test")
        checkbox.set_checked(True)
        assert checkbox.is_checked is True
        checkbox.set_checked(False)
        assert checkbox.is_checked is False


class TestTheme:
    """Tests for Theme class."""

    def test_theme_creation(self):
        """Test theme creation."""
        theme = Theme(name="dark", primary="white", secondary="gray")
        assert theme.name == "dark"

    def test_builtin_dark_theme(self):
        """Test built-in dark theme."""
        theme = Theme.get_builtin("dark")
        assert theme is not None

    def test_builtin_light_theme(self):
        """Test built-in light theme."""
        theme = Theme.get_builtin("light")
        assert theme is not None

    def test_builtin_solarized_theme(self):
        """Test built-in solarized theme."""
        theme = Theme.get_builtin("solarized")
        assert theme is not None


class TestStyle:
    """Tests for Style class."""

    def test_style_creation(self):
        """Test style creation."""
        style = Style(color="red", bold=True)
        assert style.color == "red"
        assert style.bold is True

    def test_style_render(self):
        """Test style rendering."""
        style = Style(color="blue", italic=True)
        render = style.render()
        assert isinstance(render, str)

    def test_style_combination(self):
        """Test combining multiple style attributes."""
        style = Style(color="green", bold=True, underline=True)
        assert style.bold is True
        assert style.underline is True
