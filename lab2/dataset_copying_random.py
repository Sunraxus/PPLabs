from create_annot import Annotation
import os
import shutil
import random


def dataset_copying_random(path: str, path_copy_random: str, ann: Annotation) -> None:
    """This code performs a similar task of copying files and creating annotations, it also randomly renames the files being copied."""
    if not os.path.isdir(path_copy_random):
        os.mkdir(path_copy_random)
    folders = os.listdir(path)
    for folder in folders:
        files = os.listdir(os.path.join(path, folder))
        for file in files:
            shutil.copy(os.path.join(path, folder, file), path_copy_random)
            random_f = f"{random.randint(0, 10000)}.text"
            while os.path.exists(os.path.join(path_copy_random, random_f)):
                random_f = f"{random.randint(0, 10000)}.text"
            os.rename(
                os.path.join(path_copy_random, file),
                os.path.join(path_copy_random, random_f),
            )
            ann.add_line(path_copy_random, random_f, folder)


if __name__ == "__main__":
    path = "D:/PPLabs/lab1/dataset"
    path_copy_random = "D:/PPLabs/lab2/data_copy_random"
    annot = Annotation("file_annotation_copy_random.csv")
    dataset_copying_random(path, path_copy_random, annot)
