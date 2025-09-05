#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
Ra_motor = Motor(Ports.PORT1, GearSetting.RATIO_6_1, False)
Rb_motor = Motor(Ports.PORT2, GearSetting.RATIO_6_1, False)
Rc_motor = Motor(Ports.PORT3, GearSetting.RATIO_6_1, False)
Rmotorgroup = MotorGroup(Ra_motor,Rb_motor,Rc_motor)

La_motor = Motor(Ports.PORT4, GearSetting.RATIO_6_1, False)
Lb_motor = Motor(Ports.PORT5, GearSetting.RATIO_6_1, False)
Lc_motor = Motor(Ports.PORT6, GearSetting.RATIO_6_1, False)
Lmotorgroup = MotorGroup(La_motor, Lb_motor,Lc_motor)

inertial_7 = Inertial(Ports.PORT7)
controller_1 = Controller(PRIMARY)
intake = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
elevation = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
slapapult = Motor(Ports.PORT10, GearSetting.RATIO_36_1, False)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

widthofbot = 32.5

inertial_7.calibrate()
while inertial_7.is_calibrating():
    sleep(50)
inertial_7.set_heading(0, DEGREES)
inertial_7.set_rotation(0, DEGREES)
    



#movement functions
def set_Left_velocity(percent):
    L_down.set_velocity(percent, PERCENT)
    L_up.set_velocity(percent, PERCENT)
def set_Right_velocity(percent1):
    R_down.set_velocity(percent1, PERCENT)
    R_up.set_velocity(percent1, PERCENT)

#autonomous functions
#returns positive values for the distance between two points.
def distanceL(a, b):
    if b > a:
        return 360 + a - b
    else:
        return a-b
    
def distanceR(a, b):
    if a > b:
        return 360 - a + b
    else:
        return b-a
    
#moving right and left side a specific distance.
def Right_move(cmR, speedR):#move right a designated amount of distance under a designated speed.
    set_Right_velocity(speedR)#set speed
    t = cmR/(181.83 * speedR / 100) #conversion from distance to time
    wait(t, SECONDS)
    set_Right_velocity(0)

def Left_move(cmL, speedL):#move left a designated amount of distance under a designated speed.
    set_Left_velocity(speedL)#set speed
    t = cmL/(181.83 * speedL / 100) #conversion from distance to time
    wait(t, SECONDS)
    set_Left_velocity(0)

#forward and backward
def Forward_backward(distance, speed):# enter both positive for forward and both negative for backward

    R_down.set_stopping(BRAKE)
    R_up.set_stopping(BRAKE)
    L_down.set_stopping(BRAKE)
    L_up.set_stopping(BRAKE)
    
    set_Right_velocity(speed)#set speed
    set_Left_velocity(speed)#set speed
    t = distance/(181.83 * speed / 100) #conversion from distance to time
    wait(t, SECONDS)
    set_Right_velocity(0)
    set_Left_velocity(0)


#rotating, input the designated location and speed, controlled using a PID recursive function loop
def Rotate_right(degrees, speed):

    R_down.set_stopping(BRAKE)
    R_up.set_stopping(BRAKE)
    L_down.set_stopping(BRAKE)
    L_up.set_stopping(BRAKE)

    distance = distanceR(inertial_7.orientation(YAW, DEGREES), degrees)

    r = (distance/360) * widthofrobot * 3.1415926
    #right side should be negative, left side postive
    t = r/(181.83 * speed / 100) #conversion from distance to time

    set_Right_velocity(-1*speed)
    set_Left_velocity(1*speed)
    wait(t, SECONDS)
    set_Right_velocity(0)
    set_Left_velocity(0)

    #the following ifs are recursive functions creating a PID loop.
    if distanceR(inertial_7.orientation(YAW, DEGREES), degrees) > 2 and distanceL(inertial_7.orientation(YAW, DEGREES), degrees) > 2: #if both sides difference is greater than 2
        if distanceR(inertial_7.orientation(YAW, DEGREES), degrees) > distanceL(inertial_7.orientation(YAW, DEGREES), degrees) : #determining the closest distance to designated point
            Rotate_left(degrees, speed)

        elif distanceL(inertial_7.orientation(YAW, DEGREES), degrees) > distanceR(inertial_7.orientation(YAW, DEGREES), degrees) : #determining the closest distance to designated point
            Rotate_right(degrees, speed)

def Rotate_left(degrees, speed):
    R_down.set_stopping(BRAKE)
    R_up.set_stopping(BRAKE)
    L_down.set_stopping(BRAKE)
    L_up.set_stopping(BRAKE)

    distance = distanceL(inertial_7.orientation(YAW, DEGREES), degrees)

    r = (distance/360) * 3.1415926 * widthofronbot
    t = r/(181.83 * speed / 100) #conversion from distance to time

    set_Right_velocity(1*speed)#set speed
    set_Left_velocity(-1*speed)

    wait(t, SECONDS)
    set_Right_velocity(0)
    set_Left_velocity(0)

    if distanceR(inertial_7.orientation(YAW, DEGREES), degrees) > 2 and distanceL(inertial_7.orientation(YAW, DEGREES), degrees) > 2: #if both sides difference is greater than 2
        if distanceR(inertial_7.orientation(YAW, DEGREES), degrees) > distanceL(inertial_7.orientation(YAW, DEGREES), degrees) : #determining the closest distance to designated point
            Rotate_left(degrees, speed)

        elif distanceL(inertial_7.orientation(YAW, DEGREES), degrees) > distanceR(inertial_7.orientation(YAW, DEGREES), degrees) : #determining the closest distance to designated point
            Rotate_right(degrees, speed)

