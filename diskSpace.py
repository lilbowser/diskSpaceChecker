import ctypes
import platform
import os
import win32api


class HardDriveSpaceException(Exception):
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


def get_free_space(folder, units="MB"):
    """
        Return folder/drive free space
        :rtype: (int, int, str)
        :type folder: str
    """

    u_constants = get_byte_unit_const(units)
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        total_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, ctypes.pointer(total_bytes),
                                                   ctypes.pointer(free_bytes))
        return int(free_bytes.value / u_constants), int(
            total_bytes.value / u_constants), units
    else:
        return int(os.statvfs(folder).f_bfree * os.statvfs(folder).f_bsize / u_constants), units


def get_byte_unit_const(units="MB"):
    unit_const = {"GB": 1073741824,
                  "MB": 1048576,
                  "KB": 1024,
                  "B": 1
                  }
    return unit_const[units.upper()]


def get_available_disks(only_real_drives=True):
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split("\x00")

    if only_real_drives: 
        real_drives = []
        for drive in drives:
            if os.path.isdir(drive):  # if drive is a directory
                real_drives.append(drive)
        if not real_drives:
            return drives  # if real_drives is empty, lets return drives to prevent any problems.
        else:
            return real_drives

    else:
        return drives


if __name__ == "__main__":
    try:
        byteFormat = "mb"
        size = get_free_space(r"c:", byteFormat)
        print size
        if size[0] < 10000000000:
            raise HardDriveSpaceException(
                "Hard drive space limit reached, there is only %s %s space left." % (size[0], size[1]))
    except HardDriveSpaceException as e:
        print e
