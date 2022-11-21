import nidaqmx

class kepco:

    def set_cur_channel_1(self, current):
        set_current = -current/2
        with nidaqmx.Task() as task:
            task.ao_channels.add_ao_voltage_chan("Dev2/ao0")
            task.write(set_current,auto_start=True)

    def set_cur_channel_2(self, current):
        set_current = -current/2
        with nidaqmx.Task() as task:
            task.ao_channels.add_ao_voltage_chan("Dev2/ao1")
            task.write(set_current,auto_start=True)

    def on_off_channel_1(self,on_off):
        if (on_off):
            with nidaqmx.Task() as task:
                task.do_channels.add_do_chan("Dev2/port2/line7")
                task.write(False,auto_start=True) # use false to open
        else :
            with nidaqmx.Task() as task:
                task.do_channels.add_do_chan("Dev2/port2/line7")
                task.write(True,auto_start=True) # use True to close kepco

    def on_off_channel_2(self,on_off):
        if (on_off):
            with nidaqmx.Task() as task:
                task.do_channels.add_do_chan("Dev2/port2/line5")
                task.write(False,auto_start=True) # use false to open
        else :
            with nidaqmx.Task() as task:
                task.do_channels.add_do_chan("Dev2/port2/line5")
                task.write(True,auto_start=True) # use True to close kepco
