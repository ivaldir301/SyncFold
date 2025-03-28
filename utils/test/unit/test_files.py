from utils.logger import configure_logger
from utils.files import FileOperator
import hashlib
import shutil
import os

logger = configure_logger("logs/log_testing.log")

def test_replicate_file():
    test_origin_file: str = ".testing/test1/"
    test_file_path2: str = ".testing/replilca/"

    os.makedirs(test_origin_file, exist_ok=True)
    test_origin_file = test_origin_file + "testfile.txt"

    with open(test_origin_file, "w") as file:
        file.write("abc")
        file.close()

    FileOperator.replicate_file(test_origin_file, test_file_path2, logger)

    with open(test_origin_file, "rb") as file:
        test_origin = file.read()
        test_origin_md5 = hashlib.md5(test_origin).hexdigest()

    with open(test_file_path2+"testfile.txt", "rb") as file:
        test_destiny = file.read()
        test_destiny_md5 = hashlib.md5(test_destiny).hexdigest()

    assert test_origin_md5 == test_destiny_md5
    shutil.rmtree(".testing/")


def test_compare_files_with_equal():
    test_file1: str = ".testing/test1.txt"
    test_file2: str = ".testing/test2.txt"

    os.makedirs(".testing/")

    with open(test_file1, "w") as file:
        file.write("abc")
        file.close()

    with open(test_file2, "w") as file:
        file.write("abc")
        file.close()

    with open(test_file1, "rb") as file:
        file_data = file.read()
        file1_md5 = hashlib.md5(file_data).hexdigest()

    with open(test_file2, "rb") as file:
        file_data = file.read()
        file2_md5 = hashlib.md5(file_data).hexdigest()

    function_result = FileOperator.compare_file(test_file1, test_file2, logger)
    compare_result = (file1_md5 == file2_md5)
    assert function_result == compare_result
    shutil.rmtree(".testing/")

def test_compare_files_with_different():
    test_file1: str = ".testing/test1.txt"
    test_file2: str = ".testing/test2.txt"

    os.makedirs(".testing/")
    with open(test_file1, "w") as file:
        file.write("abc")
        file.close()

    with open(test_file2, "w") as file:
        file.write("def")
        file.close()

    with open(test_file1, "rb") as file:
        file_data = file.read()
        file1_md5 = hashlib.md5(file_data).hexdigest()

    with open(test_file2, "rb") as file:
        file_data = file.read()
        file2_md5 = hashlib.md5(file_data).hexdigest()

    function_result = FileOperator.compare_file(test_file1, test_file2, logger)
    compare_result = (file1_md5 == file2_md5)
    assert function_result == compare_result
    shutil.rmtree(".testing/")
