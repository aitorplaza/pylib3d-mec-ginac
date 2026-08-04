'''
Python Interactive Console widget for PyQt5.
Provides a REPL with shared namespace for the code editor.
'''

import sys
import io
import traceback
import code
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont, QTextCursor, QColor, QTextCharFormat, QFontDatabase
from PyQt5.QtCore import Qt


class ConsoleLineEdit(QLineEdit):
    '''
    Custom QLineEdit with command history support via Up/Down arrow keys.
    '''
    def __init__(self, console, parent=None):
        super().__init__(parent)
        self._console = console

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self._console._history_up()
        elif event.key() == Qt.Key_Down:
            self._console._history_down()
        else:
            super().keyPressEvent(event)


class PythonConsoleWidget(QWidget):
    '''
    Interactive Python console (REPL) with shared namespace.
    The code editor executes into the same namespace dict.
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.namespace = {'__name__': '__main__', '__doc__': None}
        self.console = code.InteractiveConsole(self.namespace)
        self.history = []
        self.history_index = -1

        self._setup_ui()
        self._print_welcome()


    def _get_monospaced_font(self):
        '''Get a monospaced font, trying preferred families first.'''
        font = QFont()
        for family in ['Source Code Pro', 'Consolas', 'Courier New', 'Monospace']:
            if family in QFontDatabase().families():
                font.setFamily(family)
                break
        font.setPointSize(11)
        font.setFixedPitch(True)
        return font


    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        font = self._get_monospaced_font()

        # Output Area (read-only)
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setFont(font)
        self.output_area.setStyleSheet('''
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: none;
            }
        ''')
        layout.addWidget(self.output_area)

        # Input Area (prompt + line edit)
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(5, 3, 5, 3)
        input_layout.setSpacing(4)

        self.prompt_label = QLabel('>>> ')
        self.prompt_label.setFont(font)
        self.prompt_label.setStyleSheet('color: #569cd6; background-color: #252526; font-weight: bold;')

        self.input_line = ConsoleLineEdit(self)
        self.input_line.setFont(font)
        self.input_line.setStyleSheet('''
            QLineEdit {
                background-color: #252526;
                color: #d4d4d4;
                border: none;
            }
        ''')
        self.input_line.returnPressed.connect(self._execute_line)

        input_layout.addWidget(self.prompt_label)
        input_layout.addWidget(self.input_line)

        input_widget = QWidget()
        input_widget.setStyleSheet('background-color: #252526;')
        input_widget.setLayout(input_layout)

        layout.addWidget(input_widget)


    def _print_welcome(self):
        '''Print welcome message with version info.'''
        vtk_version = 'Unknown'
        try:
            import vtk
            vtk_version = vtk.vtkVersion.GetVTKVersion()
        except ImportError:
            pass

        py_version = f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'

        welcome_msg = (
            'lib3d-mec-ginac IDE\n'
            f'Python {py_version} | VTK {vtk_version}\n'
            'Type Python commands or press F5 to run the editor script\n'
        )
        self.append_text(welcome_msg, '#808080')


    def _execute_line(self):
        '''Execute a single line from the input field.'''
        command = self.input_line.text()
        self.input_line.clear()

        # Add to history
        if command.strip():
            self.history.append(command)
            self.history_index = len(self.history)

        # Display the command with prompt
        prompt = self.prompt_label.text()
        self.append_text(f'{prompt}{command}', '#d4d4d4')

        # Capture stdout/stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        redirected_stdout = io.StringIO()
        redirected_stderr = io.StringIO()
        sys.stdout = redirected_stdout
        sys.stderr = redirected_stderr

        try:
            more = self.console.push(command)
        except Exception:
            more = False
            traceback.print_exc(file=sys.stderr)
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        # Display captured output
        stdout_val = redirected_stdout.getvalue()
        if stdout_val:
            self.append_text(stdout_val, '#d4d4d4')

        stderr_val = redirected_stderr.getvalue()
        if stderr_val:
            self.append_text(stderr_val, '#f44747')

        # Update prompt for multiline input
        if more:
            self.prompt_label.setText('... ')
        else:
            self.prompt_label.setText('>>> ')


    def _history_up(self):
        '''Navigate to previous command in history.'''
        if self.history and self.history_index > 0:
            self.history_index -= 1
            self.input_line.setText(self.history[self.history_index])

    def _history_down(self):
        '''Navigate to next command in history.'''
        if self.history and self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.input_line.setText(self.history[self.history_index])
        elif self.history_index == len(self.history) - 1:
            self.history_index = len(self.history)
            self.input_line.clear()


    def append_text(self, text, color='#d4d4d4'):
        '''Append colored text to the output area.'''
        cursor = self.output_area.textCursor()
        cursor.movePosition(QTextCursor.End)

        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        cursor.setCharFormat(fmt)

        cursor.insertText(text)
        if not text.endswith('\n'):
            cursor.insertText('\n')

        self.output_area.setTextCursor(cursor)
        self.output_area.ensureCursorVisible()


    def execute_code(self, code_string):
        '''
        Execute a code string (from the editor) in the shared namespace.
        Captures stdout/stderr and displays results in the output area.
        '''
        self.append_text('--- Running script ---', '#808080')

        old_stdout = sys.stdout
        old_stderr = sys.stderr
        redirected_stdout = io.StringIO()
        redirected_stderr = io.StringIO()
        sys.stdout = redirected_stdout
        sys.stderr = redirected_stderr

        try:
            exec(code_string, self.namespace)
        except Exception:
            traceback.print_exc(file=sys.stderr)
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        stdout_val = redirected_stdout.getvalue()
        if stdout_val:
            self.append_text(stdout_val, '#d4d4d4')

        stderr_val = redirected_stderr.getvalue()
        if stderr_val:
            self.append_text(stderr_val, '#f44747')

        self.append_text('--- Script finished ---', '#808080')


    def get_namespace(self):
        '''Return the shared namespace dict.'''
        return self.namespace


    def reset_namespace(self):
        '''Clear and re-initialize the namespace.'''
        self.namespace.clear()
        self.namespace.update({'__name__': '__main__', '__doc__': None})
        self.console = code.InteractiveConsole(self.namespace)
        self.append_text('--- Namespace reset ---', '#808080')
