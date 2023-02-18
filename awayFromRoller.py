# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       AICamp                                                       #
# 	Created:      12/14/2022, 6:49:40 PM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()
controller_1 = Controller(PRIMARY)
left_motor_a = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT7, GearSetting.RATIO_18_1, True)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
right_motor_b = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True) 
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)
intake = Motor(Ports.PORT18, GearSetting.RATIO_18_1, True)
tower = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
flywheel = Motor(Ports.PORT17, GearSetting.RATIO_18_1, True)
gavintrollerroller = Motor(Ports.PORT13, GearSetting.RATIO_18_1, True)

# drivetrain initilization stuff that takes up way too many lines 
# region

# wait for rotation sensor to fully initialize
wait(30, MSEC)



# define variables used for controlling motors based on controller inputs
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False

# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3
            # right = axis2
            drivetrain_left_side_speed = controller_1.axis3.position()
            drivetrain_right_side_speed = controller_1.axis2.position()
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller_1:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller_1 = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller_1:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller_1 = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)
#endregion

# Begin project code
# gavin's kinda sus
# test
'''def pre_autonomous():
   # actions to do when the program starts
   brain.screen.clear_screen()
   brain.screen.print("pre auton code")
   wait(1, SECONDS)
 
def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("slayful girliepop!")
   # place automonous code here
def user_control():
    brain.screen.clear_screen()
    # place driver control in this while loop'''

brain.screen.set_font(FontType.MONO30)
for x in range(10):
    brain.screen.print("FACE YOUR FEAR!!!")
    brain.screen.next_row()
controller_1.screen.print("FACE YOUR FEAR!!!")

flypower = 100

# The code begins.
left_drive_smart.set_velocity(70, PERCENT)
right_drive_smart.set_velocity(70, PERCENT)
intake.set_velocity(100, PERCENT)
gavintrollerroller.set_velocity(100, PERCENT)

drivetrain.drive_for(REVERSE, 27, INCHES)
drivetrain.turn_for(RIGHT, 130, DEGREES)
drivetrain.drive_for(REVERSE, 13, INCHES)
wait(0.2, SECONDS)
left_drive_smart.set_velocity(20, PERCENT)
right_drive_smart.set_velocity(20, PERCENT)
drivetrain.drive_for(REVERSE, 7, INCHES, wait=False)
gavintrollerroller.spin_for(REVERSE, 0.69, SECONDS)
wait(0.6, SECONDS)
drivetrain.drive_for(FORWARD, 6, INCHES)
drivetrain.turn_for(LEFT, 136, DEGREES)
flywheel.spin_for(REVERSE, 20, TURNS, 58, PERCENT, wait=False)
wait(1.7, SECONDS)
tower.spin_for(FORWARD, 11, TURNS, 100, PERCENT)
flywheel.stop()
intake.spin_for(REVERSE, 10, TURNS, wait=False)
wait(0.5, SECONDS)
tower.spin_for(REVERSE, 9, TURNS, 100, PERCENT, wait=True)
flywheel.spin_for(REVERSE, 20, TURNS, 58, PERCENT, wait=False)
wait(1.7, SECONDS)
tower.spin_for(FORWARD, 11, TURNS, 100, PERCENT)
drivetrain.turn_for(RIGHT, 145, DEGREES)
flywheel.stop()
drivetrain.drive_for(REVERSE, 6, INCHES)

'''
drivetrain.drive_for(REVERSE, 6, INCHES, wait=False)
gavintrollerroller.spin_for(FORWARD, 0.6, SECONDS)
wait(1.2, SECONDS)
left_drive_smart.set_velocity(70, PERCENT)
right_drive_smart.set_velocity(70, PERCENT)
drivetrain.drive_for(FORWARD, 12, INCHES)
drivetrain.turn_for(RIGHT, 100, DEGREES)
wait(0.5, SECONDS)
flywheel.spin_for(REVERSE, 20, TURNS, 70, PERCENT, wait=False)
wait(3, SECONDS)
tower.spin_for(FORWARD, 11, TURNS, 100, PERCENT)
flywheel.stop()
intake.spin_for(REVERSE, 10, TURNS, wait=False)
wait(0.5, SECONDS)
tower.spin_for(REVERSE, 10, TURNS, 100, PERCENT)'''
'''
drivetrain.drive_for(FORWARD, 65, INCHES)
drivetrain.turn_for(LEFT, 138, DEGREES)
flywheel.spin_for(REVERSE, 20, TURNS, 80.9, PERCENT, wait=False)
wait(4, SECONDS)
tower.spin_for(FORWARD, 11, TURNS, 100, PERCENT)
flywheel.stop()'''



# drive code
#region
'''
while True:
    # L1 L2 (INTAKE FORWARD/REVERSE) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if controller_1.buttonL1.pressing():
        intake.spin(REVERSE, 80, PERCENT)
        tower.spin(REVERSE, 100, PERCENT)
    elif controller_1.buttonL2.pressing():
        intake.spin(FORWARD, 80, PERCENT)
    else:
        intake.stop()
    wait(5, MSEC)

    # R1 (FLYWHEEL) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if controller_1.buttonR1.pressing():
        flywheel.set_velocity(flypower, PERCENT)
        flywheel.spin(REVERSE)
    else:
        flywheel.set_velocity(0, PERCENT)
        flywheel.stop()

    # R2 (TOWER) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if controller_1.buttonR2.pressing():
        tower.set_velocity(flypower, PERCENT)
        tower.spin(FORWARD)
    else: 
        tower.set_velocity(0, PERCENT)
        tower.stop()

    # GAVIN TROLLER ROLLER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if controller_1.buttonA.pressing():
        gavintrollerroller.set_velocity(100, PERCENT)
        gavintrollerroller.spin(FORWARD)
    else:
        gavintrollerroller.set_velocity(0, PERCENT)
        gavintrollerroller.stop()
        
    print(tower.velocity(PERCENT))
    wait(0.5, MSEC) 
'''
#endregion
