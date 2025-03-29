from utils.logger import configure_logger
from syncronizer import SyncFold
import pytest
import shutil
import os

logger = configure_logger("logs/test_sync.log")

# Using this function to create the test source and destiny folders instead of writing same code in every function
# and passing it as a paramether/dependency to the test functions
# the folder with the directory and test create files and deleted in the end, after the checks
@pytest.fixture
def setup_test_environment():
    source_folder = ".test/source_folder"
    destiny_folder = ".test/destiny_folder"
    os.makedirs(source_folder, exist_ok=True)
    os.makedirs(destiny_folder, exist_ok=True)
    yield source_folder, destiny_folder
    shutil.rmtree(".test")

# This function tests if the get_file_names functions retrieves the name of the files inside a path folder
def test_get_file_names(setup_test_environment):
    source_folder, _ = setup_test_environment
    file_path = os.path.join(source_folder, "test_file.txt")
    with open(file_path, "w") as file:
        file.write("abc")
    
    sync = SyncFold(source_folder, ".test/destiny_folder", logger)
    file_names = sync.get_file_names(source_folder)
    assert "test_file.txt" in file_names

# This function tests if the copy_missing_files_in_destiny can check all the files that are present in 
# origin folder but not in destiny, and then create an exact copy of them
def test_copy_missing_files_in_destiny(setup_test_environment):
    source_folder, destiny_folder = setup_test_environment
    file_path = os.path.join(source_folder, "missing_file.txt")
    with open(file_path, "w") as file:
        file.write("Missing file content")
    
    sync = SyncFold(source_folder, destiny_folder, logger)
    sync.copy_missing_files_in_destiny()
    assert os.path.exists(os.path.join(destiny_folder, "missing_file.txt"))


# This function tests if the remove_non_coexisting_files can check files that are present in the destiny path
# but not in the source, and them delete them from the destiny
def test_remove_non_coexisting_files(setup_test_environment):
    source_folder, destiny_folder = setup_test_environment
    os.makedirs(os.path.join(destiny_folder), exist_ok=True)
    file_path = os.path.join(destiny_folder, "extra_file.txt")
    with open(file_path, "w") as file:
        file.write("Extra file content")
    
    sync = SyncFold(source_folder, destiny_folder, logger)
    sync.remove_non_coexisting_files()
    assert not os.path.exists(file_path)

# This function tests if get_subdirectories can return a list with all the subdirectories inside a path passed 
def test_get_subdirectories(setup_test_environment):
    source_folder, _ = setup_test_environment
    subdirectory = os.path.join(source_folder, "subdir")
    os.makedirs(subdirectory, exist_ok=True)
    
    sync = SyncFold(source_folder, ".test/destiny_folder", logger)
    subdirs = sync.get_subdirectories(source_folder)
    assert "subdir" in subdirs


# This function tests if the check_destiny_for_missing_directories can go throught the destiny path directory and check
# if there are any directories there are not there but are present in source directory, and then creates them
def test_check_destiny_for_missing_directories(setup_test_environment):
    source_folder, destiny_folder = setup_test_environment
    subdirectory = os.path.join(source_folder, "new_subdir")
    os.makedirs(subdirectory, exist_ok=True)
    
    sync = SyncFold(source_folder, destiny_folder, logger)
    sync.check_destiny_for_missing_directories()
    assert os.path.exists(os.path.join(destiny_folder, "new_subdir"))

