# Usage of Natural Language Processing to facilitate robot programming in ROS

Project Laboratory Human Centered Robotics Winter Semester 2021-2022 at Technical University Munich

by Cheng Yan, Kinga Bernacka (Supervisor: Matteo Pantano)



## Overview

This code is developed to



## Initialization

Before using our main.py, we must upload the pre-defined files (Commands to operate the robot) first because of the usage of GPT-3. Then we will get a file ID which could be used in search function of GPT-3. 

The initial file ID of our pre-defined commands to operate the robot is "file-xJ3fKj2VDatppSg23ZxZb4oI". We defined 5 example primitive: "move/reach", "Connect", "Change", "Compare", "Collaboration".

*If we meet some problem with the similarity scores later, do not forget to modify the pre-defined file with more content. 



## Model Selection

Since we don't have any samples for model training at all, we can only use the GPT-3 Model, which performs well in zero-shot learning. Maybe in the follow-up work, we can obtain a small amount of sample data, after which we may be able to test a variety of different models and do some fine-tuning in the future. 
