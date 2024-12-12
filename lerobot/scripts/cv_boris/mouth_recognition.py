import mediapipe as mp
import cv2
import math

# # Initialize MediaPipe Face Mesh and drawing modules
# mp_face_mesh = mp.solutions.face_mesh
# mp_drawing = mp.solutions.drawing_utils

# Initialize the video capture (try changing index if you have multiple cameras)
# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# # Use the Face Mesh model to detect faces in real-time
# with mp_face_mesh.FaceMesh(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7) as face_mesh:
#     while True:
#         ret, frame = cap.read()

#         if not ret:
#             print("Failed to grab frame")
#             break

#         # Resize frame to improve processing speed
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = face_mesh.process(frame_rgb)

#         if results.multi_face_landmarks:
#             for face_landmarks in results.multi_face_landmarks:
#                 # Draw the landmarks on the face
#                 mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS)

#                 # Get the landmarks for the upper and lower lips
#                 # Indices for the upper and lower lips
#                 upper_lip = face_landmarks.landmark[13]  # Upper lip (point 13, not 0)
#                 lower_lip = face_landmarks.landmark[14]  # Lower lip (point 14, not 17)

#                 # Calculate the Euclidean distance between the upper and lower lip landmarks
#                 distance = math.hypot(upper_lip.x - lower_lip.x, upper_lip.y - lower_lip.y)

#                 # Threshold for determining if the mouth is open
#                 if distance > 0.05:  # You can tweak this value for more accurate detection
#                     cv2.putText(frame, "Mouth: Open", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#                 else:
#                     cv2.putText(frame, "Mouth: Closed", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

#         # Show the frame with the mouth status
#         cv2.imshow("Mouth Detection", frame)

#         # Exit on pressing 'q'
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

# # Release the video capture when done
# cap.release()
# cv2.destroyAllWindows()

# Try different GStreamer pipelines if default doesn't work
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# GStreamer pipeline configuration
def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=640,
    display_height=360,
    framerate=30,
    flip_method=0
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        f"width=(int){capture_width}, height=(int){capture_height}, "
        f"format=(string)NV12, framerate=(fraction){framerate}/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (flip_method, display_width, display_height)
    )

# Try first with GStreamer pipeline for CSI camera
cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)

# If GStreamer fails, try USB camera
if not cap.isOpened():
    print("Failed to open camera with GStreamer, trying USB camera...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open USB camera")
        exit()

# Use the Face Mesh model to detect faces in real-time
with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1
    ,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as face_mesh:
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Resize frame to improve processing speed
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Draw the landmarks on the face
                mp_drawing.draw_landmarks(
                    frame,
                    face_landmarks,
                    mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1)
                )

                # Get the landmarks for the upper and lower lips
                upper_lip = face_landmarks.landmark[13]
                lower_lip = face_landmarks.landmark[14]

                # Calculate the Euclidean distance between the upper and lower lip landmarks
                distance = math.hypot(upper_lip.x - lower_lip.x, upper_lip.y - lower_lip.y)

                # Threshold for determining if the mouth is open
                if distance > 0.02:
                
                    cv2.putText(frame, "Mouth: Open", (50, 50),
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, "Mouth: Closed", (50, 50),
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Show the frame with the mouth status
        cv2.imshow("Mouth Detection", frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the video capture when done
cap.release()
cv2.destroyAllWindows()