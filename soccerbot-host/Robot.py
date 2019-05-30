import rpyc


class Robot:
    def __init__(self, robot_name):
        self.leftSpeed = 0
        self.rightSpeed = 0
        self.kicked = 0
        self.conn = rpyc.classic.connect(robot_name)  # host name or IP address of the EV3
        self.ev3 = self.conn.modules['ev3dev2.motor']  # import ev3dev.ev3 remotely
        self.kickMotor = self.ev3.MediumMotor('outA')
        self.rightMotor = self.ev3.LargeMotor('outB')
        self.leftMotor = self.ev3.LargeMotor('outC')

    def drive(self, left, right):
        if left != self.leftSpeed:
            self.leftSpeed = left
            self.leftMotor.run_forever(speed_sp=left)
        if right != self.rightSpeed:
            self.rightSpeed = right
            self.rightMotor.run_forever(speed_sp=right)

    def kick(self, kicked):
        if kicked != self.kicked:
            self.kicked = kicked
            if kicked > 0:
                self.kickMotor.run_to_abs_pos(position_sp=-90, speed_sp=1000, stop_action="hold")
            else:
                self.kickMotor.run_to_abs_pos(position_sp=0, speed_sp=200, stop_action="hold")

    def stop(self):
        self.leftMotor.stop(stop_action="coast")
        self.rightMotor.stop(stop_action="coast")
        self.kickMotor.stop(stop_action="coast")
