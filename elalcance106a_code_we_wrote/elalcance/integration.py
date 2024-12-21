import subprocess
from pynput import keyboard
from elalcance.mouth_recog import mouth_open_activate

## Teleoperation
def run_teleoperation(teleoperate_command):
    """Run the teleoperation command."""
    print("Starting teleoperation...")
    try:
        subprocess.run(teleoperate_command, shell=True, check=True)
        print("Teleoperation finished successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during teleoperation: {e}")
        raise

## Mouth Recognition 
def run_mouth_recognition(mouth_recognition_path):
    """Run the mouth recognition script."""
    print("Starting mouth recognition...")
    try:
        subprocess.run(f"python {mouth_recognition_path}", shell=True, check=True)
        print("Mouth recognition finished successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during mouth recognition: {e}")
        raise

## Episode recording and replay
def record_episode(record_command):
    """Run the command to record an episode."""
    print("Starting episode recording...")
    try:
        subprocess.run(record_command, shell=True, check=True)
        print("Episode recording finished successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during episode recording: {e}")
        raise

def replay_episode(replay_command):
    """Run the command to replay an episode."""
    print("Replaying an episode...")
    try:
        subprocess.run(replay_command, shell=True, check=True)
        print("Episode replay finished successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during episode replay: {e}")
        raise


## On press for commands 
def on_press(key, teleoperate_command, record_command, mouth_recognition_path, replay_command):
    """Handle key press events."""
    try:
        if key.char == 't':
            print("Teleoperation selected.")
            run_teleoperation(teleoperate_command)
            return False  # Stop listener
        elif key.char == 'r':
            print("Episode recording selected.")
            record_episode(record_command)
            return False  # Stop listener
        elif key.char == 'm':
            print("Mouth recognition selected.")
            run_mouth_recognition(mouth_recognition_path)
            return False  # Stop listener
        elif key.char == 'p':
            print("Episode replay selected.")
            replay_episode(replay_command)
            return False  # Stop listener
        elif key.char == 'd':
            print("Mouth Open Teleoperation selected.")
            if mouth_open_activate():
                print("Mouth is open! Starting teleoperation...")
                run_teleoperation(teleoperate_command)
            else:
                print("Mouth is not open. Teleoperation aborted.")
            return False  # Stop listener
        elif key.char == 'f':
            print("Mouth Open Replay selected.")
            if mouth_open_activate():
                print("Mouth is open! Starting replay...")
                replay_episode(replay_command)
            else:
                print("Mouth is not open. Replay aborted.")
            return False  # Stop listener
        elif key.char == 'q':
            print("Exiting the program.")
            return False  # Stop listener
    except AttributeError:
        pass

def main():
    # Commands
    teleoperate_command = (
        "python lerobot/scripts/control_robot.py teleoperate \
        --robot-path lerobot/configs/robot/so100.yaml \
        --robot-overrides '~cameras' \
        --display-cameras 0"
    )

    record_command = (
        "python lerobot/scripts/control_robot.py record \
        --robot-path lerobot/configs/robot/so100.yaml\
        --fps 30\
        --repo-id francescocrivelli/demo_recording1\
        --tags so100tutorial\
        --warmup-time-s 2\
        --episode-time-s 20\
        --reset-time-s 5\
        --num-episodes 1\
        --push-to-hub 1\
        --single-task 'demo recording'\
        --robot-overrides '~cameras'"
    )

    replay_command = (
        "python lerobot/scripts/control_robot.py replay \
    --robot-path lerobot/configs/robot/so100.yaml \
    --repo-id francescocrivelli/demo_recording1 \
    --fps 30 \
    --episode 0 \
    --robot-overrides '~cameras'" 
    )

    print("""Choose an action:
[t] Teleoperation
[m] Mouth Recognition
[r] Record an Episode
[p] Replay an Episode
[d] Teleoperation with Mouth Activation
[f] Replay with Mouth Activation
[q] Quit""")


    # Path to the mouth recognition script
    mouth_recognition_path = "lerobot/scripts/elalcance/mouth_recognition.py"

    with keyboard.Listener(
        on_press=lambda key: on_press(key, teleoperate_command, record_command, mouth_recognition_path, replay_command)) as listener:
        listener.join()

if __name__ == "__main__":
    main()
