import os
from typing import Optional


def print_next(class_mark: str, path) -> Optional[str]:
    path = os.path.join(path, class_mark)
    names_list = os.listdir(path)
    for i in range(0, len(names_list)):
        file_path = os.path.join(path, names_list[i])
        yield file_path
    yield None
        
if __name__ == '__main__':
    path = "D:/PPLabs/lab2/dataset/";
    for i in print_next('4', path):
        print(i)