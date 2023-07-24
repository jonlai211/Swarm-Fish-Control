# -*- coding: utf-8 -*-
# @Author  : JonathanLai
# @Time    : 7/17/23 2:44 PM
# @File    : system.py
from command import handle_command


class PumpSystem:
    def __init__(self):
        self.pump_state = [[0] * 10 for _ in range(10)]  # 10 * 10 pumps
        self.board_state = [[0] * 25 for _ in range(4)]  # 4 layers * 25 pumps
        self.data_transmit = [0x55, 0x88] + [0x00] * 16 + [0x99, 0x19]
        # self.data_transmit = [0x55, 0x88,
        #                       0x00, 0x00, 0x00, 0x00,  # 1 layer
        #                       0x00, 0x00, 0x00, 0x00,  # 2 layer
        #                       0x00, 0x00, 0x00, 0x00,  # 3 layer
        #                       0x00, 0x00, 0x00, 0x00,  # 4 layer
        #                       0x99, 0x19]

    # poor algorithm
    def update_data_transmit(self, board_layer, board_index, state):
        byte_index = 2 + (board_layer + 1) * 4 - (board_index // 8 + 1)
        bit_index = board_index % 8 + 1
        bit_num = bin(self.data_transmit[byte_index])[2:].zfill(8)
        bit_num_new = bit_num[:-bit_index] + str(state) + bit_num[len(bit_num) - bit_index + 1:]
        self.data_transmit[byte_index] = int(bit_num_new, 2)

    def pos_transfer(self, x, y, state):
        index = (x - 1) * 10 + y
        board_index = (index - 1) % 25
        board_layer = (index - 1) // 25
        self.update_data_transmit(board_layer, board_index, state)

    def motor_status_show(self):
        for board_layer in range(4):
            data_transmit_binary = [bin(value)[2:].zfill(8) for value in
                                    self.data_transmit[2 + board_layer * 4:6 + board_layer * 4]]
            self.board_state[board_layer] = [int(bit[-1]) for bit in ''.join(data_transmit_binary)[-25:]]
            print(board_layer + 1, "board layer:", self.board_state[board_layer])

    def pump_status_show(self):
        for board_layer in range(4):
            data_transmit_binary = [bin(value)[2:].zfill(8) for value in
                                    self.data_transmit[2 + board_layer * 4:6 + board_layer * 4]]
            self.board_state[board_layer] = [int(bit[-1]) for bit in ''.join(data_transmit_binary)[-25:]]

        for board_layer in range(4):
            for board_index in range(24, -1, -1):
                index = board_layer * 25 + (24 - board_index)
                x = index // 10
                y = index % 10
                self.pump_state[x][y] = self.board_state[board_layer][board_index]
        print("pump status:")
        for row in self.pump_state:
            print(" ".join(str(element) for element in row))


if __name__ == "__main__":
    pump = PumpSystem()

    # test
    # pump.pos_transfer(8, 4, 1)
    #
    # pump.motor_status_show()
    # pump.pump_status_show()

    while True:
        x, y, state = handle_command()
        pump.pos_transfer(x, y, state)

        pump.motor_status_show()
        pump.pump_status_show()
