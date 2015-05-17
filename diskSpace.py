import ctypes
import platform
import os


class HardDriveSpaceException(Exception):
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


def get_free_space(folder, format="MB"):
    """ 
        Return folder/drive free space 
    """
    fConstants = {"GB": 1073741824,
                  "MB": 1048576,
                  "KB": 1024,
                  "B": 1
                  }
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        total_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, ctypes.pointer(total_bytes),
                                                   ctypes.pointer(free_bytes))
        return int(free_bytes.value / fConstants[format.upper()]), int(
            total_bytes.value / fConstants[format.upper()]), format
    else:
        return int(os.statvfs(folder).f_bfree * os.statvfs(folder).f_bsize / fConstants[format.upper()]), format


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
