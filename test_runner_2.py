""" 
    an execution of user defined FISH flow steps
"""
#full location of flow_step_FISH_Xinyu.py
source = "C:/Users/790NWL2/Desktop/aigars/Xinyu/scripts/flow_step_FISH_Xinyu.py"

""" EDIT HERE: define steps to use """
wash = {
  "valve_index": 6,
  "flow_rate": 150,
  "target_volume": 20,
  "pause": 1}
not_wash = {
  "valve_index": 6,
  "flow_rate": 100,
  "target_volume": 10,
  "pause": 0}
hyb = {
  "valve_index": 6,
  "flow_rate": 300,
  "target_volume": 10,
  "pause": 0}

""" the next line sources f-ns, leave it be """
exec(open(source).read())


""" EDIT HERE: steps to run """
flow_step_simple(wash)  
flow_step_simple(not_wash)  
flow_step_simple(hyb)  


""" leave me be"""
exit_fgt_nicely()
