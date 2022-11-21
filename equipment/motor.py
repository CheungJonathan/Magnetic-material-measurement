# motor 
# written by Jonathan Cheung (ECE HKUST)
# improve version with fix step
# fix step is 6400 step / circle 

import serial
import time

# 4 is old 
# 5 is new
# address = 'COM8'

class motor:
    def __init__(self,address='COM8'):
        self.ser = serial.Serial(address, 9600)
        self.angle = 0.0
        self.angle_dif = 0.0
        self.speed_mode = 12800
        # big motor is 12800
        # small motor is 3200

        #  stop reset
        # self.ser.setDTR(False)

        time.sleep(3)

    def send_message(self,message):
        instruction = bytes(message, encoding = 'utf8')
        self.ser.write(instruction)
        time.sleep(0.02)

    def power(self,on_off):
        if on_off:
            self.send_message('30001')
        else:
            self.send_message('30002')

    def power_on(self):
        self.send_message('30001')

    def power_off(self):
        self.send_message('30002')

    def record_angle(self):
        with open('C:\\Users\\DELL\\Desktop\\programs_stable\\support\\motor_angle_record.csv', 'w') as f:
            b = self.angle
            f.write("{}".format(b))

    def rotation(self, final_angle):
        # self.angle = np.loadtxt('C:\\Users\\DELL\\Desktop\\programs_stable\\support\\motor_angle_record.csv', dtype = float, comments = '#', usecols = (0,))
        if(final_angle <= 360.0 and final_angle >= 0):
            self.angle_dif = final_angle - self.angle
        elif(final_angle > -180):
            self.angle_dif = final_angle - self.angle

        pulse = int(self.angle_dif/360*self.speed_mode)
        
        
        self.send_message(str(pulse))
        self.angle = round(self.angle + pulse / self.speed_mode * 360,7)
        print(f'pulse {pulse}, angle{self.angle}')
        self.record_angle()

    def get_ang_set_time(self):
        return abs(self.angle_dif * 0.76)

    def set_angle(self):
        self.angle = 0.0
    
    def return_zero(self):
        self.rotation(0) 

    def close(self):
        self.send_message('30002')
        self.ser.close()

    def connection_close(self):
        self.ser.close()
