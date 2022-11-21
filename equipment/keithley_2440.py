import pyvisa as py

# address_2440 = 'GPIB0::22::INSTR' # enter the keithley 2440 address here

class keithley_2440:
    def __init__(self,address_2440):
        rm = py.ResourceManager()
        self.equ_2440 = rm.open_resource(address_2440)
        self.equ_2440.write("*rst")
        self.equ_2440.write(":sour:func curr")
        self.equ_2440.write(":sour:curr:mode fix")

    def set_compliance(self,compliance):
        self.equ_2440.write(":sens:curr:prot {}".format(compliance))
    
    def reset(self):
        self.equ_2440.write("*rst")
        self.equ_2440.write(":sour:func curr")
        self.equ_2440.write(":sour:curr:mode fix")

    def set_current(self, current):
        self.equ_2440.write(":sour:curr:level {}".format(current))

    def output(self, option):
        if (option):
            self.equ_2440.write("outp on")
        else :
            self.equ_2440.write("outp off")
