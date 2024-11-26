#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  achat
#  Created by Ingenuity i/o on 2024/10/18
#

import sys
import ingescape as igs

#inputs
def input_callback(io_type, name, value_type, value, my_data):
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

    igs.input_create("argent", igs.IMPULSION_T, None)
    igs.input_create("prix", igs.IMPULSION_T, None)

    igs.output_create("ordre", igs.IMPULSION_T, None)

    igs.observe_input("argent", input_callback, None)
    igs.observe_input("prix", input_callback, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()

    igs.stop()

