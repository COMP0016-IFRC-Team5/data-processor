import os

from ._file import File

__all__ = ["Directory"]


class Directory:
    """
    A class that represents a directory on the filesystem.

    Attributes:
        __path (str): The path of the directory.
        __dirname (str): The name of the directory.
        __files (list[File]): A list of the files in the directory.
        __directories (list[Directory]): A list of the subdirectories in the
            directory.
        __content_names (list[str]): A list of the names of the files and
            subdirectories in the directory.

    Methods:
        get_directories(): Returns a list of the subdirectories in the
            directory.
        get_files(): Returns a list of the files in the directory.
        get_all_files(): Returns a list of all the files in the directory and
            its subdirectories.
        find_directory(directory): Returns the `Directory` object with the
            given name, or `None` if not found.
        find_file(file): Returns the `File` object with the given name, or
            `None` if not found.
        create_subdirectory(directory): Creates a new subdirectory with the
            given name.
        get_contents(): Returns a list of the files and subdirectories in the
            directory.
        get_content_names(): Returns a list of the names of the files and
            subdirectories in the directory.
        get_dirname(): Returns the name of the directory.
        get_path(): Returns the path of the directory.

    """
    def __init__(self, path: str):
        """
        Initializes a new `Directory` object with the given path.

        Raises:
            FileNotFoundError: If the directory does not exist.

        """
        if not os.path.exists(path):
            raise FileNotFoundError("folder does not exist")
        self.__path = path if path != "" and path[-1] != '/' else path[:-1]
        self.__dirname = os.path.basename(path)
        self.__files: list[File] = []
        self.__directories: list[Directory] = []
        self.__content_names: list[str] = []
        self.__update()

    def __scan_directory(self):
        with os.scandir(self.__path) as it:
            for entry in it:
                if entry.is_file():
                    self.__files.append(File(entry.path))
                elif entry.is_dir():
                    self.__directories.append(Directory(entry.path))

    def __update(self):
        self.__files = []
        self.__directories = []
        self.__scan_directory()
        self.__files.sort(key=lambda f: f.get_filename())
        self.__directories.sort(key=lambda d: d.get_dirname())
        self.__content_names = list(
            map(lambda c: c.get_dirname() if isinstance(c, Directory)
                else c.get_filename(),
                self.get_contents())
        )

    def get_directories(self):
        """
        Returns a list of the subdirectories in the directory.

        Returns:
            list[Directory]: A list of the subdirectories in the directory.

        """
        return self.__directories

    def get_files(self):
        """
        Returns a list of the files in the directory.

        Returns:
            list[File]: A list of the files in the directory.

        """
        return self.__files

    def get_all_files(self):
        """
        Returns a list of all the files in the directory and its subdirectories.

        Returns:
            list[File]: A list of all the files in the directory and its
                subdirectories.

        """
        files: list[File] = []
        files.extend(self.__files)
        for d in self.__directories:
            files.extend(d.get_files())
        return files

    def find_directory(self, directory: str):
        """
        Returns the `Directory` object with the given name, or `None` if not
        found.

        Parameters:
            directory (str): The name of the directory to find.

        Returns:
            Directory: The `Directory` object with the given name, or `None` if
            not found.

        """
        return next(
            (d for d in self.__directories if d.get_dirname() == directory),
            None
        )

    def find_file(self, file: str):
        """
        Returns the `File` object with the given name, or `None` if not found.

        Parameters:
            file (str): The name of the file to find.

        Returns:
            File: The `File` object with the given name, or `None` if not found.

        """
        return next((f for f in self.__files if f.get_filename() == file), None)

    def create_subdirectory(self, directory):
        """
        Creates a new subdirectory with the given name.

        Parameters:
            directory (str): The name of the subdirectory to create.

        """
        path = f"{self.__path}/{directory}"
        if os.path.exists(path):
            return
        os.makedirs(path)
        self.__update()

    def get_contents(self):
        """Returns a list of the files and subdirectories in the directory."""
        contents = []
        contents.extend(self.__files)
        contents.extend(self.__directories)
        return contents

    def get_content_names(self):
        """Returns a list of the names of the files and subdirectories in the
        directory.
        """
        return self.__content_names

    def get_dirname(self):
        """Returns the name of the directory."""
        return self.__dirname

    def get_path(self):
        """Returns the path of the directory."""
        return self.__path
