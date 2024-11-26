#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Whiteboard
#  Created by Ingenuity i/o on 2024/10/18
#

import sys
import ingescape as igs

#inputs
def input_callback(io_type, name, value_type, value, my_data):
    pass
    # add code here if needed

def service_callback(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    pass
    # add code here if needed

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python3 main.py agent_name network_device port")
        devices = igs.net_devices_list()
        print("Please restart with one of these devices as network_device argument:")
        for device in devices:
            print(f" {device}")
        exit(0)

    igs.agent_set_name(sys.argv[1])
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.debug(f"Ingescape version: {igs.version()} (protocol v{igs.protocol()})")

    igs.input_create("title", igs.STRING_T, None)
    igs.input_create("backgroundColor", igs.STRING_T, None)
    igs.input_create("labelsVisible", igs.BOOL_T, None)
    igs.input_create("chatMessage", igs.STRING_T, None)
    igs.input_create("clear", igs.IMPULSION_T, None)
    igs.input_create("ui_command", igs.STRING_T, None)

    igs.output_create("lastChatMessage", igs.STRING_T, None)
    igs.output_create("lastAction", igs.STRING_T, None)
    igs.output_create("ui_error", igs.STRING_T, None)

    igs.observe_input("title", input_callback, None)
    igs.observe_input("backgroundColor", input_callback, None)
    igs.observe_input("labelsVisible", input_callback, None)
    igs.observe_input("chatMessage", input_callback, None)
    igs.observe_input("clear", input_callback, None)
    igs.observe_input("ui_command", input_callback, None)

    igs.service_init("chat", service_callback, None)
    igs.service_arg_add("chat", "message", igs.STRING_T)
    igs.service_init("snapshot", service_callback, None)
    igs.service_init("clear", service_callback, None)
    igs.service_init("showLabels", service_callback, None)
    igs.service_init("hideLabels", service_callback, None)
    igs.service_init("addShape", service_callback, None)
    igs.service_arg_add("addShape", "type", igs.STRING_T)
    igs.service_arg_add("addShape", "x", igs.DOUBLE_T)
    igs.service_arg_add("addShape", "y", igs.DOUBLE_T)
    igs.service_arg_add("addShape", "width", igs.DOUBLE_T)
    igs.service_arg_add("addShape", "height", igs.DOUBLE_T)
    igs.service_arg_add("addShape", "fill", igs.STRING_T)
    igs.service_arg_add("addShape", "stroke", igs.STRING_T)
    igs.service_arg_add("addShape", "strokeWidth", igs.DOUBLE_T)
    igs.service_init("addText", service_callback, None)
    igs.service_arg_add("addText", "text", igs.STRING_T)
    igs.service_arg_add("addText", "x", igs.DOUBLE_T)
    igs.service_arg_add("addText", "y", igs.DOUBLE_T)
    igs.service_arg_add("addText", "color", igs.STRING_T)
    igs.service_init("addImage", service_callback, None)
    igs.service_arg_add("addImage", "base64", igs.DATA_T)
    igs.service_arg_add("addImage", "x", igs.DOUBLE_T)
    igs.service_arg_add("addImage", "y", igs.DOUBLE_T)
    igs.service_arg_add("addImage", "width", igs.DOUBLE_T)
    igs.service_arg_add("addImage", "height", igs.DOUBLE_T)
    igs.service_init("addImageFromUrl", service_callback, None)
    igs.service_arg_add("addImageFromUrl", "url", igs.STRING_T)
    igs.service_arg_add("addImageFromUrl", "x", igs.DOUBLE_T)
    igs.service_arg_add("addImageFromUrl", "y", igs.DOUBLE_T)
    igs.service_init("remove", service_callback, None)
    igs.service_arg_add("remove", "elementId", igs.INTEGER_T)
    igs.service_init("translate", service_callback, None)
    igs.service_arg_add("translate", "elementId", igs.INTEGER_T)
    igs.service_arg_add("translate", "dx", igs.DOUBLE_T)
    igs.service_arg_add("translate", "dy", igs.DOUBLE_T)
    igs.service_init("moveTo", service_callback, None)
    igs.service_arg_add("moveTo", "elementId", igs.INTEGER_T)
    igs.service_arg_add("moveTo", "x", igs.DOUBLE_T)
    igs.service_arg_add("moveTo", "y", igs.DOUBLE_T)
    igs.service_init("setStringProperty", service_callback, None)
    igs.service_arg_add("setStringProperty", "elementId", igs.INTEGER_T)
    igs.service_arg_add("setStringProperty", "property", igs.STRING_T)
    igs.service_arg_add("setStringProperty", "value", igs.STRING_T)
    igs.service_init("setDoubleProperty", service_callback, None)
    igs.service_arg_add("setDoubleProperty", "elementId", igs.INTEGER_T)
    igs.service_arg_add("setDoubleProperty", "property", igs.STRING_T)
    igs.service_arg_add("setDoubleProperty", "value", igs.DOUBLE_T)
    igs.service_init("getElementIds", service_callback, None)
    igs.service_init("getElements", service_callback, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()

    igs.stop()

