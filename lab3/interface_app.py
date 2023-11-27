from PyQt5 import QtWidgets
from create_annot import Annotation, create_annotation, dataset_copying
import os

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Dataset Annotation Tool")

        # Create widgets
        self.folder_path_label = QtWidgets.QLabel("Select Dataset Folder:")
        self.folder_path_button = QtWidgets.QPushButton("Browse")
        self.create_annotation_button = QtWidgets.QPushButton("Create Annotation File")
        self.create_dataset_button = QtWidgets.QPushButton("Create Dataset with New Organization")

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.folder_path_label)
        layout.addWidget(self.folder_path_button)
        layout.addWidget(self.create_annotation_button)
        layout.addWidget(self.create_dataset_button)

        container = QtWidgets.QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connect signals to slots
        self.folder_path_button.clicked.connect(self.browse_folder)
        self.create_annotation_button.clicked.connect(self.create_annotation)
        self.create_dataset_button.clicked.connect(self.create_dataset)

        # Annotation object
        self.annotation = None

    def browse_folder(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder_path:
            self.annotation = Annotation("file_annotation.csv")
            create_annotation(folder_path, self.annotation)

    def create_annotation(self):
        if self.annotation:
            destination_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Annotation File', '', 'CSV Files (*.csv)')
            if destination_path:
                with open(destination_path, "w", encoding="utf-8", newline="") as f:
                    f.write("Абсолютный путь,Относительный путь,Рейтинг\n")
                    f.write("\n".join([f"{row[0]},{row[1]},{row[2]}" for row in self.annotation.rows]))

    def create_dataset(self):
        if self.annotation:
            dest_folder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Destination Folder')
            if dest_folder:
                annotation_copy = Annotation("file_annotation_copy.csv")
                dataset_copying(dest_folder, self.annotation, annotation_copy)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
