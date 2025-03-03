# OpenCv-Counting-cars-
Code Explanation
This code detects and tracks vehicles in a video using OpenCV. Here's a breakdown of how it works:

Video Input: It loads a video file (....) and processes each frame.
Motion Detection: It applies Background Subtraction to detect moving objects.
Image Processing:
Converts frames to grayscale.
Applies Gaussian Blur to reduce noise.
Object Detection:
Detects moving objects using cv2.findContours().
Draws bounding boxes around detected objects that exceed a certain size (assumed to be vehicles).
Line Detection & Vehicle Counting:
Draws detection lines at specific positions in the frame.
When a vehicle crosses a line, the car counter (cars_count) is incremented.
The detection line color changes to orange when a vehicle crosses it and reverts to green otherwise.
Video Output:
Saves the processed video (output_video.avi) with bounding boxes and detection lines.
Displays the processed frames in real-time.
Exit Condition:
The program terminates when the Esc key (27) is pressed.
