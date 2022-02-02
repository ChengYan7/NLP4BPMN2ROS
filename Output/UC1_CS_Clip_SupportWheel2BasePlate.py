
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activityactivity_11fiqbb":  
    rospy.loginfo("Task reach supportwheel with the ID: activity_11fiqbb in progress.")
    # Here goes the action calling for the precise task definition
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.activeActivity = Activity
    rospy.loginfo("Task reach supportwheel with the ID activity_11fiqbb has been executed.")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") 
    
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activityactivity_1uwgc5r":  
    rospy.loginfo("Task grasp support wheel with the ID: activity_1uwgc5r in progress.")
    # Here goes the action calling for the precise task definition
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.activeActivity = Activity
    rospy.loginfo("Task grasp support wheel with the ID activity_1uwgc5r has been executed.")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") 
    
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activityactivity_03afyx2":  
    rospy.loginfo("Task clip support wheel with the ID: activity_03afyx2 in progress.")
    # Here goes the action calling for the precise task definition
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.activeActivity = Activity
    rospy.loginfo("Task clip support wheel with the ID activity_03afyx2 has been executed.")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") 
    
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activityactivity_03afyx2":  
    rospy.loginfo("Task clip support wheel with the ID: activity_03afyx2 in progress.")
    # Here goes the action calling for the precise task definition
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.activeActivity = Activity
    rospy.loginfo("Task clip support wheel with the ID activity_03afyx2 has been executed.")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") 
    