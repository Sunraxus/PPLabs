import os
from iterator import AnnIterator as AnIt
from create_annot import Annotation
from dataset_copying import dataset_copying
from dataset_copying_random import dataset_copying_random
from create_annot import create_annotation as crt
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import (
    QPushButton,
    QInputDialog,
    QApplication,
    QMainWindow,
    QFileDialog,
    QLabel,
)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap


class ReviewsDialog(QtWidgets.QDialog):
    def __init__(self, dataset_path, star_rating, parent=None):
        """
        Конструктор класса ReviewsDialog.

        Параметры:
        - dataset_path (str): Путь к датасету.
        - star_rating (int): Рейтинг отзывов, которые будут отображаться в диалоге.
        - parent: Родительский объект (по умолчанию None).
        """
        super(ReviewsDialog, self).__init__(parent)
        self.dataset_path = dataset_path
        self.star_rating = star_rating
        self.iterator = AnIt(os.path.join(dataset_path, str(star_rating)))
        self.init_ui()

    def init_ui(self):
        """
        Инициализация пользовательского интерфейса для диалога отображения рецензий.
        """
        self.setWindowTitle("Рецензии")
        self.setMinimumSize(400, 400)

        self.text_display = QtWidgets.QTextEdit(self)
        self.text_display.setReadOnly(True)
        self.text_display.setGeometry(QtCore.QRect(10, 10, 380, 280))

        button_next = QPushButton("Следующая рецензия", self)
        button_next.setGeometry(QtCore.QRect(10, 300, 180, 40))
        button_next.clicked.connect(self.show_next_review)

        button_close = QPushButton("Закрыть", self)
        button_close.setGeometry(QtCore.QRect(200, 300, 180, 40))
        button_close.clicked.connect(self.close)

        self.show_next_review()

    def show_next_review(self):
        """
        Отображает следующий отзыв из датасета в текстовом поле диалога.
        """
        try:
            next_file = self.iterator.__next__()
            with open(
                os.path.join(self.iterator.directory, next_file), "r", encoding="utf-8"
            ) as file:
                text_content = file.read()
                self.text_display.setPlainText(text_content)
        except StopIteration:
            self.text_display.setPlainText("Отзывы закончились.")
        except OSError as err:
            print(err)


class MainWindow(QMainWindow):
    def __init__(self):
        """
        Конструктор класса MainWindow.
        """
        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        """
        Инициализация пользовательского интерфейса основного окна приложения.
        """
        self.setWindowTitle("Work with dataset")
        self.setStyleSheet("background-color : #D6D6D6")
        self.setMinimumSize(650, 350)
        self.dataset_path = QFileDialog.getExistingDirectory(
            self, "Выберите папку исходного датасета"
        )
        ann = Annotation(os.path.join(self.dataset_path, "file_csv.csv"))
        if not os.path.exists("file_csv.csv"):
            crt(self.dataset_path, ann)

        src = QLabel(f"Исходный датасет:\n{self.dataset_path}", self)
        src.setFixedSize(QSize(300, 50))
        src.move(5, 0)

        button_crt_annotation = self.add_button(
            "Сформировать аннотацию исходного датасета", 300, 50, 5, 50
        )
        button_crt_annotation.clicked.connect(self.create_annotation)

        button_dataset_copy = self.add_button("Скопировать датасет", 300, 50, 5, 100)
        button_dataset_copy.clicked.connect(self.dataset_copy)

        button_dataset_random = self.add_button("Рандом датасета", 300, 50, 5, 150)
        button_dataset_random.clicked.connect(self.dataset_random)

        button_reviews = self.add_button(
            "Работа c отзывами с 1 звездой", 300, 50, 5, 200
        )
        button_reviews.clicked.connect(self.open_reviews_dialog)

        button_reviews_1_star = self.add_button("Отзывы с 1 звездой", 300, 50, 5, 200)
        button_reviews_1_star.clicked.connect(lambda: self.open_reviews_dialog(1))

        button_reviews_2_stars = self.add_button("Отзывы с 2 звездами", 300, 50, 5, 250)
        button_reviews_2_stars.clicked.connect(self.open_reviews_dialog_2_stars)

        button_reviews_3_stars = self.add_button("Отзывы с 3 звездами", 300, 50, 5, 300)
        button_reviews_3_stars.clicked.connect(self.open_reviews_dialog_3_stars)

        button_reviews_4_stars = self.add_button("Отзывы с 4 звездами", 300, 50, 5, 350)
        button_reviews_4_stars.clicked.connect(self.open_reviews_dialog_4_stars)

        button_reviews_5_stars = self.add_button("Отзывы с 5 звездами", 300, 50, 5, 400)
        button_reviews_5_stars.clicked.connect(self.open_reviews_dialog_5_stars)

        self.show()

    def open_reviews_dialog(self, star_rating):
        """
        Открывает диалог отображения рецензий для определенного рейтинга звезд.

        Параметры:
        - star_rating (int): Рейтинг отзывов, которые будут отображаться в диалоге.
        """
        dialog = ReviewsDialog(self.dataset_path, star_rating)
        dialog.exec()

    def open_reviews_dialog_2_stars(self):
        self.open_reviews_dialog(2)

    def open_reviews_dialog_3_stars(self):
        self.open_reviews_dialog(3)

    def open_reviews_dialog_4_stars(self):
        self.open_reviews_dialog(4)

    def open_reviews_dialog_5_stars(self):
        self.open_reviews_dialog(5)

    def add_button(self, name: str, size_x: int, size_y: int, pos_x: int, pos_y: int):
        """
        Создает и добавляет кнопку на главное окно приложения.

        Параметры:
        - name (str): Название кнопки.
        - size_x (int): Ширина кнопки.
        - size_y (int): Высота кнопки.
        - pos_x (int): Позиция по оси X.
        - pos_y (int): Позиция по оси Y.

        Возвращает:
        - QPushButton: Созданная кнопка.
        """
        button = QPushButton(name, self)
        button.setFixedSize(QSize(size_x, size_y))
        button.move(pos_x, pos_y)
        return button

    def create_annotation(self) -> None:
        """
        Создает и сохраняет аннотацию для исходного датасета.
        """
        path_annot = QFileDialog.getExistingDirectory(
            self, "Введите путь к папке куда хотите сохранить аннтоацию"
        )
        if not path_annot:
            return
        text, ok = QInputDialog.getText(
            self, "Ввод", "Введите название файла-аннотации:"
        )
        if ok:
            a = Annotation(os.path.join(path_annot, f"{str(text)}.csv"))
            crt(self.dataset_path, a)

    def dataset_copy(self):
        """
        Копирует датасет в указанное место с заданным именем аннотации.
        """
        path_copy = QFileDialog.getExistingDirectory(self, "Введите путь к папке")
        if not path_copy:
            return
        text, ok = QInputDialog.getText(
            self, "Ввод", "Введите название файла-аннотации:"
        )
        if ok:
            a = Annotation(os.path.join(path_copy, f"{str(text)}.csv"))
            dataset_copying(self.dataset_path, path_copy, a)

    def dataset_random(self):
        """
        Создает копию датасета с перемешанными данными и сохраняет аннотацию.
        """
        path_copy = QFileDialog.getExistingDirectory(self, "Введите путь к папке")
        if not path_copy:
            return
        name, test = QInputDialog.getText(
            self, "Ввод", "Введите название файла-аннотации:"
        )
        if test:
            a = Annotation(os.path.join(path_copy, f"{str(name)}.csv"))
            dataset_copying_random(self.dataset_path, path_copy, a)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
