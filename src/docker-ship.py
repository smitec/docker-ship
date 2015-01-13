#!/usr/bin/env python

import json
import sys
import os
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

def set_command(command, cmd):
    command[u'command'] = cmd

def map_port(command, src, dest):
    command[u'args'] += ['-p ' + str(src) + ':' + str(dest)]

def port_mapping(command, ports):
    for s,d in ports:
        map_port(command, s, d)

def link_container(command, src, dest):
    command[u'args'] += ['--link ' + src + ':' + dest]

#TODO: this is basically the port mapping function...
def container_linking(command, links):
    for s,d in links:
        link_container(command, s, d)

COMMAND_SET = {
    u'image': set_image,
    u'name': set_name,
    u'detached': set_detached,
    u'tty': set_tty,
    u'interactive': set_interactive,
    u'command': set_command,
    u'ports': port_mapping,
    u'link': container_linking,
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
    #TODO: investigate how to move sudo outside of here
    base_command = {u'start':"sudo docker run", u'args':[], u'image':'', u'cmd':''}
    for k in inst.keys():
        if k in COMMAND_SET.keys():
            COMMAND_SET[k](base_command, inst[k])
        else:
            print("Bad command: ", k)
    final_command = base_command[u'start'] + " " +  " ".join(base_command[u'args']) + \
        " " + base_command[u'image'] + " " + base_image[u'cmd']
    print("Running: " + final_command)
    os.system(final_command)

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
