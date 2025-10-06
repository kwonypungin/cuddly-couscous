import sys
from qgis.PyQt.QtWidgets import QApplication
from qgis.core import QgsApplication

# Import the main window
from main_window import MainWindow

def main():
    """Main function to run the application."""
    # On some systems, you might need to set the QGIS prefix path
    # QgsApplication.setPrefixPath("/path/to/qgis/installation", True)
    app = QgsApplication([], True)
    app.initQgis()

    # Create and show the main window
    main_win = MainWindow()
    main_win.show()

    # Start the application event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()