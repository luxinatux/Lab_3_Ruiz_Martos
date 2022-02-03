"""
    @file           encoder_Ruiz_Martos.py
    @brief          Driver class for encoder project.
    @details        Defines functions used in the task_encoder.
    @author Dylan Ruiz
    @author Lucas Martos-Repath
    @date   January 26, 2022
"""

import pyb
import time

class Encoder:
    '''
        @brief                  Interface with quadrature encoders.
        @details                Defines functions used to interface with the encoder.
    '''
    def __init__(self, chanA, chanB, timer):
        '''
            @brief              Constructs an Encoder object
            @details            Attaches pins and timers, configures channels
                                and sets the value of parameters to be used
                                in encoder functions. Initialization of pin object must
                                be done in Main. Initialization of timer occurs in init
            @param chanA        The pyb.pin() object for the first encoder channel pin
            @param chanB        The pyb.pin() object for the second encoder channel pin
            @param timer        The integer value of the timer channel wanted for the encoder
        '''
        ## The positions of encoder 1
        self.pos_1 = 0
        
        
        ## The change in position for encoder 1 
        self.delta_1 = 0
            
        ## Attaches the A pin
        self.pinA = chanA
        ## Attaches the B Pin
        self.pinB = chanB
        
        
        
        ## Initializes timer to the channel n selected by timer input variable
        self.tim = pyb.Timer(timer, prescaler = 0, period = 65535) 
        
        ## Configures channel 1 for timer n, using pin a as input
        self.tch1 = self.tim.channel(1, pyb.Timer.ENC_A, pin=self.pinA)
        ## Configures channel 2 for timer n, using pin b as input
        self.tch2 = self.tim.channel(2, pyb.Timer.ENC_B, pin=self.pinB)

        
        ## Last position of encoder 1 when calculating delta
        self.start_1 = 0
        
        ## Position of encoder 1 when calculating delta
        self.stop_1 = 0
        
    def update(self):
        '''
            @brief              Updates encoder position and delta
            @details            Updated the encoder position and delta, as well
                                as accounting for overflow
        '''
        self.stop_1 = abs(self.tim.counter())
        
        self.delta_1 = self.stop_1 - self.start_1
        
        if self.delta_1 < -32768:
            
            self.delta_1 = self.delta_1 + 65536
            
        elif self.delta_1 > 32768:
            self.delta_1 = self.delta_1 - 65536
            
        self.pos_1 += self.delta_1
        self.start_1 = self.stop_1
        
        
    def get_position(self):
        '''
            @brief              Returns encoder position
            @details            Returns the position of the encoder based on
                                the results of the update() fcn
            @return             The position of the encoder shaft
        '''
        
        return self.pos_1
    
    def set_position(self, position):
        '''
            @brief              Sets encoder position
            @details            Sets the encoder position to the desired
                                user input
            @param position     Resets the position to the desired
                                user input
        '''
        self.start_1 = abs(self.tim.counter())
        self.pos_1 = position
           
        
        
    def get_delta(self):
        '''
            @brief              Returns encoder delta
            @details            Returns the change in position of the encoder
                                based on the results from the update() fcn
            @return             The change in position of the encoder shaft
                                between the two most recent updates
        '''
        return self.delta_1
        
if __name__ == '__main__':
    '''
    Initialization of pin objects must be done in main
    '''
    in1 = pyb.Pin(pyb.Pin.cpu.B6)
    in2 = pyb.Pin(pyb.Pin.cpu.B7)
    
    in3 = pyb.Pin(pyb.Pin.cpu.C6)
    in4 = pyb.Pin(pyb.Pin.cpu.C7)
    
    encoder1 = Encoder(in1,in2,4) # motor in A
    #motor2 = TP_Motor(enableB,in3,in4,5) #motor in B
    while True:
        encoder1.update()
        encoder1.get_position()
        time.sleep_ms(50)
        
