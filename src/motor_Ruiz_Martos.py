"""
    @file           TP_motor.py
    @brief          Driver class that sets up and controls motors.
    @details        Defines methods used to enable, disable and control the speed of the motors.
    @author         Dylan Ruiz
    @author         Lucas Martos-Repath
    @date           January 26, 2022
        
"""

import pyb
import time

class Motor:
    '''
        @brief      A motor class for one channel of the DRV8847
        @details    Objects of this class can be used to apply PWM to a
                    given DC motor
    '''
    
    def __init__(self, en_pin, in1pin, in2pin, timer):
        '''
            @brief          Initializes and returns a motor object 
            @details        Sets up pin and timer objects to a motor. 
                            Initialization of pin object must be done in Main. 
                            Initialization of timer occurs in init.
            @param en_pin   The pyb.pin() object for the enable motor pin
            @param in1pin   The pyb.pin() object for the PWM of the motor pin for forward direction.
            @param in2pin   The pyb.pin() object for the PWM of the motor pin for reverse direction.
            @param timer    The integer value of the timer channel wanted for the PWM.
        '''
        ## Initializes timer 
        self.timer = pyb.Timer(timer, freq = 20000)
        ## Initializes first motor pin
        self.pinIN1 = in1pin
        ## Initializes second motor pin
        self.pinIN2 = in2pin
        ## Initializes enable pin
        self.pinENABLE = en_pin
        

        

        ## Configures channel 1 for timer 
        self.timer_ch1 = self.timer.channel(1, pyb.Timer.PWM, pin=self.pinIN1)
        ## Configures channel 2 for timer 
        self.timer_ch2 = self.timer.channel(2, pyb.Timer.PWM, pin=self.pinIN2)

# 
       
    def enable(self):
        '''
            @brief      Brings the motor out of sleep mode
        '''
        ## Sets the sleep pin to high
        self.pinENABLE.high()
        ## Sets a delay of 25 us
        time.sleep_us(25)
   
    
    
    def disable(self):
        '''
            @brief       Disables selected motor.
        '''
        # self.motor = motor
        self.pinENABLE.low()
    
        pass
        
    def set_duty(self, duty):
        '''
            @brief              Sets the PWM duty cylce for the motor channel
            @details            This method sets the duty cycle to be sent to the 
                                motor to the given level. Positive values cause effort
                                in one direction, negative values in the opposite
                                direction
            @param      duty    A signed inteher holding the duty cycle
                                of the PWM signal sent to the motor
        '''
        # self.motor = motor
        if duty > 0:
            self.timer_ch1.pulse_width_percent(0)
            self.timer_ch2.pulse_width_percent(abs(duty))
        elif duty < 0:
            self.timer_ch1.pulse_width_percent(abs(duty))
            self.timer_ch2.pulse_width_percent(0)
            

if __name__ == '__main__':
    
    enableA = pyb.Pin(pyb.Pin.cpu.A10, pyb.Pin.OUT_PP)
    in1 = pyb.Pin(pyb.Pin.cpu.B4)
    in2 = pyb.Pin(pyb.Pin.cpu.B5)
    
    enableB = pyb.Pin(pyb.Pin.cpu.C1, pyb.Pin.OUT_PP)
    in3 = pyb.Pin(pyb.Pin.cpu.A0)
    in4 = pyb.Pin(pyb.Pin.cpu.A1)
    
    motor1 = Motor(enableA,in1,in2,3) # motor in A
    motor2 = Motor(enableB,in3,in4,5) #motor in B
    motor1.enable()
    motor2.enable()
    motor1.set_duty(-50)
    motor2.set_duty(50)
    
    time.sleep_ms(10000)
    motor1.disable()
    motor2.disable()
    
    

        
    
    
    
    
    
    
    
    

