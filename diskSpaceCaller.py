__author__ = 'Josh'
import diskSpace
# import win32api
import os
#
# drives = win32api.GetLogicalDriveStrings()
# drives = drives.split("\x00")
drives = diskSpace.get_available_disks(True)
for drive in drives:
    # drive = drive.strip('\\')
    # drive = drive.lower()
    print drive
    print os.path.isdir(drive)
    print (diskSpace.get_free_space(drive, "GB"))
raw_input("End")
