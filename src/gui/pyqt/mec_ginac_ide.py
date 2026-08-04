'''
lib3d-mec-ginac IDE — MATLAB-style integrated development environment.

Standalone program that provides:
- Python code editor with syntax highlighting (left panel)
- 3D VTK visualizer for mechanical systems (right panel)
- Interactive Python console with shared namespace (bottom panel)

Usage:
    python mec_ginac_ide.py
    python -m src.gui.pyqt
'''

import sys
import os

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QMenuBar, QMenu,
    QAction, QStatusBar, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Add this directory to sys.path for standalone execution
_this_dir = os.path.dirname(os.path.abspath(__file__))
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)

from vtk_widget import VtkViewportWidget
from code_editor import CodeEditorPanel
from python_console import PythonConsoleWidget


class MecGinacIDE(QMainWindow):
    '''
    Main window of the lib3d-mec-ginac IDE.

    Layout:
        ┌────────────────┬───────────────────┐
        │  Code Editor   │  3D VTK Viewer    │
        │                │                   │
        ├────────────────┴───────────────────┤
        │  Interactive Python Console        │
        └────────────────────────────────────┘
    '''

    def __init__(self):
        super().__init__()
        self.setWindowTitle('lib3d-mec-ginac IDE')
        self.resize(1400, 900)

        # Apply dark theme to the entire application
        self._apply_dark_theme()

        # Create the three main widgets
        self.code_editor = CodeEditorPanel(self)
        self.vtk_viewer = VtkViewportWidget(self)
        self.console = PythonConsoleWidget(self)

        # Connect editor "Run" signal to console execution
        self.code_editor.execute_requested.connect(self.console.execute_code)

        # Setup layout with splitters
        self._setup_layout()

        # Setup menus
        self._setup_menus()

        # Setup status bar
        self._setup_status_bar()

        # Initialize the mechanical system in the shared namespace
        self._init_mec_system()


    def _apply_dark_theme(self):
        '''Apply a dark theme stylesheet to the entire application.'''
        self.setStyleSheet('''
            QMainWindow {
                background-color: #1e1e1e;
            }
            QMenuBar {
                background-color: #2d2d2d;
                color: #d4d4d4;
                border-bottom: 1px solid #404040;
            }
            QMenuBar::item:selected {
                background-color: #404040;
            }
            QMenu {
                background-color: #2d2d2d;
                color: #d4d4d4;
                border: 1px solid #404040;
            }
            QMenu::item:selected {
                background-color: #094771;
            }
            QMenu::separator {
                height: 1px;
                background: #404040;
            }
            QStatusBar {
                background-color: #007acc;
                color: white;
            }
            QSplitter::handle {
                background-color: #404040;
            }
            QSplitter::handle:horizontal {
                width: 3px;
            }
            QSplitter::handle:vertical {
                height: 3px;
            }
            QToolBar {
                background-color: #2d2d2d;
                border: none;
                spacing: 5px;
                padding: 2px;
            }
            QToolBar QToolButton {
                color: #d4d4d4;
                background-color: transparent;
                border: none;
                padding: 4px 8px;
            }
            QToolBar QToolButton:hover {
                background-color: #404040;
            }
        ''')


    def _setup_layout(self):
        '''Create the splitter-based layout with 3 panels.'''
        # Top splitter: editor (left) | vtk viewer (right)
        self.top_splitter = QSplitter(Qt.Horizontal)
        self.top_splitter.addWidget(self.code_editor)
        self.top_splitter.addWidget(self.vtk_viewer)
        self.top_splitter.setSizes([560, 840])  # 40% / 60%

        # Main splitter: top content (top) | console (bottom)
        self.main_splitter = QSplitter(Qt.Vertical)
        self.main_splitter.addWidget(self.top_splitter)
        self.main_splitter.addWidget(self.console)
        self.main_splitter.setSizes([585, 315])  # 65% / 35%

        self.setCentralWidget(self.main_splitter)


    def _setup_menus(self):
        '''Build the menu bar with File, Simulation, Scene, and Help menus.'''
        menu_bar = self.menuBar()

        # --- File menu ---
        file_menu = menu_bar.addMenu('&File')

        new_action = QAction('📄 New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.code_editor.new_file)
        file_menu.addAction(new_action)

        open_action = QAction('📂 Open...', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.code_editor.open_file)
        file_menu.addAction(open_action)

        save_action = QAction('💾 Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.code_editor.save_file)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # --- Edit menu ---
        edit_menu = menu_bar.addMenu('&Edit')

        run_action = QAction('▶ Run Script', self)
        run_action.setShortcut('F5')
        run_action.triggered.connect(self.code_editor.run_code)
        edit_menu.addAction(run_action)

        edit_menu.addSeparator()

        reset_ns_action = QAction('Reset Namespace', self)
        reset_ns_action.triggered.connect(self.console.reset_namespace)
        edit_menu.addAction(reset_ns_action)

        # --- Simulation menu ---
        self.simulation_menu = menu_bar.addMenu('&Simulation')
        # Placeholder — connected in _init_mec_system when system is available
        self.simulation_menu.addAction(QAction('(No system loaded)', self))

        # --- Scene menu ---
        self.scene_menu = menu_bar.addMenu('S&cene')
        self.scene_menu.addAction(QAction('(No scene loaded)', self))

        # --- Help menu ---
        help_menu = menu_bar.addMenu('&Help')

        about_action = QAction('About', self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)


    def _setup_status_bar(self):
        '''Configure the status bar.'''
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Ready')


    def _init_mec_system(self):
        '''
        Try to import lib3d_mec_ginac and set up the default system in the
        shared namespace. If the library is not available, the IDE still works
        as a generic Python editor + console.
        '''
        namespace = self.console.get_namespace()
        try:
            # Try importing the mechanical library into the shared namespace
            exec('from lib3d_mec_ginac import *', namespace)
            self.console.append_text(
                'lib3d-mec-ginac loaded successfully.\n', '#808080'
            )

            # Try to connect the default system's scene to the VTK viewer
            if 'get_default_system' in namespace:
                system = namespace['get_default_system']()
                if system and hasattr(system, 'get_scene'):
                    scene = system.get_scene()
                    self.vtk_viewer.set_scene(scene)
                    self.console.append_text(
                        'Default system scene connected to 3D viewer.\n', '#808080'
                    )
                    self._setup_simulation_menu(scene)
                    self._setup_scene_menu(scene)

        except ImportError:
            self.console.append_text(
                'Warning: lib3d_mec_ginac not found. Running as generic Python IDE.\n',
                '#f44747'
            )
        except Exception as e:
            self.console.append_text(
                f'Warning: Error initializing mechanical system: {e}\n',
                '#f44747'
            )


    def _setup_simulation_menu(self, scene):
        '''Populate the Simulation menu with controls.'''
        self.simulation_menu.clear()

        simulation = scene._simulation

        # Start / Stop
        start_stop_action = QAction('Start/Stop', self)
        start_stop_action.triggered.connect(
            lambda: simulation.start() if simulation.is_stopped() else simulation.stop()
        )
        self.simulation_menu.addAction(start_stop_action)

        # Pause / Resume
        pause_resume_action = QAction('Pause/Resume', self)
        pause_resume_action.triggered.connect(
            lambda: simulation.resume() if not simulation.is_running() else simulation.pause()
        )
        self.simulation_menu.addAction(pause_resume_action)


    def _setup_scene_menu(self, scene):
        '''Populate the Scene menu with drawing visibility toggles.'''
        self.scene_menu.clear()

        drawing_groups = ('points', 'vectors', 'frames', 'solids', 'grid', 'others')
        for group in drawing_groups:
            action = QAction(f'Draw {group}', self)
            action.setCheckable(True)
            action.setChecked(True)
            action.toggled.connect(
                lambda checked, g=group: scene.toogle_drawings(**{g: checked})
            )
            self.scene_menu.addAction(action)

        self.scene_menu.addSeparator()

        purge_action = QAction('Purge drawings', self)
        purge_action.triggered.connect(lambda: scene.purge_drawings())
        self.scene_menu.addAction(purge_action)


    def _show_about(self):
        '''Show the About dialog.'''
        QMessageBox.about(
            self,
            'About lib3d-mec-ginac IDE',
            'lib3d-mec-ginac IDE\n\n'
            'MATLAB-style integrated development environment\n'
            'for the lib3d-mec-ginac mechanical system library.\n\n'
            'Built with PyQt5, QScintilla, and VTK.'
        )


    def closeEvent(self, event):
        '''Clean up VTK resources on window close.'''
        self.vtk_viewer.cleanup()
        event.accept()



def main():
    '''Entry point for the IDE application.'''
    app = QApplication(sys.argv)
    app.setApplicationName('lib3d-mec-ginac IDE')

    window = MecGinacIDE()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
