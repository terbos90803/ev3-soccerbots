import rpyc
conn = rpyc.classic.connect('ev3dev-BLUE') # host name or IP address of the EV3
ev3 = conn.modules['ev3dev2.motor']      # import ev3dev.ev3 remotely
m = ev3.LargeMotor('outB')
m.run_timed(time_sp=1000, speed_sp=600)
