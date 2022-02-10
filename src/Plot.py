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
        s_port.write(b'\x03') #runs the main function
        time.sleep(1)
        s_port.write(b'\x04') #runs the main function
        time.sleep(1)
        completition = 0
        x_list = []
        y_list = []
        while not completition == 1:
            mixed_output = s_port.readline().split(b',')
            print(mixed_output)
            try:
                time1 = int(mixed_output[0])
            except:
                completition = 1
                
            try:
                pos1 = int(mixed_output[1])
            except:
                completition = 1
            if completition == 0:
                x_list.append(time1)
                y_list.append(pos1)
                
            
            
        #print(mixed_output)
        #final = len(mixed_output)
        
        #s_port.write(b'L1\r') #endline? 
        
        #bytearray('hi', 'utf8')
        #bytearray('hi\r', 'utf8')
    s_port.close() #This made our code the only consistent repeatable output
    '''
    x_list = []
    y_list = []
    state = 0
    for i in range(final):

        if state == 0:
            try: 
                pos_1 = int(mixed_output[i])
            except ValueError:
                Fault_1 = False
                pass
            else: 
                Fault_1 = True
            state = 1
            if Fault_1 == True:
                pos_fin = pos_1
            continue
                
        if state == 1:
            try: 
                tim_1 = int(mixed_output[i])
            except ValueError:
                Fault_2 = False
                pass
            else: 
                Fault_2 = True
            state = 0
            
            if Fault_2 == True and Fault_1 == True:
                tim_fin = tim_1
                x_list.append(tim_fin)
                y_list.append(pos_fin)
    '''
                
                
    #print(x_list)
    #print(y_list)

    #https://matplotlib.org/stable/tutorials/introductory/pyplot.html


    #plotting of the data commences here
    plt.plot(x_list,y_list)
    plt.xlabel("Time[ms]")
    plt.ylabel("Position[ticks]")
    plt.title("Step Response, Kp = 0.5") #title is changed for various plots

if __name__ == '__main__':
    plot()