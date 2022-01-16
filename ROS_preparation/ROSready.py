
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:ActivityRC_1":
    rospy.loginfo("Task release component with the ID: RC_1 in progress.") #useful info for the debugger
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
    rospy.loginfo("Task release component with the ID RC_1 has been executed.")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")        
        
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:ActivityGC_1":  
        rospy.loginfo("Task grasp component with vacuum gripper with the ID: GC_1 in progress.")
        # Here goes the action calling for the precise task definition
        gripperGraspGoal = fmp_gripper_action.msg.gripperGoal(grasp=True, speed=20, force=1, distance=40, activatemodule=False, modulestrenght=255)
        Activity_name = taskDefinition["object"][-16:]
        Activity = activity(Activity_name)
        # Sends the goal to the action server.
        self.gripperActuation.send_goal(gripperGraspGoal, feedback_cb = Activity._feedbackCB, 
            done_cb = Activity._resultCB)
        self.activeActivity = Activity
        rospy.loginfo("Task grasp component with vacuum gripper with the ID GC_1 has been executed.")
        taskStatus["value"] = "inProgress"
        taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:ActivityMH":  
    rospy.loginfo("Task reach the tray with the ID: MH in progress.")
    # Here goes the action calling for the precise task definition
    gripperGraspGoal = fmp_gripper_action.msg.gripperGoal(grasp=False, speed=20, force=1, distance=40, activatemodule=False, modulestrenght=255)
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.gripperActuation.send_goal(gripperGraspGoal, feedback_cb = Activity._feedbackCB, 
        done_cb = Activity._resultCB)
    self.activeActivity = Activity
    rospy.loginfo("Task reach the tray with the ID: MH has been executed.")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:ActivityMH":
    rospy.loginfo("Task reach the tray with the ID: MH and nut object: TR-22 in progress.")
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
    rospy.loginfo("Task reach the tray with the ID: MH and nut object: TR-22 has been executed.")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                