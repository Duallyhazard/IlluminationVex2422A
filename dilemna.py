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
endgame = DigitalOut(brain.three_wire_port.a)
# wait for rotation sensor to fully initialize
wait(30, MSEC)


# region
# define variables used for controlling motors based on controller inputs
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False
wannaGetToTheRollersFast = 0.7
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
            drivetrain_left_side_speed = wannaGetToTheRollersFast * controller_1.axis3.position()
            drivetrain_right_side_speed =  wannaGetToTheRollersFast * controller_1.axis2.position()
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 * wannaGetToTheRollersFast and drivetrain_left_side_speed > -5 * wannaGetToTheRollersFast:
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
            if drivetrain_right_side_speed < 5 * wannaGetToTheRollersFast and drivetrain_right_side_speed > -5 * wannaGetToTheRollersFast:
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

def pre_autonomous():
   # actions to do when the program starts
   brain.screen.clear_screen()
   brain.screen.print("We good. We good.")
   wait(1, SECONDS)
 
def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("slayful girliepop!")
    # place automonous code here
    left_drive_smart.set_velocity(75, PERCENT)
    right_drive_smart.set_velocity(75, PERCENT)
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
    wait(0.2, SECONDS)
    drivetrain.drive_for(FORWARD, 6, INCHES)
    drivetrain.turn_for(LEFT, 136, DEGREES)
    flywheel.spin_for(REVERSE, 20, TURNS, 58, PERCENT, wait=False)
    wait(1.2, SECONDS)
    tower.spin_for(FORWARD, 10, TURNS, 100, PERCENT)
    flywheel.stop()
    intake.spin_for(REVERSE, 10, TURNS, wait=False)
    wait(0.5, SECONDS)
    tower.spin_for(REVERSE, 9, TURNS, 100, PERCENT, wait=True)
    flywheel.spin_for(REVERSE, 20, TURNS, 58, PERCENT, wait=False)
    wait(1.2, SECONDS)
    tower.spin_for(FORWARD, 10, TURNS, 100, PERCENT)
    drivetrain.turn_for(RIGHT, 145, DEGREES)
    flywheel.stop()
    drivetrain.drive_for(REVERSE, 6, INCHES)

def user_control():
    brain.screen.clear_screen()
    # place driver control in this while loop
    brain.screen.set_font(FontType.MONO30)
    for x in range(10):
        brain.screen.print("huffy puffy huffy puffy huffy puffy huffy puffy huffy puffy huffy puffy huffy puffy huffy puffy huffy puffy")
        brain.screen.next_row()
    controller_1.screen.print("I'll handle this.")
    flypower = 100
    def slayfulshoot():
        controller_1.rumble("-")
        flywheel.spin_for(REVERSE, 20, TURNS, 100, PERCENT, wait=False)
        wait(3, SECONDS)
        tower.spin_for(FORWARD, 11, TURNS, 100, PERCENT)
    def shortfulshoot():
        controller_1.rumble("-")
        flywheel.spin_for(REVERSE, 17, TURNS, 63, PERCENT, wait=False)
        wait(2, SECONDS)
        tower.spin_for(FORWARD, 12, TURNS, 100, PERCENT)
    while True:
        # slayful & shortful shooting (UP AND DOWN ) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if controller_1.buttonUp.pressing():
            slayfulshoot()
        if controller_1.buttonDown.pressing():
            shortfulshoot()
        
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
        # ENDGAME (X) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if controller_1.buttonX.pressing():
            endgame.set(True)
        if controller_1.buttonB.pressing():
            endgame.set(False)
        # DRIVE SPEED (MEMORIES FOLLOW ME LEFT AND RIGHT)
        if controller_1.buttonLeft.pressing():
            wannaGetToTheRollersFast = 1
        if controller_1.buttonRight.pressing():
            wannaGetToTheRollersFast = 0.7
        # slay!
        '''towerpower = int(flywheel.velocity(PERCENT))
        if towerpower < 0:
            print(flywheel.velocity(PERCENT))
        wait(0.5, MSEC)'''
        # round in circles got you stuck up in my head



# create competition instance
comp = Competition(user_control, autonomous)
pre_autonomous()