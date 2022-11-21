# --------------------------
# Develop by Jonathan Cheung 
# SQML HKUST 
# skcheungag@connect.ust.hk
# --------------------------

# setting the measurement parameter

read_pulse = 500e-6
complience = 10 # volt
range_cur = 2 # A
point = 42

delay_1 = 1e-3 # second

file_name = 'new_device_1_11Nov22_outplane_2'



from equipment.keithley_6221 import keithley_6221
from equipment.kepco_model import kepco
import equipment.motor as motor

import time
import pandas as pd
import plotly.express as px
import numpy as np


# set the field list 
field_list = np.linspace(-range_cur,range_cur,round(point/2))
field_list = np.append(field_list,np.linspace(range_cur,-range_cur,round(point/2)))

k6221 = keithley_6221()
kep = kepco()

kep.set_cur_channel_2(0)
kep.on_off_channel_2(True)

# mo = motor.motor()
# time.sleep(3)
# mo.rotation(90)

k6221.auto_range(False)
k6221.custom_pulse_mode()
k6221.pulse_setting(widt = 1000e-6, sdel = 500e-6) # default point is 10000
k6221.set_compliance(complience)

k6221.custom_pulse_data(read_pulse)
k6221.custom_pulse_delay(delay_1)

k6221.arm_pulse()
save_file = {
    'field':field_list * 400
}
hall_vol = []
time.sleep(3)

for field in field_list:
    kep.set_cur_channel_2(field)
    time.sleep(0.5)
    k6221.init_pulse()
    time.sleep(1)
    hall_vol.append(k6221.pulse_data()[0])


save_file['field'] = field_list
save_file['hall_voltage'] = hall_vol
output_file = pd.DataFrame.from_dict(save_file)
output_file.to_csv(file_name+'.csv',index=None)

kep.on_off_channel_2(False)
k6221.pulse_end()

df = pd.read_csv(file_name+'.csv')
fig = px.line(x=df["field"], y=df["hall_voltage"]/read_pulse)
fig.update_layout(
    xaxis_title = "Field (Oe)",
    yaxis_title='Hall resistance (Ohm)',
)
fig.show()

