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
        self.branch_table = {
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b10100010: self.mult,
            0b10100000: self.add,
            0b01000110: self.pop,
            0b01000101: self.push,
        }
        self.interrupt_mask = 5
        self.interrupt_status = 6
        self.stack_pointer = 7
    def load(self, file_name):

        with open(file_name,'r') as fh:
            all_lines = fh.readlines()
        code = []
        for line in all_lines:
            processed_line = line.split(' ')[0]
            if processed_line != '#' and processed_line != '\n':
                code.append(int(processed_line, 2))
        self.ram = code
        print(self.ram)
        for i, line in enumerate(code):
            self.ram[i] = line
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
    def add(self):
        registerA = self.ram[self.pc + 1]
        registerB = self.ram[self.pc + 2]
        self.alu("ADD", registerA, registerB)
        self.pc += 2
    def ldi(self):
        register = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.reg[register] = value
        self.pc += 2
    def prn(self):
        register = self.ram[self.pc + 1]
        print(self.reg[register])
        self.pc += 1
    def mult(self):
        registerA = self.ram[self.pc + 1]
        registerB = self.ram[self.pc + 2]
        self.alu("MULT", registerA, registerB)
        self.pc += 2
    def push(self):
        register = self.ram[self.pc + 1]
        val = self.reg[register]
        self.stack_pointer -= 1
        self.ram[self.stack_pointer] = val
        self.pc += 1
    def pop(self):
        register = self.ram[self.pc + 1]
        val = self.ram[self.stack_pointer]
        self.reg[register] = val
        self.stack_pointer += 1
        self.pc += 1
    def run(self):
        """Run the CPU."""
        print('start cpu')
        while True:
            opcode = self.ram[self.pc]
            self.ir = opcode
            if opcode == self.hlt:
                break
            elif opcode in self.branch_table:
                self.branch_table[opcode]()
            else:
                print(f'{opcode} is an invalid opcode')
                break
            self.pc += 1


