import os
from iterator import AnnIterator as AnIt
from create_annot import Annotation
from dataset_copying import dataset_copying
from dataset_copying_random import dataset_copying_random
from create_annot import create_annotation as crt
import sys
from PyQt6.QtWidgets import (QPushButton, QInputDialog, QApplication,
                             QMainWindow, QFileDialog, QLabel)
from PyQt6.QtCore import QSize, Qt
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtGui import QPixmap


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Work with dataset")
        self.setStyleSheet("background-color : #FFDEAD")
        self.setMinimumSize(650, 350)
        self.dataset_path = QFileDialog.getExistingDirectory(self, 'Выберите папку исходного датасета')
        ann = Annotation(os.path.join(self.dataset_path, "file_csv.csv"))
        if not os.path.exists("file_csv.csv"):
            crt(self.dataset_path, ann)

        src = QLabel(f'Исходный датасет:\n{self.dataset_path}', self) 
        src.setFixedSize(QSize(250, 50))
        src.move(5, 0)

        button_crt_annotation = self.add_button("Сформировать аннотацию", 250, 50, 5, 50)
        button_crt_annotation.clicked.connect(self.create_annotation)

        button_dataset_copy = self.add_button("Скопировать датасет", 250, 50, 5, 100)
        button_dataset_copy.clicked.connect(self.dataset_copy)

        button_dataset_random = self.add_button("Рандом датасета", 250, 50, 5, 150)
        button_dataset_random.clicked.connect(self.dataset_random)

        path_1 = ann.first_file_text("1")
        iterator_1 = AnIt(path_1)
        path_2 = ann.first_file_text("2")
        iterator_2 = AnIt(path_2)
        path_3 = ann.first_file_text("3")
        iterator_3 = AnIt(path_3)
        path_4 = ann.first_file_text("4")
        iterator_4 = AnIt(path_4)
        path_5 = ann.first_file_text("5")
        iterator_5 = AnIt(path_5)
        
        button_next_1 = self.add_button("файл с номером звезды 1 следующий", 250, 50, 5, 200)
        button_next_1.clicked.connect(lambda label="1", cur_iter=iterator_1: self.next(label, cur_iter))

        button_next_2 = self.add_button("файл с номером звезды 2 следующий", 250, 50, 5, 250)
        button_next_2.clicked.connect(lambda label="2", cur_iter=iterator_2: self.next(label, cur_iter))

        button_next_3 = self.add_button("файл с номером звезды 3 следующий", 250, 50, 5, 300)
        button_next_3.clicked.connect(lambda label="3", cur_iter=iterator_3: self.next(label, cur_iter))

        button_next_4 = self.add_button("файл с номером звезды 4 следующий", 250, 50, 5, 350)
        button_next_4.clicked.connect(lambda label="4", cur_iter=iterator_4: self.next(label, cur_iter))

        button_next_5 = self.add_button("файл с номером звезды 5 следующий", 250, 50, 5, 400)
        button_next_5.clicked.connect(lambda label="5", cur_iter=iterator_5: self.next(label, cur_iter))

        self.show()

    def next(self, label: str, cur_iter: AnIt):
        try:
            next_file = cur_iter.__next__()
            with open(os.path.join(cur_iter.directory, next_file), 'r') as file:
                text_content = file.read()
            self.image.setText(text_content)
            self.adjustSize()

        except StopIteration:
            self.image.setText(f"Отзывы {label} закончились.")
        except OSError as err:
            print(err)
        
    def add_button(self, name: str, size_x: int, size_y: int, pos_x: int, pos_y: int):
        button = QPushButton(name, self)
        button.setFixedSize(QSize(size_x, size_y))
        button.move(pos_x, pos_y)
        return button

    def create_annotation(self) -> None:
        text, ok = QInputDialog.getText(self, 'Ввод', 'Введите название файла-аннотации:')
        if ok:
            a = Annotation(os.path.join(self.dataset_path, f"{str(text)}.csv"))
            crt(self.dataset_path, a)

    def dataset_copy(self):
        path_copy = QFileDialog.getExistingDirectory(self, 'Введите путь к папке')
        if not path_copy:
            return
        text, ok = QInputDialog.getText(self, 'Ввод', 'Введите название файла-аннотации:')
        if ok:
            a = Annotation(os.path.join(self.dataset_path, f"{str(text)}.csv"))
            dataset_copying(self.dataset_path, path_copy, a)

    def dataset_random(self):
        path_copy = QFileDialog.getExistingDirectory(self, 'Введите путь к папке')
        if not path_copy:
            return
        name, test = QInputDialog.getText(self, 'Ввод', 'Введите название файла-аннотации:')
        if test:
            a = Annotation(os.path.join(self.dataset_path, f'{str(name)}.csv'))
            dataset_copying_random(self.dataset_path, path_copy, a)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()