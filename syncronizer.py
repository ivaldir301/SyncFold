from utils.files import FileOperator
import shutil
import time
import os

class SyncFold:
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
    
    def get_source_file_names(self):
        try:
            return self.get_file_names(self.source_folder)
        except Exception as e:
            self.logger.error(f"Error retrieving source filenames: {e}")

    def get_destiny_file_names(self):
        try:
            return self.get_file_names(self.destiny_folder)
        except Exception as e:
            self.logger.error(f"Error retrieving filenames from the replica folder: {e}")

    def get_common_files_and_update(self):
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

    def copy_missing_files_in_destiny(self):
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

    def remove_non_coexisting_files(self):
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

    def get_directories_from_source(self):
        try:
            return self.get_subdirectories(self.source_folder)
        except Exception as e:
            self.logger.error(f"Error getting source directories {e}")

    def get_directories_from_destiny(self):
        try:
            return self.get_subdirectories(self.destiny_folder)
        except Exception as e:
            self.logger.error(f"Error getting directories from replica folder {e}")

    def check_destiny_for_missing_directories(self):
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

    def run_sincronization(self):
        start = time.time()

        self.check_destiny_for_missing_directories()
        self.get_common_files_and_update()
        self.copy_missing_files_in_destiny()
        self.remove_non_coexisting_files()
        
        end = time.time()
        lapse = end - start
        self.logger.info(f"sync operation runned! (Duration: {(lapse)} seconds.)")
