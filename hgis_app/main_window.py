import os
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QMainWindow, QInputDialog
from qgis.core import QgsProject, QgsCoordinateReferenceSystem, QgsRasterLayer
from qgis.gui import QgsMapCanvas, QgsLayerTreeView

# Load the UI file
FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'main_window.ui'))

class MainWindow(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # Set up the map canvas
        self.mapCanvas = QgsMapCanvas()
        self.gridLayout.addWidget(self.mapCanvas, 0, 1) # Add canvas to the grid layout

        # Set up the layer tree view
        self.layerTreeView = QgsLayerTreeView()
        self.layerTreeView.setCanvas(self.mapCanvas)
        self.dockWidget.setWidget(self.layerTreeView) # Add layer tree to the dock

        # Connect the project's layer tree to our view
        self.layerTreeView.setModel(QgsProject.instance().layerTreeRoot())

        # Connect buttons to placeholder functions
        self.btn_coords.clicked.connect(self.set_coordinate_system)
        self.btn_bg_map.clicked.connect(self.add_background_map)
        self.btn_georef.clicked.connect(self.open_georeferencer)
        self.btn_draw.clicked.connect(self.open_drawing_tools)
        self.btn_export.clicked.connect(self.export_data)

        self.korean_crs_list = {
            "Bessel (Tokyo) / Korea Central Belt (EPSG:5174)": "EPSG:5174",
            "Korean 1985 / Central Belt (EPSG:5181)": "EPSG:5181",
            "Korean 1985 / East Sea Belt (EPSG:5183)": "EPSG:5183",
            "Korean 1985 / West Belt (EPSG:5180)": "EPSG:5180",
            "Korean 2000 / Central Belt (EPSG:5186)": "EPSG:5186",
            "Korean 2000 / East Belt (EPSG:5187)": "EPSG:5187",
            "Korean 2000 / West Belt (EPSG:5185)": "EPSG:5185",
            "UTM Zone 52N (WGS 84) (EPSG:32652)": "EPSG:32652",
        }

        print("Main window initialized.")

    def set_coordinate_system(self):
        """Show a dialog to select and apply a Korean CRS to the project."""
        crs_name, ok = QInputDialog.getItem(self, "Select Korean Coordinate System",
                                            "Coordinate Systems:", list(self.korean_crs_list.keys()), 0, False)

        if ok and crs_name:
            epsg_code = self.korean_crs_list[crs_name]
            crs = QgsCoordinateReferenceSystem(epsg_code)
            self.mapCanvas.setDestinationCrs(crs)
            print(f"Map canvas CRS set to {crs_name}")

    def add_background_map(self):
        """Add a background map (OpenStreetMap) to the project."""
        url = "type=xyz&url=https://a.tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0"
        rlayer = QgsRasterLayer(url, "OpenStreetMap", "wms")

        if not rlayer.isValid():
            print("Error: Failed to load background map.")
            return

        QgsProject.instance().addMapLayer(rlayer)
        print("OpenStreetMap background map added.")

    def open_georeferencer(self):
        print("Georeferencer feature is planned for a future version.")

    def open_drawing_tools(self):
        print("Drawing tools feature is planned for a future version.")

    def export_data(self):
        print("Export feature is planned for a future version.")