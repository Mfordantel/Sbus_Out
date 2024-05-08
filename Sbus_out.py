import random
import serial

class SBUSTransmitter:
    def __init__(self, _uart_port):
        self.ser = serial.Serial(
            port=_uart_port,
            baudrate=100000,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.EIGHTBITS,
            timeout=0,
        )
        self.sbus_packet = bytearray([0] * 25)
        self.sbus_packet[0] = 0x0F
        self.sbus_packet[23] = 0x00
        self.sbus_packet[24] = 0x00
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

    def decode_sbus_packet(self, sbus_packet):
        channels = [0] * 16
        for i in range(16):
            byte_index = 1 + (i * 11 // 8)
            bit_index = (i * 11) % 8
            channels[i] = (sbus_packet[byte_index] | (sbus_packet[byte_index + 1] << 8) | (sbus_packet[byte_index + 2] << 16)) >> bit_index & 0x07FF
        return channels

    def encode_sbus_packet(self, value):
        for i in range(16):
            byte_index = 1 + (i * 11 // 8)
            bit_index = (i * 11) % 8
            self.sbus_packet[byte_index] |= ((value[i] & 0x07FF) << bit_index) & 0xFF
            self.sbus_packet[byte_index + 1] |= ((value[i] & 0x07FF) << bit_index) >> 8 & 0xFF
            if bit_index >= 6 and i < 15:
                self.sbus_packet[byte_index + 2] |= ((value[i] & 0x07FF) << bit_index) >> 16 & 0xFF

    def transmit_sbus_packet(self, value):
        print(f"SBUS-пакет до кодирования: {value}")
        self.encode_sbus_packet(value)
        print(f"SBUS-пакет после кодирования: {self.sbus_packet}")
        self.ser.write(self.sbus_packet)

def generate_random_sbus_packet():
    packet = []
    for _ in range(16):
        packet.append(random.randint(172, 1811))
    return packet

if __name__ == '__main__':
    sbus_transmitter = SBUSTransmitter('/dev/ttyS0')  # Замените на соответствующий путь к порту UART0

    while True:
        random_sbus_packet = generate_random_sbus_packet()
        sbus_transmitter.transmit_sbus_packet(random_sbus_packet)