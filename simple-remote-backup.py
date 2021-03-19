# simple-remote-backup.py - v1
#
# Used to backup Windows Shares to a Air-Gapped Removable Drive
# Does not do encryption or compression

import os, shutil, datetime;

# Simple Month tracker for datetime
months = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"};

# Update this: Supply a database-key (can be anything),
# the path you will copy from and and the folder you will copy to
# This was made to backup to a removable drive, so it wasn't created properly
# Can probably just put in the full destination and alter the destination variable
# further down to remedy this issue.
database = {"database-key-1":
           {"source": r"Source-Folder",
           "destination": r"Destination-Folder"},
           "database-key-2":
           {"source": r"Source-Folder",
           "destination": "Destination-Folder"}
           };

# Gets Current month to backup into
currentMonth = int("{date}".format(date=datetime.date.today()).split("-")[1])
for thisMonth in months.items():
    if currentMonth == thisMonth[0]:
        currentMonth = thisMonth[1];
        break;

# Simple shutil data copy with an exception handler
def backup(src, dst):
    for dataset in database.items():
        try:
            shutil.copytree(src, dst, copy_function=shutil.copy2, dirs_exist_ok=True);
        except Exception as err:
            print("An error has occured: %s" % err);
            continue;

if __name__ == "__main__":
    driveLetter = r"E:" # change this
    for dataset in database.items():
        # Can update this to make it proper
        destination = r"{drive}\{data}\{month}".format(drive=driveLetter, data=database[dataset[0]]["destination"], month=currentMonth);
        if os.path.exists(destination):
            database[dataset[0]]["destination"] = destination;
            backup(database[dataset[0]]["source"], destination);
