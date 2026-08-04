'''
VTK Viewport Widget for PyQt5.
Embeds a VTK 3D render window inside a PyQt5 QWidget.
'''

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk


class VtkViewportWidget(QWidget):
    '''
    VTK Viewport Widget for PyQt5.
    Embeds a VTK render window and handles interaction and rendering loop.
    '''

    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene = None
        self._selected_drawing = None
        self._interactor_initialized = False

        # Setup layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create VTK widget
        self.vtkWidget = QVTKRenderWindowInteractor(self)
        layout.addWidget(self.vtkWidget)

        # Create default renderer with dark background
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(0.15, 0.15, 0.15)
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)

        # Setup interactor style
        self.interactor = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.interactor_style = vtk.vtkInteractorStyleTrackballCamera()
        self.interactor.SetInteractorStyle(self.interactor_style)

        # Setup picking via left button press observer
        self.interactor.AddObserver(vtk.vtkCommand.LeftButtonPressEvent, self._on_left_button_press)

        # Setup render loop timer (30 Hz)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._refresh)
        self.timer.start(1000 // 30)


    def set_scene(self, scene):
        '''
        Set the scene and add its renderer to the render window.
        '''
        self.scene = scene

        if scene and hasattr(scene, '_renderer'):
            render_window = self.vtkWidget.GetRenderWindow()

            # Remove existing renderers
            renderers = render_window.GetRenderers()
            renderers.InitTraversal()
            ren = renderers.GetNextItem()
            while ren:
                render_window.RemoveRenderer(ren)
                ren = renderers.GetNextItem()

            # Add scene's renderer
            self.renderer = scene._renderer
            render_window.AddRenderer(self.renderer)

            self.renderer.ResetCamera()
            render_window.Render()


    def _refresh(self):
        '''
        Refresh loop to update scene drawings and re-render.
        '''
        if self.scene and hasattr(self.scene, '_update_drawings'):
            try:
                self.scene._update_drawings()
            except Exception:
                pass

        # Only render if visible and initialized
        if self.isVisible() and self._interactor_initialized:
            try:
                self.vtkWidget.GetRenderWindow().Render()
            except Exception:
                pass


    def _on_left_button_press(self, obj, event):
        '''
        Handle picking of 3D objects on left click.
        '''
        if not self.interactor or not self.scene:
            return

        # Get mouse click position
        x, y = self.interactor.GetEventPosition()
        picker = vtk.vtkPropPicker()
        picker.Pick(x, y, 0, self.renderer)

        # Get the drawing attached to the picked actor
        actor = picker.GetActor()
        drawing = None
        if actor and hasattr(self.scene, '_get_3D_drawing_by_handler'):
            drawing = self.scene._get_3D_drawing_by_handler(actor)

        # Handle selection/deselection
        prev_selected = self._selected_drawing
        self._selected_drawing = drawing

        if drawing is None:
            if prev_selected is not None and hasattr(prev_selected, 'unselect'):
                prev_selected.unselect()
        else:
            if drawing is not prev_selected:
                if prev_selected is not None and hasattr(prev_selected, 'unselect'):
                    prev_selected.unselect()
                if hasattr(drawing, 'select'):
                    drawing.select()


    def showEvent(self, event):
        '''
        Initialize the VTK interactor when the widget becomes visible.
        '''
        super().showEvent(event)
        if not self._interactor_initialized:
            self.interactor.Initialize()
            self._interactor_initialized = True


    def cleanup(self):
        '''
        Clean up VTK resources.
        '''
        if self.timer:
            self.timer.stop()
        if self.vtkWidget:
            try:
                self.vtkWidget.Finalize()
            except Exception:
                pass
