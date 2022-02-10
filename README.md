# Lab-3_Ruiz_Martos
## **Closed Loop Controler**
 Our Closed Loop Controller is based solely off of the proportional gain. On initialization, the controller is set with a reference vector (currently in encoder ticks) that is the desired angle of the flywheel. During the controller update, it takes a measured value from the encoder, calculates the difference between this and the reference, and multiplies by the proportional gain to get a duty cycle. This duty cycle is returned.
## **Step Response Test**
 Our Step Response Test comprises of the user inputting a proportional gain constant, the motor running for one second to the desired angle of the flywheel, and recording the encoder position ticks and the time it was measured at. In our code, our plot.py creates a serial communication with a Nucleo that has our 4 other files on it. These files are encoder_Ruiz_Martos, motor_Ruiz_Martos, closedloop, and main. Our plot.py script is meant to be run on the computer, and after establishing connection with the nucleo, instructs the nucleo to quit what it is doing (ctrl + c) and restart (ctrl + d). Upon restart the Nucleo runs main.py which is adventageous for us. We send write commands through the serial to input the gain value in the response of main.py on the Nucleo. Once the Nucleo runs the program and collects the data and prints it, we use a serial read to get the data back to plot.py. 
## Results
![Kp = 0.1](kp_0.1_plot.png)
![alt text](kp_0.15_plot.png)
![alt text](kp_0.5_plot.png)
![alt text](kp_0.72_plot.png)
