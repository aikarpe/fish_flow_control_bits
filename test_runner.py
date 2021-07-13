""" 
    an execution of custom FISH flow step
    user input defines all relevant params {valve, flowrate, target volume}
"""
#full location of flow_step_FISH_Xinyu.py
source = "C:/Users/790NWL2/Desktop/aigars/Xinyu/scripts/flow_step_FISH_Xinyu.py"

valve  = int(input("give the valve index "))
flow   = float(input("please enter the flow rate "))
target = float(input("please enter the target volume "))

print('{}'.format(isinstance(valve, str)))


"""The wash dict that get plugged into the equation"""
wash = {
  "valve_index": valve,
  "flow_rate": flow,
  "target_volume": target,
  "pause": 0}

"""restart the script"""
boolean = input("are you sure you entered everything correctly: valve index {0}, flow rate {1}, Target volume {2}, if not press 0 ".format(valve,flow,target))

if boolean != "0":
    print("the script will run")
    exec(open(source).read())

    flow_step_simple(wash)  
    exit_fgt_nicely()
