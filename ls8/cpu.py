"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0b00000000] * 8
        # 1 in binary for halt
        self.hlt = 0b00000001
        # pointer counter
        self.pc = 0
        # Instruction Register
        self.ram = []
        self.ir = 0b00000000
        self.mar = 0b00000000
        self.mdr = 0b00000000
        self.flags = 0b00000000
        self.ldi = 0b10000010
        self.prn = 0b01000111
        self.mult = 0b10100010
    def load(self, file_name):

        with open(file_name,'r') as fh:
            all_lines = fh.readlines()
        code = []
        for line in all_lines:
            processed_line = line.split(' ')[0]
            if processed_line != '#' and processed_line != '\n':
                code.append(int(processed_line, 2))
        self.ram = code
    def ram_read(self, MAR):
        MDR = self.ram[MAR]
        return MDR

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MULT":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        print('start cpu')
        while True:
            opcode = self.ram[self.pc]
            self.ir = opcode
            if opcode == self.hlt:
                break
            elif opcode == self.ldi:
                register = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.reg[register] = value
                self.pc += 2
            elif opcode == self.prn:
                register = self.ram[self.pc +1]
                print(self.reg[register])
                self.pc += 1
            elif opcode == self.mult:
                registerA = self.ram[self.pc + 1]
                registerB = self.ram[self.pc + 2]
                self.alu("MULT", registerA, registerB)
                self.pc += 2
            else:
                print(f'{opcode} is an invalid opcode')
                break
            self.pc += 1


