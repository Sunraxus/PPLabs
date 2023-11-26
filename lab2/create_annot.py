import os
import csv

class Annotation:
    def __init__(self, filename: str):
        self.rows = 0
        self.file_name = filename

    def add_line(self, path: str, filename: str, rating: str) -> None:
        with open(self.file_name, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            if self.rows == 0:
                writer.writerow(["Абсолютный путь", "Относительный путь", "Рейтинг"])
                self.rows += 1
            writer.writerow([os.path.join(path, filename), os.path.relpath(os.path.join(path, filename)), rating])
            self.rows += 1

def create_annotation(path: str, ann: Annotation) -> None:
    folders = [] 
    i = 0
    for dirs, folder, files in os.walk(path):
        if i == 0:
            folders = folder
        else:
            for file in files:
                ann.add_line(dirs, file, folders[i-1])
        i += 1

if __name__ == "__main__":
    path_the_dataset = "D:/PPLabs/lab1/dataset"
    annot = Annotation("file_annotation.csv")
    create_annotation(path_the_dataset, annot)