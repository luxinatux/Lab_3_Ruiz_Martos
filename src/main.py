"""!
    @file           main.py
    @brief          Task implementation for step responses for two motors.
    @details        Implements co-task implementation using the cotask file.   
                    Produces and prints out step response results for both motors. 
                    Tasks are implemented as generators.
    @author         Dylan Ruiz
    @author         Lucas Martos-Repath
    @date           February 9, 2022
"""

import gc
import pyb
import cotask
import time
import task_share
import closedloop
import encoder_Ruiz_Martos
import motor_Ruiz_Martos
from micropython import const


def task_Encoder1():
    """!
    @brief    Task which initializes and updates encoder 1. 
    @details  Continuously writes the encoder position to the shared variable position1_share.
    """
    in1_enc = pyb.Pin(pyb.Pin.cpu.B6)
    in2_enc = pyb.Pin(pyb.Pin.cpu.B7)
    ## The encoder for Motor 1
    encoder1 = encoder_Ruiz_Martos.Encoder(in1_enc,in2_enc,4) # motor in A
    while True:
        encoder1.update()
        position1_share.put(encoder1.get_position())
        yield (0)
        
def task_Encoder2():
    """!
    @brief    Task which initializes and updates encoder 2. 
    @details  Continuously writes the encoder position to the shared variable position2_share.
    """
    in1_enc = pyb.Pin(pyb.Pin.cpu.C6)
    in2_enc = pyb.Pin(pyb.Pin.cpu.C7)
    encoder2 = encoder_Ruiz_Martos.Encoder(in1_enc,in2_enc,8) # motor in A
    while True:
        encoder2.update()
        position2_share.put(encoder2.get_position())
        yield (0)

def task_controller_motor1 ():
    """!
    @brief     Task which initializes and controlls motor 1. 
    @details   Controller object updates the duty cycle to the motor and allows closed loop proportional control.
               Implements a FSM to continuously print the position and time for the data to be processed. After 2000
               milliseconds, data will stop being processed
    """
     # CREATING MOTOR AND ENCODER OBJECTS TO BE USED
    enableA = pyb.Pin(pyb.Pin.cpu.A10, pyb.Pin.OUT_PP)
    in1_mot = pyb.Pin(pyb.Pin.cpu.B4)
    in2_mot = pyb.Pin(pyb.Pin.cpu.B5)
    motor1 = motor_Ruiz_Martos.Motor(enableA,in1_mot,in2_mot,3) # motor in A
    motor1.enable()
    ## Proportional gain for Controller 1
    Gain = 0.5
    ## Desired output postion of motor 1 in ticks
    step = 8000
    ## creating closed loop controller
    Closed_loop = closedloop.ClosedLoop(Gain, 0)
    ## Current time
    time_now = 0
    ## Initial time on first pass of Task
    time_start = time.ticks_ms()
    ## FSM state variable
    state = 0
    
    while True:
        if state == 0:
            time_now = time.ticks_diff(time.ticks_ms(),time_start)
            ## current position from Encoder task
            pos = position1_share.get()
            motor1.set_duty(Closed_loop.update(step,pos,time_now))
            print('M1,{:},{:}'.format(time_now,pos))
            if time_now >= 2000:
                state = 1
            yield (0)
        elif state == 1:
            print('done\r\n')
            state = 2
            yield(0)
        elif state == 2:
            yield(0)   
            
def task_controller_motor2 ():
    """!
    @brief     Task which initializes motor 2. 
    @details   Controller object updates the duty cycle to the motor and allows closed loop proportional control.
               Continuously prints the position and time for the data to be processed.
    """
     # CREATING MOTOR AND ENCODER OBJECTS TO BE USED
    enableB = pyb.Pin(pyb.Pin.cpu.C1, pyb.Pin.OUT_PP)
    in1_motB = pyb.Pin(pyb.Pin.cpu.A0)
    in2_motB = pyb.Pin(pyb.Pin.cpu.A1)
    motor2 = motor_Ruiz_Martos.Motor(enableB,in1_motB,in2_motB,5) # motor in B
    motor2.enable()
    ## Proportional gain for Controller 2
    Gain = 0.5
    ## Desired output postion of motor 1 in ticks
    step = 4000
    ## creating closed loop controller
    Closed_loop = closedloop.ClosedLoop(Gain, 0)
    ## Current time
    time_now = 0
    ## Initial time on first pass of Task
    time_start = time.ticks_ms()
    ## FSM state variable
    state = 0
    
    while True:
        if state == 0:
            time_now = time.ticks_diff(time.ticks_ms(),time_start)
            pos = position2_share.get()
            motor2.set_duty(Closed_loop.update(step,pos,time_now))
            print('M2,{:},{:}'.format(time_now,pos))
            if time_now >= 2000:
                state = 1
            yield (0)
        elif state == 1:
            print('done\r\n')
            state = 2
            yield(0)
        elif state == 2:
            yield(0)  

    
if __name__ == "__main__":
   
    #prints the start flag used to notify when to start reading the data lines.
    print("111\r\n")

    # Creates shares objects used to share the position between tasks.
    
    position1_share = task_share.Share('i', thread_protect = False, name = "Position 1")
    position2_share = task_share.Share('i', thread_protect = False, name = "Position 2")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    taskE1 = cotask.Task(task_Encoder1, name = 'Task_Encoder', priority = 2,
                        period = 5, profile = True, trace = False)
    taskE2 = cotask.Task(task_Encoder2, name = 'Task_Encoder', priority = 2,
                        period = 5, profile = True, trace = False)
    taskC1 = cotask.Task(task_controller_motor1, name = 'Task_Motor_Controller',
                        priority = 1, period = 15, profile = True, trace = False)
    taskC2 = cotask.Task(task_controller_motor2, name = 'Task_Motor_Controller',
                        priority = 1, period = 10, profile = True, trace = False)
    cotask.task_list.append(taskE1)
    cotask.task_list.append(taskE2)
    cotask.task_list.append(taskC1)
    cotask.task_list.append(taskC2)
    
    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()
    
    

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is received through the serial port
    vcp = pyb.USB_VCP ()
    while not vcp.any ():
        cotask.task_list.pri_sched ()

    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()
    
    # Print a table of task data and a table of shared information data
    