
# AVAILABLE OBJECTS
screw
nut


# MOVE/REACH with screw object
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activity_XXXXXX":
    rospy.loginfo("XXXXXXXXX")
    # Here goes the action calling for the precise task definition
    moveTrajGoal = fmp_move_traj.msg.ExecuteMotionPlannerGoal(execute_motion = True, change_planner = True, planner = "fmpur10withgripper_s",
        position_x=screw.x, 
        position_y=screw.y, 
        position_z=screw.z,
        change_orientation= False)  
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.moveTrajClient.send_goal(moveTrajGoal, feedback_cb = Activity._feedbackCB, 
        done_cb = Activity._resultCB)
    self.activeActivity = Activity
    rospy.loginfo("XXXXXXXXXXXXXXXXXX")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

# GRASP
# If the object connected is a 2 finger gripper the parameter to be changes is "grasp"
# if it is something else the parameter to be changed is "activatemodule"
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activity_XXXX":  
    rospy.loginfo("I am the task for the GRASP of the part")
    # Here goes the action calling for the precise task definition
    gripperGraspGoal = fmp_gripper_action.msg.gripperGoal(grasp=False, speed=20, force=1, distance=40, activatemodule=True, modulestrenght=255)
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.gripperActuation.send_goal(gripperGraspGoal, feedback_cb = Activity._feedbackCB, 
        done_cb = Activity._resultCB)
    self.activeActivity = Activity
    rospy.loginfo("XXXXXXXXXX")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

# UNGRASP
# If the object connected is a 2 finger gripper the parameter to be changes is "grasp"
# if it is something else the parameter to be changed is "activatemodule"
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activity_XXXX":  
    rospy.loginfo("I am the task for the GRASP of the part")
    # Here goes the action calling for the precise task definition
    gripperGraspGoal = fmp_gripper_action.msg.gripperGoal(grasp=False, speed=20, force=1, distance=40, activatemodule=False, modulestrenght=255)
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.gripperActuation.send_goal(gripperGraspGoal, feedback_cb = Activity._feedbackCB, 
        done_cb = Activity._resultCB)
    self.activeActivity = Activity
    rospy.loginfo("XXXXXXXXXX")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

# MOVE/REACH wit nut object
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activity_XXXXXX":
    rospy.loginfo("XXXXXXXXX")
    # Here goes the action calling for the precise task definition
    moveTrajGoal = fmp_move_traj.msg.ExecuteMotionPlannerGoal(execute_motion = True, change_planner = True, planner = "fmpur10withgripper_s",
        position_x=nut.x, 
        position_y=nut.y, 
        position_z=nut.z,
        change_orientation= False)  
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.moveTrajClient.send_goal(moveTrajGoal, feedback_cb = Activity._feedbackCB, 
        done_cb = Activity._resultCB)
    self.activeActivity = Activity
    rospy.loginfo("XXXXXXXXXXXXXXXXXX")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
