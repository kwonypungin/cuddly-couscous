# -*- coding: utf-8 -*-

import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QInputDialog
from qgis.core import QgsProject, QgsCoordinateReferenceSystem, QgsRasterLayer

# This loads your UI file so that PyQt can populate the plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'forms', 'hgis_dialog_base.ui'))


class HgisDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(HgisDialog, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.btn_coords.clicked.connect(self.set_korean_crs)
        self.btn_bg_map.clicked.connect(self.add_background_map)
        self.btn_georef.clicked.connect(self.open_georeferencer)
        self.btn_draw.clicked.connect(self.open_drawing_tools)
        self.btn_export.clicked.connect(self.export_data)
        self.btn_layer_manager.clicked.connect(self.open_layer_manager)

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

    def set_korean_crs(self):
        """Show a dialog to select and apply a Korean CRS to the project."""
        crs_name, ok = QInputDialog.getItem(self, "Select Korean Coordinate System",
                                            "Coordinate Systems:", list(self.korean_crs_list.keys()), 0, False)

        if ok and crs_name:
            epsg_code = self.korean_crs_list[crs_name]
            crs = QgsCoordinateReferenceSystem(epsg_code)
            QgsProject.instance().setCrs(crs)
            self.iface.messageBar().pushMessage("Success", f"Project CRS set to {crs_name}", level=0, duration=3)

    def add_background_map(self):
        """Add a background map (OpenStreetMap) to the project."""
        url = "type=xyz&url=https://a.tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0"
        rlayer = QgsRasterLayer(url, "OpenStreetMap", "wms")

        if not rlayer.isValid():
            self.iface.messageBar().pushMessage("Error", "Failed to load background map.", level=2, duration=5)
            return

        QgsProject.instance().addMapLayer(rlayer)
        self.iface.messageBar().pushMessage("Success", "OpenStreetMap background map added.", level=0, duration=3)

    def open_georeferencer(self):
        """Open the QGIS Georeferencer."""
        try:
            # In QGIS 3, the georeferencer is a core plugin
            self.iface.georeferencer().show()
        except Exception as e:
            self.iface.messageBar().pushMessage("Error", f"Could not open Georeferencer: {e}", level=2, duration=5)

    def open_drawing_tools(self):
        """Placeholder for drawing tools functionality."""
        self.iface.messageBar().pushMessage("Info", "Drawing tools feature is under development.", level=1, duration=5)

    def export_data(self):
        """Placeholder for export functionality."""
        self.iface.messageBar().pushMessage("Info", "Export feature is under development.", level=1, duration=5)

    def open_layer_manager(self):
        """Placeholder for layer management functionality."""
        self.iface.messageBar().pushMessage("Info", "Layer Management feature is under development.", level=1, duration=5)