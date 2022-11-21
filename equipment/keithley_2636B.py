import pyvisa

class keithley_2636B :
    def __init__(self,address): 
        rm = pyvisa.ResourceManager()
        self.k2636 = rm.open_resource(address)
        self.k2636.write("smua.sense = smua.SENSE_LOCAL")

    def reset(self):
        self.k2636.write("smua.reset()")
        self.k2636.write("smub.reset()")
    
    def output_a(self,on_off):
        if on_off:
            self.k2636.write("smua.source.output = smua.OUTPUT_ON")
        else:
            self.k2636.write("smua.source.output = smua.OUTPUT_OFF")
    
    def v_range_a(self,range_v):
        self.k2636.write(f"smua.source.rangev = {range_v}")
    
    def set_voltage_a(self,voltage):
        self.k2636.write(f"smua.source.levelv = {voltage}")

    def set_current_a(self,current):
        self.k2636.write(f"smua.source.leveli = {current}")

    # def record_a(self):
    #     return self.k2636.query("print(smua.measure.i(smua.nvbuffer1))")
    
    def auto_range_measurement_a(self,on_off):
        if on_off:
            self.k2636.write("smua.measure.autorangei = smua.AUTORANGE_ON")
        else:
            self.k2636.write("smua.measure.autorangei = smua.AUTORANGE_OFF")
    
    def comp_current_a(self,comp):
        self.k2636.write(f"smua.source.limiti = {comp}")
    
    def sweepVmeasureI(self,startv,stopv,stime,points):
        self.k2636.write(f"SweepVLinMeasureI(smua,{startv},{stopv},{stime},{points})")
    
    def sweep_data(self):
        data = self.k2636.query("printbuffer(1,smua.nvbuffer1.n,smua.nvbuffer1.readings)")
        return  data.split(",")

    def output_b(self,on_off):
        if on_off:
            self.k2636.write("smub.source.output = smub.OUTPUT_ON")
        else:
            self.k2636.write("smub.source.output = smub.OUTPUT_OFF")
    
    def v_range_b(self,range_v):
        self.k2636.write(f"smub.source.rangev = {range_v}")
    
    def set_voltage_b(self,voltage):
        self.k2636.write(f"smub.source.levelv = {voltage}")

    def record_a(self):
        return float(self.k2636.query("print(smua.measure.i(smua.nvbuffer1))"))

    def record_b(self):
        return float(self.k2636.query("print(smub.measure.i(smub.nvbuffer1))"))