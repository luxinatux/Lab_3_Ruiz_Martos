"""
    @file           closedloop.py
    @brief          Driver class implementing a closed loop controller.
    @details        Implements a closed loop P-Only controller for any system.
    @author         Dylan Ruiz
    @author         Lucas Martos-Repath
"""

class ClosedLoop:
    '''
        @brief      Closed loop feedback control class              
        @details    Objects of this class can be used to apply closed
                    closed loop feedback control to the velocity of the
                    motors
    '''
    def __init__(self, Gain_Vector, init_Reference_Vector):
        '''
            @brief                  Initializes and returns a Closed_Loop object          
            @details                The controller driver implements a P_only closed loop 
                                    controller and creates mutable gain values.
            @param Gain_Vector      The proportional gains of the closed-loop controller. 
            @param init_Reference_Vector The selected reference value based on desired value            
        '''
        ## Proportional gain value
        self.Gain_Vector = Gain_Vector
        ## Steady State Desired Value
        self.Reference_Vector = init_Reference_Vector
        ## Empty position array
        self.position = []
        ## Empty time array
        self.time = []
        
    
        
    def update(self, Reference_Vector, Measured_Vector, Time):
        '''
            @brief                           Updates the error value of the proportional controller
            @details                         Updates and calculates the error value of the 
                                             proportional controller based on the inputs of the 
                                             measured and reference values.
            @param      Reference_Vector     Reference input values based on desired values.
            @param      Measured_Vector      Inputs of measured data from the system, which is used to calculate the error.
            @param      Time                 Time input used to create a list adjacent to the position list.
            @return     duty                 The duty cycle calculated by the P-Only controller     
        '''
        self.max_lim = 100
        self.min_lim = -100
        self.Reference_Vector =  Reference_Vector 
        self.Measured_Vector =   Measured_Vector 
        
        
        self.duty = self.Gain_Vector*(self.Reference_Vector-self.Measured_Vector)


        if self.duty >= self.max_lim:
            self.duty = self.max_lim
        elif self.duty <= self.min_lim:
            self.duty = self.min_lim 
            
        self.position.append(self.Measured_Vector)
        self.time.append(Time)
        
        return self.duty
    
    def print_lists(self):
        '''
           @brief                   Prints both time and position arrays into one string.
           @details                 Prints position and time in an alternating sequence to fit both arrays into one string.
        '''
        self.Length = len(self.time)
        listofstr = []
        for i in range(self.Length):
            #print('{:},{:}'.format(self.time[i],self.position[i]))
            pos = '{:},'.format(self.position[i])
            tim = '{:},'.format(self.time[i])
            listofstr.append(pos)
            listofstr.append(tim)
    
        finalstr = "".join(listofstr)
        print(finalstr)     
        
        
   
    def get_Kp(self):
        '''
            @brief      Returns the proportional gain     
            @return     Returns the proportional gain set using the 
                        set_Kp function
        '''
        
        return self.Gain_Vector
    
    def set_K_Vector(self,Gain_Vector):
        '''
            @brief               Sets the value of the proportional gain
            @param Gain_Vector   The proportional gains of the closed-loop controller.
        '''
        
        
        self.Gain_Vector = Gain_Vector
        
    
        