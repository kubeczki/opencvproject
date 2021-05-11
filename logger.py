def log(current_time, current_process, info, file_name="Log.txt"):
    output = open(file_name, "a")
    output.write("[")
    output.write(current_time)
    output.write("]")
    output.write(" ")
    output.write(current_process)
    output.write(" ")
    output.write(info)
    output.write("\n")
    output.close()


def log_delay(frame_number, time):
    output = open("Delay.txt", "a")
    output.write("Frame number: ")
    output.write(str(frame_number))
    output.write(" time of processing single frame: ")
    output.write("{:.4f}".format(time))
    output.write(" s")
    output.write("\n")
    output.close()


def log_process_duration(process_name, time):
    output = open("Process Duration.txt", "a")
    output.write("Process: ")
    output.write(process_name)
    output.write(" time of single iteration: ")
    output.write("{:.4f}".format(time))
    output.write(" s")
    output.write("\n")
    output.close()

