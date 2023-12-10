from create_annot import Annotation
import os
import shutil


def dataset_copying(path: str, path_copy: str, ann: Annotation) -> None:
    """This code copies files from the source directory to the new directory and simultaneously creates an annotation for the copied files."""
    if not os.path.isdir(path_copy):
        os.mkdir(path_copy)
    folders = os.listdir(path)
    for folder in folders:
        files = os.listdir(os.path.join(path, folder))
        for file in files:
            shutil.copy(os.path.join(path, folder, file), path_copy)
            os.rename(
                os.path.join(path_copy, file),
                os.path.join(path_copy, f"{folder}_{file}"),
            )
            ann.add_line(path_copy, f"{folder}_{file}", folder)


if __name__ == "__main__":
    path = "D:/PPLabs/lab1/dataset"
    path_copy = "D:/PPLabs/lab2/copy_dataset"
    annot = Annotation("file_annotation_copy.csv")
    dataset_copying(path, path_copy, annot)
