from rt_system_std import system_std
from rt_system_alt import system_alt
from rt_system_sampling import system_sampling
import sys
import time
from logger import log


def choose_system_version(version, file_name):
    resolution_number = int(input("Choose preferred resolution: \n1. 720p\n2. 480p\n3. 360p\n4. 144p\n"))
    if resolution_number == 1:
        resolution = [1280, 720]
    elif resolution_number == 2:
        resolution = [640, 480]
    elif resolution_number == 3:
        resolution = [480, 360]
    elif resolution_number == 4:
        resolution = [256, 144]
    else:
        print("Wrong input, default resolution chosen (720p)")
        resolution = [1280, 720]

    if version == "std":
        log(time.asctime(), "choose_system_version;", "Standard version has been activated")
        log(time.asctime(), "choose_system_version;", "Standard version has been activated", "Delay.txt")
        log(time.asctime(), "choose_system_version;", "Standard version has been activated", "Process Duration.txt")
        system_std(file_name, resolution)
    elif version == "alt":
        log(time.asctime(), "choose_system_version;", "Alternate version has been activated")
        log(time.asctime(), "choose_system_version;", "Alternate version has been activated", "Delay.txt")
        log(time.asctime(), "choose_system_version;", "Alternate version has been activated", "Process Duration.txt")
        system_alt(file_name, resolution)
    elif version == "par":
        log(time.asctime(), "choose_system_version;", "Parallel version has been activated")
        log(time.asctime(), "choose_system_version;", "Parallel version has been activated", "Delay.txt")
        log(time.asctime(), "choose_system_version;", "Parallel version has been activated", "Process Duration.txt")
        system_sampling(1, file_name, resolution)
    elif version == "samp":
        while True:
            try:
                sampling_step = int(input("Sampling step (positive integer): "))
                if int(sampling_step) == sampling_step and sampling_step > 0:
                    log(time.asctime(), "choose_system_version;", "Sampling version has been activated")
                    log(time.asctime(), "choose_system_version;", "Sampling version has been activated", "Delay.txt")
                    log(time.asctime(), "choose_system_version;", "Sampling version has been activated", "Process Duration.txt")
                    system_sampling(sampling_step, file_name, resolution)
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
