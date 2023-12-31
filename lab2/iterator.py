import os

class AnnIterator:
    """this code implements an iterator for traversing files in a directory starting from a specific index. Each call to __next__ returns the following file name"""
    def __init__(self, directory: str):
        self.directory = directory
        self.files = os.listdir(directory)
        self.current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index < len(self.files):
            next_file = self.files[self.current_index]
            self.current_index += 1
            return next_file
        else:
            raise StopIteration

if __name__ == "__main__":
    path = "D:/PPLabs/lab2/copy_dataset"
    it = AnnIterator(path)
    print(it.__next__())
    print(it.__next__())
    print(it.__next__())
    print(it.__next__())
    print(it.__next__())
    