import os
import re 


def next_file(path: str):
    if not os.path.exists(path):
        raise FileExistsError(f'Этот {path} файл не существует.')
    direct, filename = os.path.split(path) 
    a = "".join(re.findall(r'\d', filename))
    number = int(a) + 1
    file_new = re.sub(a, f'{number:04d}', filename)
    file_new = os.path.join(direct, file_new)
    if os.path.exists(file_new):
        return file_new
    else:
        return None

if __name__ == "__main__":
    path = "D:/PPLabs/lab2/copy_dataset"
    file_path = os.path.join(path, '1_0001.txt')
    print(file_path)
    file_path = next_file(file_path)
    print(next_file(file_path))
