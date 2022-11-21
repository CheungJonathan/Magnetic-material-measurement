# --------------------------
# Develop by Jonathan Cheung 
# SQML HKUST 
# skcheungag@connect.ust.hk
# --------------------------

read_pulse = 1e-4
range_vol = 35  # *100uA it is range current
complience = 15 # volt

field = 9
delay_1 = 1e-3 # second
delay_2 = 1e-3 # second

file_name = f'multi_stage_test_pillar_inplane_{field}_A_field_dif_4.csv'

# - Loading equipment library and other -
from equipment.kepco_model import kepco
from equipment.keithley_6221 import keithley_6221
import equipment.motor as motor

import time
import pandas as pd
import plotly.express as px

# mo = motor.motor()
# time.sleep(4)
# mo.rotation(-0.05)

k6221 = keithley_6221()
kep = kepco()

k6221.auto_range(False)
k6221.custom_pulse_mode()
k6221.pulse_setting(widt = 1000e-6, sdel = 500e-6) # default point is 10000  
k6221.set_compliance(complience)

kep.set_cur_channel_2(field)
kep.on_off_channel_2(True)

write_pulse = [] # generate data 
for i in range(range_vol*2+1):
    write_pulse.append(round(-1e-4*range_vol+i*1e-4,4))
for i in range(range_vol*2):
    write_pulse.append(round(1e-4*range_vol-1e-4-i*1e-4,4))

# pulse writing
for i in range(len(write_pulse)//50+1):
    text = ''
    w_text = write_pulse[i*50:(i+1)*50]
    for j in range(len(w_text)):
        if j == 0:
            list_write = '{},{}'.format(w_text[j],read_pulse)
            delay_data = "{},{}".format(delay_1,delay_2)
        else:
            list_write += ',{},{}'.format(w_text[j],read_pulse)
            delay_data += ",{},{}".format(delay_1,delay_2)
    if i == 0:
        k6221.custom_pulse_data(list_write)
        k6221.custom_pulse_delay(delay_data)
    else :
        k6221.custom_pulse_data_append(list_write)
        k6221.custom_pulse_delay_append(delay_data)
    time.sleep(1)

time.sleep(3)
k6221.arm_pulse()
time.sleep(5)
k6221.init_pulse()
time.sleep(len(write_pulse)*(delay_1+delay_2+0.2)+10)

k6221.pulse_end()
kep.on_off_channel_2(False)

record = k6221.pulse_data()

vol_write = record[::2]
vol_read = record[1::2]

read_list=[]
for _ in write_pulse:
    read_list.append(read_pulse)

my_data = {
    "write pulse":write_pulse,
    "read pulse":read_list,
    "Volt write pulse":vol_write,
    "Volt read pulse":vol_read
}
save_data = pd.DataFrame.from_dict(my_data)
save_data.to_csv(file_name+'.csv',index=None)

df_1 = pd.read_csv(file_name+'.csv')
fig = px.line(x=df_1['write pulse'], y=df_1['Volt write pulse']/df_1['write pulse'])
fig.update_layout(
    xaxis_title = "Current (A)",
    yaxis_title='Hall resistance (Ohm)',
)
fig.show()

fig_2 = px.line(x=df_1['write pulse'],  y=df_1['Volt read pulse']/df_1['read pulse'])
fig_2.update_layout(
    xaxis_title = "Current (A)",
    yaxis_title='Hall resistance (Ohm)',
)
fig_2.show()