from vex import *

brain = Brain()
controller = Controller()


r1=Motor(Ports.PORT1)
r2=Motor(Ports.PORT2)
r3=Motor(Ports.PORT3)
right_motors=MotorGroup(r1, r2, r3)

l1=Motor(Ports.PORT4)
l2=Motor(Ports.PORT5)
l3=Motor(Ports.PORT6)
left_motors=MotorGroup(l1, l2, l3)


def left_motor(speed):  
    speed = speed * 6
    left_motors.set_velocity(speed)

def right_motor(speed):
    speed = speed * 6
    right_motors.set_velocity(speed)





def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous started")

    WHEEL_DIAM_IN   = 3.5     # wheel diameter in inches (adjust if not 4")
    TRACK_WIDTH_IN  = 12.8    # distance between left/right wheel centers (in)
    GEAR_RATIO_DRIVE = 0.75    # external gear ratio affecting wheel RPM (1.0 if direct)

    WHEEL_CIRC_IN = math.pi * WHEEL_DIAM_IN

    def drive_inches(speed_percent, inches, brake=True):
        turns = abs(inches) / WHEEL_CIRC_IN / GEAR_RATIO_DRIVE
        direction = FORWARD if inches >= 0 else REVERSE

        left_motors.set_velocity(abs(speed_percent), PERCENT)
        right_motors.set_velocity(abs(speed_percent), PERCENT)

        left_motors.spin_for(direction, turns, TURNS, False)
        right_motors.spin_for(direction, turns, TURNS, True)

        if brake:
            left_motors.stop(BRAKE)
            right_motors.stop(BRAKE)
        else:
            left_motors.stop(COAST)
            right_motors.stop(COAST)

    def turn_degrees(speed_percent, degrees, brake=True):

        arc_len_in = math.pi * TRACK_WIDTH_IN * (abs(degrees) / 360.0)
        turns = arc_len_in / WHEEL_CIRC_IN / GEAR_RATIO_DRIVE

        left_dir  = FORWARD if degrees > 0 else REVERSE
        right_dir = REVERSE if degrees > 0 else FORWARD

        left_motors.set_velocity(abs(speed_percent), PERCENT)
        right_motors.set_velocity(abs(speed_percent), PERCENT)

        left_motors.spin_for(left_dir,  turns, TURNS, False)
        right_motors.spin_for(right_dir, turns, TURNS, True)

        if brake:
            left_motors.stop(BRAKE)
            right_motors.stop(BRAKE)
        else:
            left_motors.stop(COAST)
            right_motors.stop(COAST)

    # === ROUTE: first floor cluster -> adjacent loader -> long goal ===
    start_on_right = True  # flip per alliance start tile

    # 1) go to block cluster (2nd arg is distance)
    drive_inches(60, 20)
    drive_inches(25, 3)
    drive_inches(40, -6)

    # 2) go to loader
    if start_on_right:
        turn_degrees(45, 90)
    else:
        turn_degrees(45, -90)

    drive_inches(55, 16)
    drive_inches(35, -4)

    # 3) long goal
    if start_on_right:
        turn_degrees(45, -90)
    else:
        turn_degrees(45, 90)
    drive_inches(60, 36)
    drive_inches(25, 2)
    drive_inches(40, -6)


def driver_control():

    left_motors.spin(REVERSE)
    right_motors.spin(REVERSE)

    brain.screen.clear_screen()
    brain.screen.print("driver control")
    # place driver control in this while loop

    while True:


        left_motors.set_velocity(controller.axis3.position() - controller.axis1.position())
        right_motors.set_velocity(controller.axis3.position() + controller.axis1.position())


        # rumbles for motor overheat and stuff
        # if motor overheat
            #controller.rumble('..--')

        #add controls from controller
        wait(20, MSEC)

# create competition instance
comp = Competition(driver_control, autonomous)

driver_control()

# actions to do when the program starts
brain.screen.clear_screen()