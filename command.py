# -*- coding: utf-8 -*-
# @Author  : JonathanLai
# @Time    : 7/19/23 8:54 AM
# @File    : command.py

def handle_command():
    command = input("Enter a command: ")
    command_parts = command.split()

    if command == "exit":
        exit()
    elif command == "help":
        pass
    elif command_parts[0] == "pump":
        x = int(command_parts[1])
        y = int(command_parts[2])
        state = 0
        if (command_parts[3] == "on") or (command_parts[3] == "1"):
            state = 1
        return x, y, state
