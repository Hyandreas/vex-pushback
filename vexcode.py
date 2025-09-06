# Library imports
from vex import *

brain = Brain()
controller = Controller()


r1=Motor(Ports.PORT1)
r2=Motor(Ports.PORT2)
r3=Motor(Ports.PORT3)
right_motors=MotorGroup(r1, r2, r3)

l1=Motor(Ports.PORT1)
l2=Motor(Ports.PORT2)
l3=Motor(Ports.PORT3)
left_motors=MotorGroup(l1, l2, l3)


def left_motor(speed):  
    speed = speed * 6
    left_motors.set_velocity(speed)

def right_motor(speed):
    speed = speed * 6
    right_motors.set_velocity(speed)





def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here

def user_control():

    left_motors.spin(FORWARD)
    right_motors.spin(FORWARD)

    brain.screen.clear_screen()
    brain.screen.print("driver control")
    # place driver control in this while loop

    while True:

        left_motor(controller.axis3.position() - controller.axis1.position())
        right_motor(controller.axis3.position() + controller.axis1.position())


        # rumbles for motor overheat and stuff
        # if motor overheat
            #controller.rumble('..--')

        #add controls from controller
        wait(20, MSEC)

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()
