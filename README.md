# Project Name
El Alcance

## Table of Contents
- [Description](#description)
- [Acknowledgement](#acknowledgement)
- [Setup](#setup)
- [Features](#features)
- [integration.py Key Functions](#integrationpy-key-functions)
- [Link to Project Report](#link-to-project-report)
- [Citation](#citation)


## Description
Our project involves a collaboration with Tukuypaj, a non-profit organization supporting numerous underserved communities in Chile. We learnt that the organization is often short-staffed in having available personnel to feed their quadriplegic community during mealtimes. Therefore, our primary project objective was to build a robotic system that can help reach for food and feed quadriplegic beneficiaries. 

We repurposed the SOARM-100 robotic arm, allowing caretakers to record feeding trajectories that the system can replicate. Using computer vision, a camera sensor allows the robotics system to respond to the beneficiaries’ facial expressions to actuate the trajectory. Additionally, we incorporated reinforcement learning to enable the robot to adapt to dynamic situations, such as handling different types of food and varying positions between the food and the beneficiary's mouth. This approach aims to create a system with generalized intelligence, capable of providing a reliable and versatile feeding solution. 

Our long-term vision is to create a fully autonomous system that the beneficiaries can use independently, with the ability to replicate this system to operate at scale and improve the lives of many others. 

## Acknowledgement 
Our work builds off the incredible community who have built out the frameworks and infrastructure for the SOARM-100, lerobot and huggingface environments:
- Thanks to TheRobotStudio, Jess Moss, Remi Cadene, Simon Alibert for creating the hardware guide for setting up the SOARM-100
- Thanks to Remi Cadene, Simon Alibert, Alexander Soare, Quentin Gallouedec, Adil Zouitine and Thomas Wolf for creating the lerobot and huggingface software infrastructure for gathering data on trajectories and creating the frameworks that enable robot learning.
- Thanks to Sitarama Raju Chekuri, whom executed a robot learning project with the Koch V1.1 arm, whose implementation we studied closely in understanding proper robot learning research practices and in emulating them for our project 

## Setup 
Our project builds off from the SOARM-100 github repo and the lerobot github repo, where further details on the setup and walkthrough can be found on the following github repositories:
[1] TheRobotStudio, Moss, J., Cadene, R., & Alibert, S. (2024). TheRobotStudio/so-ARM100: Standard open arm 100. SO-ARM100. https://github.com/TheRobotStudio/SO-ARM100
[2] Alibert, S., Cadene, R., Soare, A., Gallouedec, Q., Zouitine, A., & Wolf, T. (2024). Lerobot/examples/10_use_so100.md at main · Huggingface/lerobot. LeRobot: State-of-the-art Machine Learning for Real-World Robotics in Pytorch. https://github.com/huggingface/lerobot

## Features
This section will primarily focus on the features we built out ourselves that apply specifically to our project needs. 

Originally, we tried creating various CAD designs of spoon holders that would enable the SO-ARM100’s end effector to latch onto, the initial idea being that with spoon inserted into the holder, we’d use the SOARM-100’s mechanics to manually pick up the spoon holder, scoop up food from a bowl, before bringing it to the beneficiary. However, in testing this idea we noticed that executing motions via this approach was highly inconsistent. It was either that the gripper could not latch onto the spoon holder securely, or the spoon holder would move erratically once being picked up. We realized that redesigning the gripper joints of the SOARM-100 to directly incorporate a spoon holder would be the best approach. However, given that we were facing a tight deadline we were not able to change the end effector of the follower arm for this purpose. The CAD files of the spoon/fork holder that we designed with Fusion360 can be found in the *elalcance106a_additional_materials* folder.

For the data collection aspect of the project, we learnt a lot from Chekuri's implementation using the Koch arm, where he designed his data collection setup to include a camera at the gripper of the follower arm. We learnt the need of putting a camera right next to the gripper to ensure that we could gather camera data of the gripper opening and closing, and decided to incoporate that into our data collection setup. Adapting his design for a camera holder, we used an extended base to fit the broader size on the gripper of the follower arm of the SOARM-100, and measured for and incorporated holes to ensure that it would not cover screw holes meant to secure the servos to the joint. The created stl file, alongside a datasheet for all of the materials that we used to create the SOARM-100 and this data collection setup, are included in the same *elalcance106a_additional_materials* folder.

Additionally we also wrote our own software to consolidate the various functions we wanted our robotic system to perform, incorporating the mouth-activation element of our project into the process. The created folder of our written code, *elalcance*, can be found in the *elalcance106a_code_we_wrote* folder. To execute the functions of the folder, it would first need to be moved to be under the lerobot/scripts directory. 

The *elalcance* folder contains five files in total, the .pycache and __init__.py files allow for functions created within this folder to be exported and executable. The mouth_recognition.py file provides a window for a live demonstration of the code used for implementing the mesh for mouth-open detection, and mouth_recog.py turns the code into a exportable function named mouth_open_activate which returns a boolean value, only giving a True output when it detects a mouth being open. Otherwise, when the mouth remains closed the original state of the program continues to run.  We also wrote a python script integration.py that creates an interface to integrate all of the various features we wanted to include for our robot system. The idea is that with all of the various commands and functions that needed to be executed, we wanted to streamline and consolidate them into a single script such that it would be easier for use by both future developers and caretakers of the beneficiaries alike. The script aims to use keyboard inputs rather than typed words to execute commands in the lerobot environment, while also integrating our created computer vision algorithms for mouth-open sensing. 

## integration.py Key Functions
The following table details the functions of each inserted key:

| Key | Function |
|-----|----------|
| `t` | Executes Python terminal command for teleoperation in the `lerobot` environment. |
| `m` | Shows window display of written mouth recognition software in action. Changes made to boundary conditions and limits for mouth-open detection written in software can be directly tested on this platform. |
| `r` | Executes Python terminal command for recording episodes in the `lerobot` environment. |
| `p` | Executes Python terminal command for replaying recorded episodes in the `lerobot` environment. |
| `d` | Integrated logic such that the teleoperation function of the SOARM-100 would only occur when a camera sensor detects that a mouth has been opened. |
| `f` | Integrated logic such that the replay of a recorded episode of the trajectory of the SOARM-100 would only occur when a camera sensor detects that a mouth has been opened. |
| `q` | Quit the program. |

To run the file, you would need to navigate to the lerobot directory and run the following command:
```bash
python lerobot/scripts/elalcance/integration.py
```

## Link to Project Report
https://www.francescocrivelli.com/alcance/index.html

## Citation
If you use our work or find it helpful, please cite us using the following BibTeX entry:

```bibtex
@misc{crivelli2024lealcance,
        author = {Francesco C., Bryan S., Claire B., and Boris},
        title = {Le-Alcance: A Fork of LeRobot for Low-Cost Robotic Learning},
        howpublished = "\url{https://github.com/francescocrivelli/le-alcance}",
        year = {2024}
}
```