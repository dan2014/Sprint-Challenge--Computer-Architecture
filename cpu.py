"""CPU functionality."""

import sys
import time
import re

class CPU:
    """Main CPU class."""

    def __init__(self,sleep=0):
        """Construct a new CPU."""
        self.sleep = sleep
        self.ram = [0] * 256
        self.pc = 0b00000000
        self.reg = [0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,0b00000000]
        self.ir = 0b00000000
        self.fl = 0b00000000
        self.branchtable = {}
        self.branchtable["ALU"] = self.handle_ALU
        self.branchtable["PC"] = self.handle_PC
        self.branchtable["OTHER"] = self.handle_OTHER

    def get_operands(self,operand_num):
        operands = []
        if operand_num > 0:
            for _ in range(operand_num):
                self.pc += 1
                operand = self.ram_read(self.pc)
                operands.append(operand)
        # address = self.pc
        # opt_code = self.ram_read(address)
        # self.ir = opt_code

        return operands


    def handle_ALU(self,operand,ins):
        alu_ops = {0b0000:("ADD",self.ADD),0b0001:("SUB",self.SUB),0b0010:("MUL",self.MUL),0b0011:("DIV",self.DIV),0b0100:("MOD",self.MOD),0b0101:("INC",self.INC),0b0110:("DEC",self.DEC),0b0111:("CMP",self.CMP),0b1000:("AND",self.AND),0b1001:("NOT",self.NOT),0b1010:("OR",self.OR),0b1011:("XOR",self.XOR),0b1100:("SHL",self.SHL),0b1101:("SHR",self.SHR)}

        operands = self.get_operands(operand)
        alu_ops[ins][1](*operands)
    
    def handle_PC(self,operand,ins):
        pc_ops = {0b0000:("CALL",self.CALL),0b0001:("RET",self.RET),0b0010:("INT",self.INT),0b0011:("IRET",self.IRET),0b0100:("JMP",self.JMP),0b0101:("JEQ",self.JEQ),0b0110:("JNE",self.JNE),0b0111:("JGT",self.JGT),0b1000:("JLT",self.JLT),0b1001:("JLE",self.JLE),0b1010:("JGE",self.JGE)}
        operands = self.get_operands(operand)
        pc_ops[ins][1](*operands)
        

    def handle_OTHER(self,operand,ins):
        other_ops = {0b0000:("NOP",self.NOP),0b0001:("HLT",self.HLT),0b0010:("LDI",self.LDI),0b0011:("LD",self.LD),0b0100:("ST",self.ST),0b0101:("PUSH",self.PUSH),0b0110:("POP",self.POP),0b0111:("PRN",self.PRN),0b1000:("PRA",self.PRA)}

        operands = self.get_operands(operand)
        other_ops[ins][1](*operands)

    def ram_read(self,address):
        return self.ram[address]

    def ram_write(self):
        pass


    def load(self,args):
        """Load a program into memory."""

        address = 0

        if len(args) != 2:
            print("usage: file.py <filename>", file=sys.stderr)
            sys.exit(1)

        filepath = args[1]
        program = []
        try:
            with open(filepath) as f:
                for line in f:
                    m = re.compile("[0-1]{8}",)
                    match = m.search(line)
                    if match is not None:
                        instruction = int(match.group(),2)
                        program.append(instruction)
                    
        except FileNotFoundError:
            print(f"{args[0]}: {args[1]} not found")
            sys.exit(2)


        for instruction in program:
            self.ram[address] = instruction
            address += 1


    # def alu(self, op, reg_a, reg_b):
    #     """ALU operations."""
    #     if op == "ADD":
    #         self.reg[reg_a] += self.reg[reg_b]
    #     #elif op == "SUB": etc
    #     else:
    #         raise Exception("Unsupported ALU operation")

        # SET FL Register

    def cu(self):
        """Control Unit operations."""
        alu_bitmask = 0b00100000
        pc_bitmask = 0b00010000
        operand_bitmask = 0b11000000
        instruction_bitmask = 0b00001111
        instruction = 0

        operand_num = 0
        
        address = self.pc
        # print("address", address, "register",self.reg)
        # Fetch
            # Copy Instruction from RAM into PC
            # Increment PC 
        opt_code = self.ram_read(address)
        self.ir = opt_code

         # Decode
            # Decode the contents of the IR register

        operand_num += opt_code & operand_bitmask
        operand_num = operand_num >> 6
        instruction += opt_code & instruction_bitmask
        if alu_bitmask & opt_code:
        # Execute
            self.branchtable["ALU"](operand_num,instruction)
            self.pc += 1
        elif pc_bitmask & opt_code:
        # Execute
            self.branchtable["PC"](operand_num,instruction)
        else:
            
        # Execute
            self.branchtable["OTHER"](operand_num,instruction)
            self.pc += 1

    def run(self):
        """Run the CPU."""
        
        while self.ir != 0b00000001:
            if self.sleep != 0:
                time.sleep(self.sleep)

            self.cu()


