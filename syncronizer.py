from utils.files import FileOperator
import shutil
import time
import os

class SyncFold:
    """
    This class represents the attributes and methods to do operations such as scan directories, sub-directories, and their respective files,
    to then proceed to sync the exact state of the source folder/file path in the specified destiny/replica path.

    Attributes:
        source_folder: str
        destiny_folder: str
        logger: logger
    """

    def __init__(self, source_folder: str, destiny_folder: str, logger):
        if not os.path.exists(source_folder):
            self.logger.error("Error: The provided path for source folder does not exist.")
            exit()

        if not os.path.isdir(source_folder):
            self.logger.error(f"Error: {source_folder} is not an directory.")
            exit()

        self.logger = logger
        self.source_folder = source_folder
        self.destiny_folder = destiny_folder


    def get_file_names(self, source_folder) -> list:
        """
        This method scans throught a folder passed, collecting all the file names that it finds and returns a list of them.

        Args:
            source_folder: str
        
        Returns:
            all_files: list

        Raises:
           PermissionError: When the user that run the program does not have enough permissions to read the file names in the passed path.
           OSError: Whenever there's some type of error or crash originated in the Operative System. 
        """

        all_files = []

        try:
            for root, dirs, files in os.walk(source_folder):
                for file in files:
                    relative_path = os.path.relpath(os.path.join(root, file), source_folder)
                    all_files.append(relative_path)
        except PermissionError:
            self.logger.error(f"Error: Permission denied while accessing files in the source folder.")
        except OSError as e:
            self.logger.error(f"An unexpected error occurred while walking through the folder: {str(e)}")

        return all_files
    
    def get_source_file_names(self) -> list:
        try:
            return self.get_file_names(self.source_folder)
        except Exception as e:
            self.logger.error(f"Error retrieving source filenames: {e}")

    def get_destiny_file_names(self) -> list:
        try:
            return self.get_file_names(self.destiny_folder)
        except Exception as e:
            self.logger.error(f"Error retrieving filenames from the replica folder: {e}")

    def get_common_files_and_update(self) -> None:
        """
        This method get's all the files from the source directory path, all the files from the destiny path, and
        then checks which common files there's in the source and in the destiny folder, and matches the content of them there.

        Args:
            None

        Returns:
            None
        
        Raises:
            PermissionError: When the current user used to run the program does not have enough permissions to copy files from source folder to destiny folder. 
            OSError: Whenever there's some type of error or crash originated in the Operative System. 
            Exception: Any other exception not expecified throught the except blocks specificly will be thrown freely and logged.
        """

        source_directory_files = self.get_source_file_names()
        destiny_directory_files = self.get_destiny_file_names()

        same_files = [item for item in source_directory_files if item in destiny_directory_files]
        try:
            for file_name in same_files:
                source_path = os.path.join(self.source_folder, file_name)
                replica_path = os.path.join(self.destiny_folder, file_name)
                if not FileOperator.compare_file(source_path, replica_path, self.logger):
                    FileOperator.replicate_file(source_path, replica_path, self.logger)
                    self.logger.info(f'File: {file_name} successfully updated.')
        except PermissionError as e:
            self.logger.error(e)
        except OSError as e:
            self.logger.error(e)
        except Exception as e:
            self.logger.error(f'An error happened while updating common files: {type(e).__name__} - {e}')

    def copy_missing_files_in_destiny(self) -> None:
        """
        This method checks which files are in the source folder path but are not present in the destiny
        path, then proceeding to creating the missing files in the destiny folder.

        Args:
            None
        
        Returns:
            None
        """
        
        source_files = self.get_source_file_names()
        destiny_files = self.get_destiny_file_names()

        try:
            missing_files = [item for item in source_files if item not in destiny_files]
            for file in missing_files:
                source_path = os.path.join(self.source_folder, file)
                destiny_path = os.path.join(self.destiny_folder, file)
                FileOperator.replicate_file(source_path, destiny_path, self.logger)
                self.logger.info(f'File: {file} successfully copied to backup.')
        except Exception as e: 
            self.logger.error(e)

    def remove_non_coexisting_files(self) -> None:
        """
        This method checks in the destiny directory path, for files that are not present in the source path, 
        and then deletes them.

        Args:
            None
        
        Returns:
            None
        """

        try:
            source_files = self.get_source_file_names()
            destiny_files = self.get_destiny_file_names()

            extra_files = [item for item in destiny_files if item not in source_files]
            for file in extra_files:
                destiny_path = os.path.join(self.destiny_folder, file)
                os.remove(destiny_path)
                self.logger.info(f'File: {file} deleted from backup folder.')
        except PermissionError as e:
            self.logger.error(e)
        except OSError as e:
            self.logger.error(e)
        except Exception as e:
            self.logger.error(f'An unexpected error occurred during _remove_extra_files: {type(e).__name__} - {str(e)}')

    def get_subdirectories(self, folder_directory) -> list:
        """
        This method goes throught a directory path passed and get's all the folders present inside it.

        Args:
            folder_directory: str

        Returns:
            None

        Raises:
            PermissionError: When the current user used to run the program does not have enough permissions to copy files from source folder to destiny folder. 
            OSError: Whenever there's some type of error or crash originated in the Operative System. 
            Exception: Any other exception not expecified throught the except blocks specificly will be thrown freely and logged. 
        """

        subdirectories = []

        try:
            for dirpath, _, _ in os.walk(folder_directory):
                rel_path = os.path.relpath(dirpath, folder_directory)
                if rel_path != '.':
                    subdirectories.append(rel_path)
        except PermissionError:
            self.logger.error(f"Error: Permission denied while accessing files in the {folder_directory} folder.")
        except OSError as e:
            self.logger.error(f"An unexpected error occurred while walking through the folder: {str(e)}")
        except Exception as e:
            self.logger.error(f'An unexpected error occurred retrieving subdirectories: {type(e).__name__} - {str(e)}')

        return subdirectories

    def get_directories_from_source(self) -> list:
        try:
            return self.get_subdirectories(self.source_folder)
        except Exception as e:
            self.logger.error(f"Error getting source directories {e}")

    def get_directories_from_destiny(self) -> list:
        try:
            return self.get_subdirectories(self.destiny_folder)
        except Exception as e:
            self.logger.error(f"Error getting directories from replica folder {e}")

    def check_destiny_for_missing_directories(self) -> None:
        """
        This method goes throught the source directory and the destiny directory, checks which folders are present
        in the source but not in the destiny directory, and then proceeds to creating them in the destiny directory.

        Args:
            None

        Returns:
            None

        Raises:
            PermissionError: When the current user used to run the program does not have enough permissions to copy files from source folder to destiny folder. 
            OSError: Whenever there's some type of error or crash originated in the Operative System. 
            Exception: Any other exception not expecified throught the except blocks specificly will be thrown freely and logged.
        """

        try:
            source_directory = self.get_directories_from_source()
            destiny_directory = self.get_directories_from_destiny()

            missing_dirs = [item for item in source_directory if item not in destiny_directory]
            for directory in missing_dirs:
                os.mkdir(os.path.join(self.destiny_folder, directory))
                self.logger.info(f'Directory-> {directory} created in destiny folder.')

            extra_dirs = [item for item in destiny_directory if item not in source_directory]
            for directory in extra_dirs:
                shutil.rmtree(os.path.join(self.destiny_folder, directory))
                self.logger.info(f'Directory-> {directory} deleted from destiny folder.')

        except PermissionError as e:
            self.logger.error(f"Error: Permission denied while accessing directories. - {e}")
        except OSError as e:
            self.logger.error(f"An unexpected error occurred: {e}")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {type(e).__name__} - {e}")

    def run_sincronization(self) -> None:
        start = time.time()

        # Orchestrating in order, the process of syncronizing the directories
        self.check_destiny_for_missing_directories()
        self.get_common_files_and_update()
        self.copy_missing_files_in_destiny()
        self.remove_non_coexisting_files()
        
        end = time.time()
        lapse = end - start
        self.logger.info(f"sync operation runned! (Duration: {(lapse)} seconds.)")
