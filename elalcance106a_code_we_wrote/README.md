# Project Name
El Alcance

## Description
We designed for the elacnace folder to be run under lerobot/scripts folder, import this folder over to use its functionalities.

## Features
The elalcance folder contains five files in total, the .pycache and __init__.py files allow for functions created within this folder to be exported and executable. The mouth_recognition.py file provides a window for a live demonstration of the code used for implementing the mesh for mouth-open detection, and mouth_recog.py turns the code into a exportable function named mouth_open_activate which returns a boolean value, only giving a True output when it detects a mouth being open. Otherwise, when the mouth remains closed the original state of the program continues to run.  We also wrote a python script integration.py that creates an interface to integrate all of the various features we wanted to include for our robot system. The idea is that with all of the various commands and functions that needed to be executed, we wanted to streamline and consolidate them into a single script such that it would be easier for use by both future developers and caretakers of the beneficiaries alike. The script aims to use keyboard inputs rather than typed words to execute commands in the lerobot environment, while also integrating our created computer vision algorithms for mouth-open sensing. 

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
