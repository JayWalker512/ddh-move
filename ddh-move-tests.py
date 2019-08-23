#!/usr/bin/env python3
import os
import shutil
import subprocess

def make_file(name = "file.txt", contents = "File contents"):
    with open(name, "w") as f:
        f.write(contents)

def make_directory(path = "folder"):
    return os.mkdir(path)

def file_exists(path = None):
    return os.path.isfile(path)

def is_ddh_installed():
    ret = subprocess.run(['ddh', '--version'], stdout=subprocess.PIPE)
    if ret.returncode != 0:
        return False
    return True

def make_test_files():
    os.mkdir("test_files")
    os.mkdir("test_destination")
    make_file("test_files/abcd.txt")
    make_file("test_files/dupe1.txt")
    make_file("test_files/dupe2.txt")
    make_file("test_files/file2.txt", "Other content")

def get_dry_run_output():
    ret = subprocess.run("ddh test_files --output no --format json -v duplicates".split(), stdout=subprocess.PIPE)
    lines = ret.stdout.decode('utf-8').split('\n')
    ret = subprocess.Popen("python3 ddh-move.py test_destination --dry-run".split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    ret.stdin.write(bytes(lines[-2], encoding='utf-8'))
    output = ret.communicate()[0]
    return output.decode('utf-8')

def move_the_dupes():
    ret = subprocess.run("ddh test_files --output no --format json -v duplicates".split(), stdout=subprocess.PIPE)
    lines = ret.stdout.decode('utf-8').split('\n')
    ret = subprocess.Popen("python3 ddh-move.py test_destination".split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    ret.stdin.write(bytes(lines[-2], encoding='utf-8'))
    output = ret.communicate()[0]

def cleanup_test_files():
    shutil.rmtree("test_files", ignore_errors=True)
    shutil.rmtree("test_destination", ignore_errors=True)

def main():
    assert (True == is_ddh_installed()), "You need to have ddh installed to run the tests."

    make_test_files()

    #make sure that a --dry-run prints out the correct files
    correct_files = ["test_files/dupe1.txt", "test_files/dupe2.txt"]
    output = get_dry_run_output()
    for file in correct_files:
        assert file in output,"--dry-run option did not print the correct files!"

    #move the dupes and ensure the correct files get moved
    move_the_dupes()
    correct_files = ["dupe1.txt", "dupe2.txt"]
    for file in os.listdir("test_destination"):
        assert file in correct_files,"The test_destination folder contains an unexpected file: " + file
    #and the correct files are left behind
    unmoved_files = ["abcd.txt", "file2.txt"]
    for file in os.listdir("test_files"):
        assert file in unmoved_files,"The test_files folder contains an unexpected file: " + file

    cleanup_test_files()
    print("All tests passed!")

if __name__ == "__main__":
    main()