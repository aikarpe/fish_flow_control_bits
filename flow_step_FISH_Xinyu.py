""" these are basic functions for Xinyu's FISH flow experiment 

    step is considered as a most simple unit in flow experiment
    and each step consists of 
        - switch valve 
        - set pressure
        - flow 
            for T seconds | until volume V is reached
        - wait for P seconds



    for M-SWITCH vale use human indexing: 
        1st valve index: 1, 
        last valve index: 10


    to synchronize acquisition in Andor's IQ use TTL signals
        - python script is master and Andor's IQ protocol is slave
        - script should send out TTL signal (channel: TTL_TO_IQ, type: TTL_TO_IQ_TYPE) and wait for response (end of acquisition; channel: TTL_FROM_IQ, type: TTL_FROM_IQ_TYPE)


"""
 
from __future__ import print_function 

import time

from Fluigent.SDK import fgt_init, fgt_close

from Fluigent.SDK import fgt_get_valveChannelCount
from Fluigent.SDK import fgt_get_valveRange, fgt_get_valvePosition, fgt_set_valvePosition

from Fluigent.SDK import fgt_set_pressure, fgt_get_pressure, fgt_get_pressureRange

from Fluigent.SDK import fgt_get_sensorValue, fgt_get_sensorRange
from Fluigent.SDK import fgt_set_sensorRegulation

from Fluigent.SDK import fgt_set_TtlMode, fgt_read_Ttl, fgt_get_TtlChannelsInfo
from Fluigent.SDK import fgt_trigger_Ttl

from sys import exit 

  
###################### DEVICE SETTINGS #########################
PRESSURE_CHANNEL = 0
SENSOR = 0
M_SWITCH = 0
DELTA_TIME = 0.1 # s
TTL_TO_IQ = 0 # add input on IQ side
TTL_FROM_IQ = 1 # add output on IQ side
TTL_TO_IQ_TYPE = 3 # add description
TTL_FROM_IQ_TYPE = 1 # add description
#################################################################

def flow_step(valve_index, valve_position, pressure_controller_index, pressure, step_duration, pause_duration):
    """ a basic FISH flow expreiment step """
    
    fgt_set_valvePosition(valve_index, valve_position)
    fgt_set_pressure(pressure_controller_index, pressure)
    time.sleep(step_duration)
    fgt_set_pressure(pressure_controller_index, 0)
    time.sleep(pause_duration)

def flow_step_adv(valve_index, valve_position, pressure_controller_index, sensor_index, flow_rate, target_volume, step_time, pause_duration):
    """ a basic FISH flow expreiment step """
    
    fgt_set_valvePosition(valve_index, valve_position - 1) # here human indexing changed to sdk's 
    print('valve position set {} '.format(valve_position))
    
    current_volume = 0

    print('target_volume {}'.format(target_volume))

    while current_volume < target_volume:
        fgt_set_sensorRegulation(sensor_index, pressure_controller_index, flow_rate)
        time.sleep(step_time)
        sensorMeasurement = fgt_get_sensorValue(sensor_index)
        # units are important!!! make sure update takes that into account!!!
        current_volume = current_volume + step_time * flow_rate / 60 
        print('dispensed: {}   target_volume: {}   rate: {}   (q) to abort'.format(current_volume, target_volume, flow_rate))

    
    fgt_set_pressure(pressure_controller_index, 0)
    print('will wait for {} s'.format(pause_duration))
    time.sleep(pause_duration)

def flow_step_simple(step):
    """ simplified flow step """
    flow_step_adv(M_SWITCH, \
                  step["valve_index"], \
                  PRESSURE_CHANNEL, \
                  SENSOR, \
                  step["flow_rate"], \
                  step["target_volume"], \
                  DELTA_TIME, \
                  step["pause"])

def wait_for_IQ_acq_completion(ttl_ID):
    while not fgt_read_Ttl(ttl_ID): # trigger happened? 0: no, 1: yes
        time.sleep(0.5)

def exit_fgt_nicely():
    """ reset pressure channel an close communication """
    fgt_set_pressure(PRESSURE_CHANNEL, 0)
    fgt_close()
    exit()


################################################################

## init session
fgt_init()

## set up TTLs that communicates with IQ
                        # set up TTL channels
fgt_set_TtlMode(TTL_TO_IQ, TTL_TO_IQ_TYPE)
fgt_set_TtlMode(TTL_FROM_IQ, TTL_FROM_IQ_TYPE)


