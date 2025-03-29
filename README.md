# SincFold

SincFold is a command line program that syncronises two directories and it's contents periodicly, maintaining them the exact same in content and structure.

## How it works?

The program first takes a source folder provided by the user, which is the folder that will be used as template to create the replica with.
Then with the second path(replica path), it will scan throught the source directory, looking for all the files and directories existing there, then checks the
files in replica that are not in source, deletes them, and create the files and directories that are in source but not in the replica folder, while also
creating an exact copy of similar files that are in both folders, but the copy in replica does not match the contents of the one in source.

It will also show live logs of all the process, while also saving the logs to a log file, in the file path provided for the logs.

SincFold takes in 3 paramethers:
``` --source ```the source directory which you want to syncronize from
``` --replica ``` the destiny/replica directory, which you want the source folder to be syncronized with
``` --log_folder ``` the path which you want the logger file to be created
``` --interval ``` the time interval in which you want the syncronization process to happen (indicated in seconds)

## Example of running it

1 - Create the environment and install the dependencies

```
python3 -m venv venv
source venv/bin/activate # if you're on mac/linux
env\Scripts\activate # if you're on windows
pip3 install -r requirements.txt
```

2 - Run the tests to ensure the program is working correctly in the environment:

```
pytest
```

3 - With all tests being run ok, here's a example on how to run the program(make sure the source directory exists):
```
python3 main.py --source /Users/user/test1 --replica /Users/user/test2 --log_folder /Users/user/logs/log_test.log --interval 30
```

Make sure to replace the folders paths:

- `/Users/user/test1`: A directory you have on your disk, with files and subdirectories you want to synchronize in another directory.
- `/Users/user/test2`: An existing directory or a path to one, where you want your source folder to be replicated.
- `/Users/user/logs/log_test.log`: A path to the file you want your logs to go to.
- `30`: The time interval in seconds you want the synchronization process to happen.


## Licence

This repository is under the MIT License.