def Turn_right(degreesR, turnspeedR):#incomplete
    global rotation
    R_down.set_stopping(BRAKE)
    R_up.set_stopping(BRAKE)
    L_down.set_stopping(BRAKE)
    L_up.set_stopping(BRAKE)

    rotation = inertial_7.orientation(YAW, DEGREES)
    #Rd and Ld are temporary variables
    Rd = (degreesR/360) * 97.75 * -1 #has to be going backwards to turn right
    Ld = (degreesR/360) * 97.75
    Right_move(Rd, turnspeedR)
    Left_move(Ld, turnspeedR)

    #the PID control below may have too high requirements for the robot, and may spin left and right.
    while not inertial_7.orientation(YAW, DEGREES) - rotation == degreesR:
        if inertial_7.orientation(YAW, DEGREES) - rotation > degreesR:
            Turn_left(inertial_7.orientation(YAW, DEGREES) - rotation - degreesR)
        elif inertial_7.orientation(YAW, DEGREES) - rotation < degreesR:
            Turn_right(degreesR - (inertial_7.orientation(YAW, DEGREES) - rotation))

def Turn_left(degreesL, turnspeedL):#incomplete
    global rotation
    R_down.set_stopping(BRAKE)
    R_up.set_stopping(BRAKE)
    L_down.set_stopping(BRAKE)
    L_up.set_stopping(BRAKE)

    rotation = inertial_7.orientation(YAW, DEGREES)
    #Rd and Ld are temporary variables
    Rd = (degreesL/360) * 97.75 
    Ld = (degreesL/360) * 97.75 * -1 #has to be going backwards to turn right
    Right_move(Rd, turnspeedL)
    Left_move(Ld, turnspeedL)
    #INCOMPLETE BELOW
    #the PID control below may have too high requirements for the robot, and may spin left and right.
    #while not rotation - inertial_7.orientation(YAW, DEGREES) == degreesL:
    #    if rotation - inertial_7.orientation(YAW, DEGREES) > degreesR:
    #        Turn_left(inertial_7.orientation(YAW, DEGREES) - rotation - degreesR)
    #    elif inertial_7.orientation(YAW, DEGREES) - rotation < degreesR:
    #        Turn_right(degreesR - (inertial_7.orientation(YAW, DEGREES) - rotation))

#control functions
def control():
    speed = (R_up.velocity(PERCENT) + L_down.velocity(PERCENT)) / 2
    if 0 > speed:
        speed = 0
    set_Right_velocity(controller_1.axis3.position() - controller_1.axis1.position())
    set_Left_velocity(controller_1.axis3.position() + controller_1.axis1.position())
    
    #code for intake, will keep motor spinning at 20%, increase as the speed of base increases
    if controller_1.buttonL1.pressing():
        intake.set_velocity(0, PERCENT)
    elif controller_1.buttonL2.pressing():
        intake.set_velocity(-100, PERCENT)
    else:
        intake.set_velocity((1 * (70 + speed)), PERCENT)
            # Negative speed for intake is going in
        wait(5, MSEC)

    if controller_1.buttonR2.pressing():
        elevation.set_velocity(-100,PERCENT)
    elif controller_1.buttonR1.pressing():
        elevation.set_velocity(100,PERCENT)
    else:
        elevation.set_velocity(0,PERCENT)
        
    if controller_1.buttonDown.pressing():#allowing catapult to maintain initiall loading position.
        #slapapult.set_velocity(-100,PERCENT)
        slapapult.spin_for(BACKWARD, 360, DEGREES, wait = True)
        


def when_started1():
    global rotation

    inertial_7.calibrate()
    while inertial_7.is_calibrating():
        sleep(50)
    
    R_down.spin(FORWARD)
    R_up.spin(FORWARD)
    L_down.spin(FORWARD)
    L_up.spin(FORWARD)
    intake.spin(FORWARD)
    elevation.spin(FORWARD)
    slapapult.spin(FORWARD)

    Rotate_right(90, 10)

    R_down.set_stopping(COAST)
    R_up.set_stopping(COAST)
    L_down.set_stopping(COAST)
    L_up.set_stopping(COAST)
    elevation.set_stopping(BRAKE)


    
    while True:
        control()
        if controller_1.buttonA.pressing():
            controller_1.screen.clear_screen()
            heading = inertial_7.heading(DEGREES)
            controller_1.screen.set_cursor(1,1)
            controller_1.screen.print(heading)

when_started1()

