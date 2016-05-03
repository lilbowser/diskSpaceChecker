#! python3

# Library for finding the total and remaining disk space of a drive.
# Copyright AGoldfarb April 2016

import ctypes
import platform
import os
import win32api

__version__ = "0.1.1"

class HardDriveSpaceException(Exception):
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


def get_free_space(folder, units="MB"):
    """
        Return folder/drive free space (Free Space, total space, units)

        :type folder: str
        :return: A Dict with items: units, bytes_per_unit, folder, free, total
        :rtype: dict
    """

    u_constants = get_byte_unit_def(units)
    disk_info = {
        'units': units,
        'bytes_per_unit': u_constants,
        'folder': folder
    }

    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        total_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, ctypes.pointer(total_bytes),
                                                   ctypes.pointer(free_bytes))

        disk_info['free'] = int(free_bytes.value / u_constants)
        disk_info['total'] = int(total_bytes.value / u_constants)

        # return int(free_bytes.value / u_constants), int(total_bytes.value / u_constants), units
        return disk_info
    else:
        disk_info['free'] = int(os.statvfs(folder).f_bfree * os.statvfs(folder).f_bsize / u_constants)
        disk_info['total'] = int(os.statvfs(folder).f_blocks * os.statvfs(folder).f_bsize / u_constants)

        # return int(os.statvfs(folder).f_bfree * os.statvfs(folder).f_bsize / u_constants), units
        return disk_info


def get_byte_unit_def(units="MB"):
    """
    Input: Units(str). Returns const based on input.
    :param units:
    :return:
    """
    unit_const = {"GB": 1073741824,
                  "MB": 1048576,
                  "KB": 1024,
                  "B": 1
                  }
    return unit_const[units.upper()]


def get_available_disks(only_real_drives=True, minimum_drive_size=0):
    """
    Returns a list of disk drives on the system
    First input control whether all drives are listed, or just writeable drives. (Default is only writeable.)
    Second input controls the minimum size a drive must be (In GB). 0 turns this off. (Default is 0.)

    @type minimum_drive_size: int
    @type only_real_drives: bool
    @rtype: list[drives]
    """

    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split("\x00")

    if only_real_drives:
        real_drives = []
        for drive in drives:
            if os.path.isdir(drive):  # if drive is a directory
                 real_drives.append(drive)
        if not real_drives:
            pass  # if real_drives is empty, lets return drives to prevent any problems.
        else:
            drives = real_drives

    if minimum_drive_size > 0:
        large_drive = []
        minimum_drive_size *= get_byte_unit_def("GB")
        for drive in drives:
            (free, total, units) = get_free_space(drive, "B")
            if total > minimum_drive_size:
                large_drive.append(drive)
        if not large_drive:
            pass
        else:
            drives = large_drive
    return drives


if __name__ == "__main__":
    try:
        byteFormat = "mb"
        size = get_free_space(r"c:", byteFormat)
        print(size)
        if size[0] < 10000000000:
            raise HardDriveSpaceException(
                "Hard drive space limit reached, there is only %s %s space left." % (size[0], size[1]))
    except HardDriveSpaceException as e:
        print(e)
