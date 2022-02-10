"""!
    @file           Plot.py
    @brief          Data Acquisition file  
    @details        Communicates to the nucleo via serial port to collect step response data and plot it
    @author         Dylan Ruiz
    @author         Lucas Martos-Repath
"""
import serial
import time
import struct
from matplotlib import pyplot as plt

def plot():
    '''!
        @brief                  Runs main.py file on the nucleo and collects data.     
        @details                Runs main.py file on the nucleo via serial port and collects time and location(ticks) data from a step response.
                                When running on a different computer, ensure that the correct com port number is changed.
    '''
    with serial.Serial('COM3', 115200) as s_port:
        #joe = ''
       # s_port.write(b'\x02')
        #time.sleep(1)
        s_port.write(b'\x03') #runs the main function
        #time.sleep(1)
        s_port.write(b'\x04') #runs the main function
        #time.sleep(2)
        
        while True:
            a = s_port.readline()
            try:
                b = int(a)
            except:
                b = 0
            
            if b == 111:
                break
               
        asb = s_port.readline()      
        completition = 0
        x1_list = []
        y1_list = []
        x2_list = []
        y2_list = []
        while not completition == 1:
            mixed_output = s_port.readline().split(b',')
            print(mixed_output)
            
            if mixed_output[0] == b'M1':
                try:
                    time1 = int(mixed_output[1])
                except:
                    completition = 1
                    
                try:
                    pos1 = int(mixed_output[2])
                except:
                    completition = 1
                if completition == 0:
                    x1_list.append(time1)
                    y1_list.append(pos1)
            else:

                try:
                    time2 = int(mixed_output[1])
                except:
                    completition = 1
                    
                try:
                    pos2 = int(mixed_output[2])
                except:
                    completition = 1
                if completition == 0:
                    x2_list.append(time2)
                    y2_list.append(pos2)
            
            
       
        s_port.write(b'\r\n') #runs the main function
    s_port.close() #This made our code the only consistent repeatable output
     


    #plotting of the data commences here
    plt.plot(x1_list,y1_list,x2_list,y2_list)
    plt.xlabel("Time[ms]")
    plt.ylabel("Position[ticks]")
    plt.title("Step Response 1, period = 15ms") #title is changed for various plots
    
    '''
    plt.plot(x2_list,y2_list)
    plt.xlabel("Time[ms]")
    plt.ylabel("Position[ticks]")
    plt.title("Step Response 2, Kp = 0.5") #title is changed for various plots
'''
if __name__ == '__main__':
    plot()