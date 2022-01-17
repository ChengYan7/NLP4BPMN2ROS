import json

my_file = open("ROSready.py", "w")
f = open('GPT3_out.json') #GPT-3 output file with activities
data = json.load(f)
 
def substitute(act_name, act_id, obj_name, obj_id, primitive):
    if (obj_name == "2 finger gripper"):
        finger_gripper = True; 
        act_module = False; 
    elif (obj_name=="vacuum gripper"):
        finger_gripper = False; 
        act_module = True; 
    else: 
        #default values
        finger_gripper = False; 
        act_module = False; 

  # MOVE/REACH with screw object
    if((primitive=="move" or primitive =="reach") and obj_name=="screw"):
        print("move/reach + screw")
        my_file.write(f"""
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activity{act_id}":
    rospy.loginfo("Task {act_name} with the ID: {act_id} in progress.") #useful info for the debugger
    # Here goes the action calling for the precise task definition
    moveTrajGoal = fmp_move_traj.msg.ExecuteMotionPlannerGoal(execute_motion = True, change_planner = True, planner = "fmpur10withgripper_s",
        position_x={obj_name}.x, 
        position_y={obj_name}.y, 
        position_z={obj_name}.z,
        change_orientation= False)  
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.moveTrajClient.send_goal(moveTrajGoal, feedback_cb = Activity._feedbackCB, 
        done_cb = Activity._resultCB)
    self.activeActivity = Activity
    rospy.loginfo("Task {act_name} with the ID {act_id} has been executed.")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")        
        """)
        
    if(primitive=="grasp"):
        print("grasp")
        # GRASP
        # If the object connected is a 2 finger gripper the parameter to be changes is "grasp"
        # if it is something else the parameter to be changed is "activatemodule"
        my_file.write(f"""
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activity{act_id}":  
        rospy.loginfo("Task {act_name} with the ID: {act_id} in progress.")
        # Here goes the action calling for the precise task definition
        gripperGraspGoal = fmp_gripper_action.msg.gripperGoal(grasp={finger_gripper}, speed=20, force=1, distance=40, activatemodule={act_module}, modulestrenght=255)
        Activity_name = taskDefinition["object"][-16:]
        Activity = activity(Activity_name)
        # Sends the goal to the action server.
        self.gripperActuation.send_goal(gripperGraspGoal, feedback_cb = Activity._feedbackCB, 
            done_cb = Activity._resultCB)
        self.activeActivity = Activity
        rospy.loginfo("Task {act_name} with the ID {act_id} has been executed.")
        taskStatus["value"] = "inProgress"
        taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        """)

        # UNGRASP
        # If the object connected is a 2 finger gripper the parameter to be changes is "grasp"
        # if it is something else the parameter to be changed is "activatemodule"
    if(primitive=="ungrasp"):    
        print("ungrasp")
        my_file.write(f"""
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activity{act_id}":  
    rospy.loginfo("Task {act_name} with the ID: {act_id} in progress.")
    # Here goes the action calling for the precise task definition
    gripperGraspGoal = fmp_gripper_action.msg.gripperGoal(grasp={finger_gripper}, speed=20, force=1, distance=40, activatemodule={act_module}, modulestrenght=255)
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.gripperActuation.send_goal(gripperGraspGoal, feedback_cb = Activity._feedbackCB, 
        done_cb = Activity._resultCB)
    self.activeActivity = Activity
    rospy.loginfo("Task {act_name} with the ID: {act_id} has been executed.")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            """)

        # MOVE/REACH wit nut object
    if((primitive=="move" or primitive =="reach") and obj_name=="nut"):
            print("move/reach + nut")
            my_file.write(f"""
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activity{act_id}":
    rospy.loginfo("Task {act_name} with the ID: {act_id} and nut object: {obj_id} in progress.")
    # Here goes the action calling for the precise task definition
    moveTrajGoal = fmp_move_traj.msg.ExecuteMotionPlannerGoal(execute_motion = True, change_planner = True, planner = "fmpur10withgripper_s",
        position_x={obj_name}.x, 
        position_y={obj_name}.y, 
        position_z={obj_name}.z,
        change_orientation= False)  
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.moveTrajClient.send_goal(moveTrajGoal, feedback_cb = Activity._feedbackCB, 
        done_cb = Activity._resultCB)
    self.activeActivity = Activity
    rospy.loginfo("Task {act_name} with the ID: {act_id} and nut object: {obj_id} has been executed.")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                """)
      
for i in data['activities']:
    substitute(i['act_name'], i['act_id'], i['obj_name'], i['obj_id'], i['primitive'])      
    #substitute(act_name, act_id, obj_name, obj_id, primitive):  

my_file = open("ROSready.py")
content = my_file.read()
my_file.close()

