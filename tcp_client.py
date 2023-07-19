# -*- coding:utf-8 -*-
# Time : 2023-07-14 15:12
# Author: JKP
# File : tcp_client.py

import socket
import struct
from system import PumpSystem


class TCPClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.datas_format = "BBBBBBBBBBBBBBBBBBBB"
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def send_message(self, data_transmit):
        # Modify the method
        # data_transmit = [0x55, 0x88,
        #                  0x00, 0x00, 0x00, 0x00,  # 1 layer
        #                  0x00, 0x00, 0x00, 0x00,  # 2 layer
        #                  0x00, 0x00, 0x00, 0x00,  # 3 layer
        #                  0x00, 0x00, 0x00, 0x00,  # 4 layer
        #                  0x99, 0x19]
        data_package = struct.pack(self.datas_format, *data_transmit)
        # print(data_package)
        self.client_socket.send(data_package)


if __name__ == "__main__":
    client = TCPClient("localhost", 8000)
    pump = PumpSystem()

    # test: open pump 3, 3; board 1, 23
    pump.pos_transfer(3, 3, 1)

    client.send_message(pump.data_transmit)
