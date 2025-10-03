# ---------------------------------------------------------------------------- #
#                                                                              #
#   Module:       main.py                                                      #
#   Author:       Leo Ji, Kirill Oleynikov, Andreas Tsang                      #
#   Created:      9/6/2025, 4:37:53 AM                                         #
#   Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
import math

brain = Brain()
controller = Controller()


r1=Motor(Ports.PORT1,True)
r2=Motor(Ports.PORT2, True)
r3=Motor(Ports.PORT3, False)
right_motors=MotorGroup(r1, r2, r3)

l1=Motor(Ports.PORT4, True)
l2=Motor(Ports.PORT5, True)
l3=Motor(Ports.PORT6, )
left_motors=MotorGroup(l1, l2, l3)

imu = Inertial(Ports.PORT7)

piston1 = DigitalOut(brain.three_wire_port.a)
piston2 = DigitalOut(brain.three_wire_port.b)
# start retracted
piston1.set(False)
piston2.set(False)

# PID Controller Class
class PIDController:
    def __init__(self, kP, kI, kD, max_output=1.0, min_output=-1.0):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.max_output = max_output
        self.min_output = min_output
        
        self.prev_error = 0
        self.integral = 0
        self.last_time = 0

    def calculate(self, setpoint, current_value):
        # Calculate error (shortest path)
        error = setpoint - current_value
        error = (error + 180) % 360 - 180  # Normalize to [-180, 180]
        
        # Calculate time delta
        current_time = brain.timer.time(SECONDS)
        dt = current_time - self.last_time if self.last_time > 0 else 0.02
        self.last_time = current_time
        
        # Avoid division by zero
        if dt <= 0:
            dt = 0.02
        
        # PID terms
        P = self.kP * error
        self.integral += error * dt
        I = self.kI * self.integral
        D = self.kD * (error - self.prev_error) / dt
        
        # Total output
        output = P + I + D
        
        # Clamp output
        output = max(min(output, self.max_output), self.min_output)
        
        # Store previous error
        self.prev_error = error
        
        return output
    
    def reset(self):
        self.prev_error = 0
        self.integral = 0
        self.last_time = 0


def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous started")
    
    # Calibrate IMU first!
    brain.screen.print("Calibrating IMU...")
    imu.calibrate()
    while imu.is_calibrating():
        wait(50, MSEC)
    brain.screen.clear_screen()
    brain.screen.print("IMU calibrated!")

    WHEEL_DIAM_IN   = 3.25     # wheel diameter in inches
    TRACK_WIDTH_IN  = 12.8    # distance between left/right wheel centers
    GEAR_RATIO_DRIVE = 0.75   # external gear ratio affecting wheel RPM

    pi = math.pi

    WHEEL_CIRC_IN = pi * WHEEL_DIAM_IN

    def drive_inches(speed_percent, inches, brake=True):
        turns = abs(inches) / WHEEL_CIRC_IN / GEAR_RATIO_DRIVE
        # IMPORTANT: your drivetrain uses REVERSE as forward
        direction = REVERSE if inches >= 0 else FORWARD

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

        left_dir  = REVERSE if degrees > 0 else FORWARD
        right_dir = FORWARD if degrees > 0 else REVERSE

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


    def drive_inches_pid(movement, max_speed=70, tolerance=2.0, timeout=3000):
        pass
        current_Lmotor_pos = 0#function
        current_Rmotor_pos = 0#function

        #function to calibrate both sides so they are the same. 

        

    def turn_degrees_pid(target_angle, max_speed=70, tolerance=2.0, timeout=3000):
        """
        Turn to specific angle using PID control
        target_angle: desired heading in degrees
        max_speed: maximum motor speed percentage (0-100)
        tolerance: how close we need to be to consider it done
        timeout: maximum time to attempt turning (ms)
        """
        brain.screen.print(f"Turning to {target_angle}°")
        
        # Create PID controller (tune these values for your robot!)
        pid = PIDController(kP=0.3, kI=0.001, kD=0.2, max_output=1.0, min_output=-1.0)
        
        start_time = brain.timer.time(MSEC)
        completed = False
        
        #reduces error caused by coasting
        left_motors.set_stopping(BRAKE)
        right_motors.set_stopping(BRAKE)
        

        while not completed and (brain.timer.time(MSEC) - start_time < timeout):
            # Get current angle
            current_angle = imu.rotation()
            
            # Calculate PID output
            output = pid.calculate(target_angle, current_angle)
            
            # Convert to motor speeds (scaled to max_speed)
            left_speed = output * max_speed
            right_speed = -output * max_speed
            
            # Apply to motors
            left_motors.spin(FORWARD)
            right_motors.spin(FORWARD)
            left_motors.set_velocity(left_speed, PERCENT)
            right_motors.set_velocity(right_speed, PERCENT)
            
            
            # Check if we're within tolerance
            error = abs(target_angle - current_angle)
            error = min(error, 360 - error)  # Shortest path error
            
            if error <= tolerance:
                completed = True
                brain.screen.print(f"Turn complete! Error: {error:.1f}°")
            else:
                brain.screen.clear_row(2)
                brain.screen.set_cursor(2, 1)
                brain.screen.print(f"Current: {current_angle:.1f}°, Error: {error:.1f}°")
            
            wait(20, MSEC)
        
        # Stop motors
        
        return completed

    start_on_right = True  # flip per alliance start tile
    brain.screen.print("autonomous complete")

    turn_degrees_pid(90)

def driver_control():

    left_motors.spin(FORWARD)
    right_motors.spin(FORWARD)

    brain.screen.clear_screen()
    brain.screen.print("driver control")
    # place driver control in this while loop

    while True:
        left_motors.set_velocity((controller.axis1.position() + controller.axis3.position()),PERCENT)
        right_motors.set_velocity((controller.axis1.position() - controller.axis3.position()), PERCENT)

        if controller.buttonR1.pressing():
            piston1.set(True)
            piston2.set(True)
        elif controller.buttonR2.pressing():
            piston1.set(False)
            piston2.set(False)
        # rumbles for motor overheat and stuff
        # if motor overheat
            #controller.rumble('..--')

        #add controls from controller
        wait(20, MSEC)

# create competition instance
comp = Competition(driver_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()
