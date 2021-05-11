from rt_system_std import system_std
from rt_system_alt import system_alt
from rt_system_sampling import system_sampling
import sys
import time
from logger import log


def choose_system_version(version, file_name):
    if version == "std":
        log(time.asctime(), "choose_system_version;", "Standard version has been activated")
        log(time.asctime(), "choose_system_version;", "Standard version has been activated", "Delay.txt")
        log(time.asctime(), "choose_system_version;", "Standard version has been activated", "Process Duration.txt")
        system_std(file_name)
    elif version == "alt":
        log(time.asctime(), "choose_system_version;", "Alternate version has been activated")
        log(time.asctime(), "choose_system_version;", "Alternate version has been activated", "Delay.txt")
        log(time.asctime(), "choose_system_version;", "Alternate version has been activated", "Process Duration.txt")
        system_alt(file_name)
    elif version == "par":
        log(time.asctime(), "choose_system_version;", "Parallel version has been activated")
        log(time.asctime(), "choose_system_version;", "Parallel version has been activated", "Delay.txt")
        log(time.asctime(), "choose_system_version;", "Parallel version has been activated", "Process Duration.txt")
        system_sampling(1, file_name)
    elif version == "samp":
        while True:
            try:
                sampling_step = int(input("Sampling step (positive integer): "))
                if int(sampling_step) == sampling_step and sampling_step > 0:
                    log(time.asctime(), "choose_system_version;", "Sampling version has been activated")
                    log(time.asctime(), "choose_system_version;", "Sampling version has been activated", "Delay.txt")
                    log(time.asctime(), "choose_system_version;", "Sampling version has been activated", "Process Duration.txt")
                    system_sampling(sampling_step, file_name)
                    break
            except:
                print("Sampling step must be a positive integer!")
                continue
            print("Sampling step must be a positive integer!")
    else:
        print("Unrecognized version. Try std, alt, par or samp")


if __name__ == '__main__':

    sys_version = sys.argv[1]
    if len(sys.argv) == 2:
        filename = "no_filename"
    else:
        filename = sys.argv[2]

    choose_system_version(sys_version, filename)

    sys.exit()
