import hashlib
import shutil
import os


class FileOperator:
    """
        This class has the method operations used for files in the SyncFile, for copying files 
        from one path to another and for comparing two files.

        Methods:
            replicated_file -> Copies a file from the source path, into a destiny path, passed by 
            the user.

                args:
                    source_path: str
                    destiny_path: str

                returns:
                    none

            compare_file -> compares the contents between two files, and returns the difference.

                args:
                   source_path: str
                   destiny_path: str

                returns:
                    True - if files are equal | False - if they are different
    """
    @staticmethod
    def replicate_file(source_path: str, destiny_path: str):
        from utils.logger import configure_logger
        logging = configure_logger("./logs/log_today.log")
        try:
            logging.info(f"start file replication: {source_path} - {destiny_path}")
            destiny_path = os.path.dirname(destiny_path)
            os.makedirs(destiny_path, exist_ok=True)

            shutil.copy2(source_path, destiny_path)
            logging.info("file replicated successfully!")
        except FileNotFoundError as e:
            logging.error(f"ERROR: specified source file for copy was not found: {source_path}")
            logging.error(f"{e}")
        except PermissionError as e:
            logging.error(f"ERROR: os user does not have the permissions to copy the files.")
            logging.error(f"{e}")
        except shutil.SameFileError as e:
            logging.error(f"ERROR: the source and destiny paths passed are the same.")
            logging.error(f"{e}")
        except IsADirectoryError as e:
            logging.error("ERROR: the path passed for source is a directory, not a file.")
            logging.error(f"{3}")
        except TypeError as e:
            logging.error("ERROR: an invalid argument was provided as a path.")
            logging.error(f"{e}")
        except Exception as e:
            logging.error("ERROR: unknown exception occured.")
            logging.error(f"{e}")

    @staticmethod
    def compare_file(source_path: str, destiny_path: str):
        from utils.logger import configure_logger
        logging = configure_logger("./logs/log_today.log")

        try:
            logging.info(f"starting comparison of two files: {source_path} - {destiny_path}")
            with open(source_path, "rb") as source_file:
                source_file_data = source_file.read()
                source_file_md5 = hashlib.md5(source_file_data).hexdigest()

            with open(destiny_path, "rb") as destiny_file:
                destiny_file_data = destiny_file.read()
                destiny_file_md5 = hashlib.md5(destiny_file_data).hexdigest()

            logging.info("comparison operation successfull!")
            return (source_file_md5 == destiny_file_md5)
        except FileNotFoundError as e:
            logging.error(f"ERROR: specified source file for copy was not found: {source_path}")
            logging.error(f"{e}")
        except PermissionError as e:
            logging.error(f"ERROR: os user does not have the permissions to open the files.")
            logging.error(f"{e}")
        except UnicodeDecodeError as u:
            logging.error(f"ERROR: there was an error decoding the files.")
            logging.error(f"{e}")
        except IsADirectoryError as d:
            logging.error("ERROR: the path passed for source is a directory, not a file.")
            logging.error(f"{e}")
        except Exception as e:
            logging.error("ERROR: unknown exception occured.")
            logging.error(f"{e}")
