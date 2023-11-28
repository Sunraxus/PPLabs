import os
import csv
import logging

class Annotation:
    def __init__(self, filename: str):
        """The method is a constructor of the class that initializes the Annotation object. Takes filename as an argument."""
        self.rows = 0
        self.filename = filename
        self.__header = ['Absolute Path', 'Relative Path', 'Label']

    def add_line(self, path: str, filename: str, label: str) -> None:
        """A method for adding a line to an annotation. Accepts path, filename, and label."""
        with open(self.filename, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            if self.rows == 0:
                writer.writerow(["Absolute Path", "Relative Path", "Label"])
            writer.writerow([os.path.join(path, filename), os.path.relpath(os.path.join(path, filename)), label])
            self.rows += 1

    def first_file_text(self, label: str):
        """Method for getting the path to the first file with the specified label."""
        res = [] 
        try:
            with open(self.filename, 'r') as file:
                rows = csv.DictReader(file)
                for row in rows:
                    if row[self.__header[2]] == label:
                        return row[self.__header[0]]
        except OSError as err:
            logging.warning(f' При попытке открытия аннотации {self.filename} произошла ошибка:\n{err}.')
        return res[0]
def create_annotation(path: str, ann: Annotation) -> None:
    """A function for creating annotations based on files in the specified directory."""
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