###############################################################
    # ALU OPS
    def ADD(self,*args):
        registerA,registerB = args[0], args[1]
        val = registerA + registerB

        if val > 255:
            print("WARNING! INTEGER OVERFLOW")
            self.reg[registerA] = 0
        else:
            self.reg[registerA] = val
    def SUB(self,*args):
        registerA,registerB = args[0], args[1]
        val = registerA - registerB

        if val < 0:
            print("WARNING! INTEGER OVERFLOW")
            self.reg[registerA] = 0
        else:
            self.reg[registerA] = val

    def MUL(self,*args):
        registerA,registerB = args[0], args[1]
        val = registerA * registerB

        if val > 255:
            print("WARNING! INTEGER OVERFLOW")
            self.reg[registerA] = 0
        else:
            self.reg[registerA] = val
        
    def DIV(self,*args):
        registerA,registerB = args[0], args[1]
        val = registerA / registerB
        
        if val < 0:
            print("WARNING! INTEGER OVERFLOW")
            self.reg[registerA] = 0
        else:
            self.reg[registerA] = registerA // registerB

    def MOD(self,*args):
        pass
    def INC(self,*args):
        pass
    def DEC(self,*args):
        pass
    def CMP(self,*args):
        registerA,registerB = self.reg[args[0]], self.reg[args[1]]
        # FL bits: 00000LGE 
        if registerA == registerB:
            self.fl = 0b00000001
        elif registerA < registerB:
            self.fl = 0b00000100
        else:
            self.fl = 0b00000010
 

    def AND(self,*args):
        pass
    def NOT(self,*args):
        pass
    def OR(self,*args):
        pass
    def XOR(self,*args):
        pass
    def SHL(self,*args):
        pass
    def SHR(self,*args):
        pass
###############################################################
    # PC OPS
    def CALL(self,*args):
        pass
    def RET(self,*args):
        pass
    def INT(self,*args):
        pass
    def IRET(self,*args):
        pass
    def JMP(self,*args):
        register = self.reg[args[0]]
        self.pc = register
    def JEQ(self,*args):
        register = self.reg[args[0]]
        if self.fl & 0b00000001 == 0b00000001:
        # FL bits: 00000LGE
            self.pc = register
        else:
            self.pc += 1
    def JNE(self,*args):
        register = self.reg[args[0]]
        if self.fl != 0b00000001:
            self.pc = register
        else:
            self.pc += 1
    def JGT(self,*args):
        pass
    def JLT(self,*args):
        pass
    def JLE(self,*args):
        pass
    def JGE(self,*args):
        pass
###############################################################
    # Other OPS
    def NOP(self,*args):
        pass
    
    def HLT(self,*args):
        pass

    def LDI(self,*args):
        register,integer = args[0], args[1]
        self.reg[register] = integer

    def LD(self,*args):
        pass

    def ST(self,*args):
        pass

    def PUSH(self,*args):
        pass

    def POP(self,*args):
        pass

    def PRN(self,*args):
        register = args[0]
        
        reg_value = format(self.reg[register], '#010b')
        print("\n",reg_value)

    def PRA(self,*args):
        pass
