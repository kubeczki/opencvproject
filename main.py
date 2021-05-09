from rt_system_std import system_std
from rt_system_alt import system_alt
import sys


def choose_system_version(version):
    if version == "std":
        system_std()
    elif version == "alt":
        system_alt()
    else:
        print("Unrecognized version. Try std or alt")


if __name__ == '__main__':
    sys_version = sys.argv[1]

    choose_system_version(sys_version)
    # system_alt()
    # system_std()
    sys.exit()
