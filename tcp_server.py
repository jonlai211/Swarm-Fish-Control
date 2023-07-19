# -*- coding:utf-8 -*-
# Time : 2023-07-14 15:13
# Author: JKP
# File : tcp_server.py

import socket
import struct
import time
import serial


class TCPServer:
    def __init__(self, host, port, serial_port, serial_baudrate):
        self.host = host
        self.port = port
        self.serial_port = serial_port
        self.baudrate = serial_baudrate
        self.package_head = 0xFE
        self.board_1 = 0x01
        self.board_2 = 0x02
        self.board_3 = 0x03
        self.board_4 = 0x04

        self.ser = serial.Serial(self.serial_port, self.baudrate)
        self.ser_format = ">BBBBBBH"

        self.datas_format = "BBBBBBBBBBBBBBBBBBBB"
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"Server started on {self.host}:{self.port}")

    def listen(self):
        while self.ser.isOpen():
            try:
                client_socket, address = self.server_socket.accept()
                print(f"Connection from {address[0]}:{address[1]}")
                while client_socket:
                    package_head_data = client_socket.recv(1024)
                    data = list(struct.unpack(self.datas_format, package_head_data))
                    if data:
                        board_1_encode = self.CRC16(self.board_1, data[2:6])
                        board_1_contents = [self.package_head, self.board_1] + data[2:6] + [board_1_encode]
                        print(board_1_contents)
                        package_board_1 = struct.pack(self.ser_format, *board_1_contents)
                        self.ser.write(package_board_1)
                        time.sleep(0.025)

                        board_2_encode = self.CRC16(self.board_2, data[6:10])
                        board_2_contents = [self.package_head, self.board_2] + data[6:10] + [board_2_encode]
                        print(board_2_contents)
                        package_board_2 = struct.pack(self.ser_format, *board_2_contents)
                        self.ser.write(package_board_2)
                        time.sleep(0.025)

                        board_3_encode = self.CRC16(self.board_3, data[10:14])
                        board_3_contents = [self.package_head, self.board_3] + data[10:14] + [board_3_encode]
                        print(board_3_contents)
                        package_board_3 = struct.pack(self.ser_format, *board_3_contents)
                        self.ser.write(package_board_3)
                        time.sleep(0.025)

                        board_4_encode = self.CRC16(self.board_4, data[14:18])
                        board_4_contents = [self.package_head, self.board_4] + data[14:18] + [board_4_encode]
                        print(board_4_contents)
                        package_board_4 = struct.pack(self.ser_format, *board_4_contents)
                        self.ser.write(package_board_4)

            except Exception as e:
                print("Exception: ", e)
        client_socket.close()

    def CRC16(self, board_ID, datas):
        crc16 = 0xFFFF
        poly = 0xA001
        datas_handle = [self.package_head, board_ID] + datas
        for data in datas_handle:
            a = int(data)
            crc16 = a ^ crc16
            for i in range(8):
                if 1 & (crc16) == 1:
                    crc16 = crc16 >> 1
                    crc16 = crc16 ^ poly
                else:
                    crc16 = crc16 >> 1
        return int(crc16)


if __name__ == "__main__":
    # Change port and baudrate to match device
    server = TCPServer("localhost", 8000, "/dev/ttyUSB0", 115200)
    server.listen()
