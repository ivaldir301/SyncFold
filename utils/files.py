import hashlib
import shutil
import os


class FileOperator:
    """
    This class has the method operations used for files in the SyncFile, for copying files 
    from one path to another and for comparing two files.

    Attributes:
        None
    """

    @staticmethod
    def replicate_file(source_path: str, destiny_path: str, logger) -> None:
        """
        This function takes in the source file and replicates/copies it to the destiny path, passed in the paramethers.

        Args:
            source_path: str
            destiny_path: str
            logger: logger
        
        Returns:
            None

        Raises:
           FileNotFoundError: When the source file path passed is not found or inexistent in the disk
           PermissionError: When the current user used to run the program does not have enough permissions to copy files from source folder to destiny folder. 
           shutil.SameFileError: When the paths passed to the function referenciates to the same file.
           IsADirectoryError: When the path passed as source referenciates to a directory, instead of a file.
           TypeError: When there's an error with the format string passed as a path, for source and or for destiny path.
           Exception: Any other exception not expecified throught the except blocks specificly will be thrown freely and logged.
        """
        
        try:
            logger.info(f"start file replication: {source_path} - {destiny_path}")
            destiny_path = os.path.dirname(destiny_path)
            os.makedirs(destiny_path, exist_ok=True)

            shutil.copy2(source_path, destiny_path)
            logger.info("file replicated successfully!")
        except FileNotFoundError as e:
            logger.error(f"ERROR: specified source file for copy was not found: {source_path}")
            logger.error(f"{e}")
        except PermissionError as e:
            logger.error(f"ERROR: os user does not have the permissions to copy the files.")
            logger.error(f"{e}")
        except shutil.SameFileError as e:
            logger.error(f"ERROR: the source and destiny paths passed are the same.")
            logger.error(f"{e}")
        except IsADirectoryError as e:
            logger.error("ERROR: the path passed for source is a directory, not a file.")
            logger.error(f"{3}")
        except TypeError as e:
            logger.error("ERROR: an invalid argument was provided as a path.")
            logger.error(f"{e}")
        except Exception as e:
            logger.error("ERROR: unknown exception occured.")
            logger.error(f"{e}")

    @staticmethod
    def compare_file(source_path: str, destiny_path: str, logger) -> None:
        """
        This function takes in two files paths, and compares two generate hashes using the MD5 algorithm, checking if the two files are equal.

        Args:
            source_path: str
            destiny_path: str
            logger: logger

        Returns:
            None
        
        Raises:
            FileNotFoundError: When the source file path passed is not found or inexistent in the disk
            PermissionError: When the current user used to run the program does not have enough permissions to copy files from source folder to destiny folder. 
            UnicodeDecodeError: This exception happens when the decoding process fails.
            TypeError: When there's an error with the format string passed as a path, for source and or for destiny path.
            Exception: Any other exception not expecified throught the except blocks specificly will be thrown freely and logged.
        """
        try:
            logger.info(f"starting comparison of two files: {source_path} - {destiny_path}")
            with open(source_path, "rb") as source_file:
                source_file_data = source_file.read()
                source_file_md5 = hashlib.md5(source_file_data).hexdigest()

            with open(destiny_path, "rb") as destiny_file:
                destiny_file_data = destiny_file.read()
                destiny_file_md5 = hashlib.md5(destiny_file_data).hexdigest()

            logger.info("comparison operation successfull!")
            return (source_file_md5 == destiny_file_md5)
        except FileNotFoundError as e:
            logger.error(f"ERROR: specified source file for copy was not found: {source_path}")
            logger.error(f"{e}")
        except PermissionError as e:
            logger.error(f"ERROR: os user does not have the permissions to open the files.")
            logger.error(f"{e}")
        except UnicodeDecodeError as u:
            logger.error(f"ERROR: there was an error decoding the files.")
            logger.error(f"{e}")
        except IsADirectoryError as d:
            logger.error("ERROR: the path passed for source is a directory, not a file.")
            logger.error(f"{e}")
        except Exception as e:
            logger.error("ERROR: unknown exception occured.")
            logger.error(f"{e}")
