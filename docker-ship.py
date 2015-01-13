import json
import sys

# Valid Commands
def set_image(command, imagename):
    command[u'image'] = imagename

def set_name(command, name):
    command[u'args'] += ['--name ' + name]

def set_flag(command, f):
    command[u'args'] += ['-' + f]

def set_tty(command, b):
    if b:
        set_flag(command, 't')

def set_interactive(command, b):
    if b:
        set_flag(command, 'i')

def set_detached(command, b):
    if b:
        set_flag(command, 'd')

COMMAND_SET = {
    u'image': set_image,
    u'name': set_name,
    u'detached': set_detached,
    u'tty': set_tty,
    u'interactive': set_interactive,
}

# Helper functions

def print_help():
    message = (
        "usage: docker-ship runfile \n"
        "runfile is a file containing JSON.\n"
        "each instance should be formatted as:-\n"
        "instance {\n"
        "   image: nginx-test,\n"
        "   name: ng,\n"
        "}"
        "\nBetter docs coming, promise"
    )
    print(message)   

def validate_and_run(inst):
    base_command = {u'start':"docker run", u'args':[], u'image':''}
    for k in inst.keys():
        if k in COMMAND_SET.keys():
            COMMAND_SET[k](base_command, inst[k])
        else:
            print("Bad command: ", k)
    final_command = base_command[u'start'] + " " +  " ".join(base_command[u'args']) + " " + base_command[u'image']
    print(final_command)

def launch_instance(filename):
    try:
        f = open(filename, 'r')
        data = json.load(f)
        # validate and run each instance
        for inst in data:
            validate_and_run(inst)
        f.close()
    except IOError:
        print("Cannot open or read, ", filename, ", skipping.")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print_help()
    else:
        for i in range(1,len(sys.argv)):
            launch_instance(sys.argv[i])
