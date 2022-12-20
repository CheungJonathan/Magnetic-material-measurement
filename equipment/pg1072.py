import pyvisa as py

# address_pg1072 = 'TCPIP0::AT::inst0::INSTR' # enter the keithley 2182a address here

class pg1072:
    
    def __init__(self,address_pg1072):
        rm = py.ResourceManager()
        self.equ_pg1072= rm.open_resource(address_pg1072)

    def info(self):
        # return the information of the equipment
        return self.equ_pg1072.query("*IDN?")

    def reset(self):
        self.equ_pg1072.write("*RST")

    def output(self,on_off,channel=1):
        if on_off:
            self.equ_pg1072.write(f'OUTPut{channel} ON')
        else:
            self.equ_pg1072.write(f'OUTPut{channel} OFF')
    
    def single_pulse_mode(self):
        # set the pulse mode
        self.equ_pg1072.write("SOURce1:PULSe:MODE SINGLE")
    
    def trigger_mode(self):
        # set the trigger mode
        self.equ_pg1072.write("TRIGger:MODE CONTINUOUS")
    
    def arm_pulse(self):
        self.equ_pg1072.write("PULSEGENControl:START")

    def trigger(self):
        self.equ_pg1072.write("*TRG")

    def set_pulse_period(self,period,channel=1,unit_period='ns'):
        self.equ_pg1072.write(f"SOURce{channel}:PERiod {period} {unit_period}")
    
    def set_pulse_vol(self,vol_high,vol_low,channel=1):
        self.equ_pg1072.write(f"SOURce{channel}:VOLT HIGH {vol_high}")
        self.equ_pg1072.write(f"SOURce{channel}:VOLT LOW {vol_low}")

    def set_pulse_width(self,width,channel=1,unit_period='ns'):
        self.equ_pg1072.write(f"SOURce{channel}:WIDth {width} {unit_period}")
    