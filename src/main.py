"""!
@file basic_tasks.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import time
import task_share
import closedloop
import encoder_Ruiz_Martos
import motor_Ruiz_Martos
import print_task

def task_Encoder ():
    """!
    Task which takes things out of a queue and share to display.
    """
    in1_enc = pyb.Pin(pyb.Pin.cpu.B6)
    in2_enc = pyb.Pin(pyb.Pin.cpu.B7)
    encoder1 = encoder_Ruiz_Martos.Encoder(in1_enc,in2_enc,4) # motor in A
    while True:
        encoder1.update()
        position1_share.put(encoder1.get_position())
        yield (0)

def task_controller_motor ():
    """!
    Task which puts things into a share and a queue.
    """
     # CREATING MOTOR AND ENCODER OBJECTS TO BE USED
    enableA = pyb.Pin(pyb.Pin.cpu.A10, pyb.Pin.OUT_PP)
    in1_mot = pyb.Pin(pyb.Pin.cpu.B4)
    in2_mot = pyb.Pin(pyb.Pin.cpu.B5)
    motor1 = motor_Ruiz_Martos.Motor(enableA,in1_mot,in2_mot,3) # motor in A
    motor1.enable()
    Gain = 0.5
    step = 8000
    Closed_loop = closedloop.ClosedLoop(Gain, 0)
    time_now = 0
    time_start = time.ticks_ms()
    while True:
        time_now = time.ticks_diff(time.ticks_ms(),time_start)
        pos = position1_share.get()
        motor1.set_duty(Closed_loop.update(step,pos,time_now))
        print_queue.put ("Encoder Pos: {:d}\r\n".format (pos))

            
        yield (0)

# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print ('\033[2JTesting ME405 stuff in cotask.py and task_share.py\r\n'
           'Press ENTER to stop and show diagnostics.')

    # Create a share and a queue to test function and diagnostic printouts
    share0 = task_share.Share ('h', thread_protect = False, name = "Share 0")
    q0 = task_share.Queue ('L', 16, thread_protect = False, overwrite = False,
                           name = "Queue 0")
    
    position1_share = task_share.Share('i', thread_protect = False, name = "Position 1")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    """
    task1 = cotask.Task (task1_fun, name = 'Task_1', priority = 1, 
                         period = 400, profile = True, trace = False)
    task2 = cotask.Task (task2_fun, name = 'Task_2', priority = 2, 
                         period = 1500, profile = True, trace = False)
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)
    """
    
    taskE = cotask.Task(task_Encoder, name = 'Task_Encoder', priority = 2,
                        period = 5, profile = True, trace = False)
    taskC = cotask.Task(task_controller_motor, name = 'Task_Motor_Controller',
                        priority = 1, period = 10, profile = True, trace = False)
    cotask.task_list.append(taskE)
    cotask.task_list.append(taskC)
    
    #print task code
    print_task = cotask.Task (print_task_function, name = 'Printing', 
                          priority = 0, profile = True)
    cotask.task_list.append (print_task)

    
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
    print ('\n' + str (cotask.task_list))
    print (task_share.show_all ())
    print (taskE.get_trace ())
    print ('\r\n')