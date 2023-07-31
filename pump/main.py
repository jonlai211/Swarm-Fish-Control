# -*- coding: utf-8 -*-
# @Author  : JonathanLai
# @Time    : 7/17/23 3:04 PM
# @File    : main.py

import threading
from tcp_server import TCPServer
from tcp_client import TCPClient
from system import PumpSystem
from command import handle_command


def run_server():
    server = TCPServer("localhost", 8000, "/dev/ttyUSB0", 115200)
    try:
        server.listen()
    finally:
        server.server_socket.close()


def run_client():
    client = TCPClient("localhost", 8000)
    pump_pos = PumpSystem()
    try:
        handle_command()
        client.send_message(pump_pos.data_transmit)
    finally:
        client.client_socket.close()


if __name__ == "__main__":
    # TODO: Fix threading construction problems
    server_thread = threading.Thread(target=run_server)
    client_thread = threading.Thread(target=run_client)

    server_thread.start()
    client_thread.start()

    server_thread.join()
    client_thread.join()
