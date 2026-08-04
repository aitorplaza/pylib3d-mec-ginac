'''
Python Code Editor widget based on QScintilla.
Provides syntax highlighting, line numbers, and dark theme.
'''

import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolBar, QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QFont, QFontDatabase, QColor
from PyQt5.QtCore import pyqtSignal
from PyQt5.Qsci import QsciScintilla, QsciLexerPython


class PythonCodeEditor(QsciScintilla):
    '''
    A QScintilla-based Python code editor with syntax highlighting and a dark theme.
    '''
    def __init__(self, parent=None):
        super().__init__(parent)

        # Configure font
        font = QFont()
        for family in ['Source Code Pro', 'Consolas', 'Courier New', 'Monospace']:
            if family in QFontDatabase().families():
                font.setFamily(family)
                break
        font.setPointSize(11)
        font.setFixedPitch(True)
        self.setFont(font)
        self.setMarginsFont(font)

        # Configure lexer for Python syntax highlighting
        self.lexer = QsciLexerPython(self)
        self.lexer.setDefaultFont(font)

        # Dark theme colors
        bg_color = QColor('#1e1e1e')
        fg_color = QColor('#d4d4d4')
        self.lexer.setDefaultPaper(bg_color)
        self.lexer.setDefaultColor(fg_color)

        # Apply background to all lexer styles
        for i in range(128):
            self.lexer.setPaper(bg_color, i)

        # Syntax colors
        self.lexer.setColor(QColor('#d4d4d4'), QsciLexerPython.Default)
        self.lexer.setColor(QColor('#6a9955'), QsciLexerPython.Comment)
        self.lexer.setColor(QColor('#6a9955'), QsciLexerPython.CommentBlock)
        self.lexer.setColor(QColor('#b5cea8'), QsciLexerPython.Number)
        self.lexer.setColor(QColor('#ce9178'), QsciLexerPython.DoubleQuotedString)
        self.lexer.setColor(QColor('#ce9178'), QsciLexerPython.SingleQuotedString)
        self.lexer.setColor(QColor('#569cd6'), QsciLexerPython.Keyword)
        self.lexer.setColor(QColor('#dcdcaa'), QsciLexerPython.FunctionMethodName)
        self.lexer.setColor(QColor('#4ec9b0'), QsciLexerPython.ClassName)
        self.lexer.setColor(QColor('#dcdcaa'), QsciLexerPython.Decorator)

        self.setLexer(self.lexer)
        self.setPaper(bg_color)

        # Editor behavior
        self.setUtf8(True)
        self.setIndentationsUseTabs(False)
        self.setIndentationWidth(4)
        self.setTabWidth(4)
        self.setAutoIndent(True)

        # Cursor (caret) configuration
        self.setCaretForegroundColor(QColor('white'))
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor('#2a2d2e'))

        # Line numbers margin
        self.setMarginsBackgroundColor(QColor('#2a2a2a'))
        self.setMarginsForegroundColor(QColor('#858585'))
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setMarginWidth(0, '00000')

        # Brace matching
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # 80-column edge line (subtle)
        self.setEdgeMode(QsciScintilla.EdgeLine)
        self.setEdgeColumn(80)
        self.setEdgeColor(QColor('#404040'))



class CodeEditorPanel(QWidget):
    '''
    Widget containing a PythonCodeEditor and a toolbar for file operations and code execution.
    '''
    execute_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_file = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create toolbar
        self.toolbar = QToolBar('Editor Actions', self)
        layout.addWidget(self.toolbar)

        # Toolbar actions
        self.new_action = QAction('📄 New', self)
        self.new_action.setShortcut('Ctrl+N')
        self.new_action.triggered.connect(self.new_file)
        self.toolbar.addAction(self.new_action)

        self.open_action = QAction('📂 Open', self)
        self.open_action.setShortcut('Ctrl+O')
        self.open_action.triggered.connect(self.open_file)
        self.toolbar.addAction(self.open_action)

        self.save_action = QAction('💾 Save', self)
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.triggered.connect(self.save_file)
        self.toolbar.addAction(self.save_action)

        self.toolbar.addSeparator()

        self.run_action = QAction('▶ Run', self)
        self.run_action.setShortcut('F5')
        self.run_action.triggered.connect(self.run_code)
        self.toolbar.addAction(self.run_action)

        # Code editor
        self.editor = PythonCodeEditor(self)
        layout.addWidget(self.editor)


    def new_file(self):
        '''Clear the editor to start a new file.'''
        self.editor.clear()
        self.current_file = None


    def open_file(self):
        '''Open a .py file from the filesystem.'''
        filepath, _ = QFileDialog.getOpenFileName(
            self, 'Open Python File', '', 'Python Files (*.py);;All Files (*)'
        )
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.editor.setText(content)
                self.current_file = filepath
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Could not open file:\n{e}')


    def save_file(self):
        '''Save current content to a file.'''
        if not self.current_file:
            filepath, _ = QFileDialog.getSaveFileName(
                self, 'Save Python File', '', 'Python Files (*.py);;All Files (*)'
            )
            if not filepath:
                return
            self.current_file = filepath

        try:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(self.editor.text())
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Could not save file:\n{e}')


    def run_code(self):
        '''Emit the execute signal with the current editor text.'''
        code = self.editor.text()
        self.execute_requested.emit(code)
