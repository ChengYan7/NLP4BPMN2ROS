
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activityactivity_0koa7o9":  
    rospy.loginfo("Task reach baseplate with the ID: activity_0koa7o9 in progress.")
    # Here goes the action calling for the precise task definition
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.activeActivity = Activity
    rospy.loginfo("Task reach baseplate with the ID activity_0koa7o9 has been executed.")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") 
    
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activityactivity_0ebmhpg":  
    rospy.loginfo("Task grasp baseplate with the ID: activity_0ebmhpg in progress.")
    # Here goes the action calling for the precise task definition
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.activeActivity = Activity
    rospy.loginfo("Task grasp baseplate with the ID activity_0ebmhpg has been executed.")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") 
    
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activityactivity_0ebmhpg":  
    rospy.loginfo("Task grasp baseplate with the ID: activity_0ebmhpg in progress.")
    # Here goes the action calling for the precise task definition
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.activeActivity = Activity
    rospy.loginfo("Task grasp baseplate with the ID activity_0ebmhpg has been executed.")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") 
    
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activityactivity_1cwx7p7":  
    rospy.loginfo("Task move baseplate with the ID: activity_1cwx7p7 in progress.")
    # Here goes the action calling for the precise task definition
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.activeActivity = Activity
    rospy.loginfo("Task move baseplate with the ID activity_1cwx7p7 has been executed.")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") 
    
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activityactivity_1cwx7p7":  
    rospy.loginfo("Task move baseplate with the ID: activity_1cwx7p7 in progress.")
    # Here goes the action calling for the precise task definition
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.activeActivity = Activity
    rospy.loginfo("Task move baseplate with the ID activity_1cwx7p7 has been executed.")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") 
    
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activityactivity_02ig9gu":  
    rospy.loginfo("Task release baseplate with the ID: activity_02ig9gu in progress.")
    # Here goes the action calling for the precise task definition
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.activeActivity = Activity
    rospy.loginfo("Task release baseplate with the ID activity_02ig9gu has been executed.")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") 
    
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activityactivity_02ig9gu":  
    rospy.loginfo("Task release baseplate with the ID: activity_02ig9gu in progress.")
    # Here goes the action calling for the precise task definition
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.activeActivity = Activity
    rospy.loginfo("Task release baseplate with the ID activity_02ig9gu has been executed.")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") 
    