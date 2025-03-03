import cv2
import numpy as np
from time import sleep
import os

# Minimum width and height thresholds for a detected object to be considered a vehicle
min_width = 80
min_height = 80

# Offset value used to determine the detection line's range
offset = 10

# Vertical positions of the detection lines in the video frame
line_positions = [100, 200, 300, 550]

# Delay (in milliseconds) between processing each frame
delay = 50

# List to store the detected objects (vehicles)
detections = []

# Counter to keep track of the number of detected vehicles
cars_count = 0

# Video source input
cap = cv2.VideoCapture('tracking_3.avi')

# Create background subtractor
subtraction = cv2.createBackgroundSubtractorMOG2()

# Get the width, height, and frames per second (fps) of the input video
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for mp4
output_video_path = 'output_video.avi'
out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

# Initialize line color
line_color = (0, 255, 0)  # Initial color is green

while True:
    # Read a frame from the video capture
    ret, frame = cap.read()
    if not ret:
        break

    # Introduce a delay to control the processing speed
    sleep(1 / delay)

    # Convert the frame to grayscale and apply Gaussian blur to reduce noise
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 5)

    # Apply background subtraction to detect moving objects
    img_sub = subtraction.apply(blur)

    # Dilate the image to fill gaps in between object contours
    dilated = cv2.dilate(img_sub, np.ones((5, 5)))

    # Apply morphological operations to further refine the detected objects
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilated = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    dilated = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

    # Find contours in the dilated image
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw detection lines on the frame
    for line_position in line_positions:
        cv2.line(frame, (0, line_position), (frame.shape[1], line_position), line_color, 2)

    # Iterate through each contour
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # Check if the contour meets the minimum size requirements
        if w >= min_width and h >= min_height:
            # Store the coordinates of the detected object
            detections.append((x, y, w, h))
            # Draw a rectangle around the detected object
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Iterate through the stored detections
    for (x, y, w, h) in detections:
        # Check if the object intersects with any of the detection lines
        for line_position in line_positions:
            if (y < line_position + offset) and (y > line_position - offset):
                # Change line color to orange
                line_color = (0, 127, 255)
                # Increment the vehicle count
                cars_count += 1
                # Print the current vehicle count
                print("No. of cars detected:", cars_count)
                # Remove the detected object from the list
                detections.remove((x, y, w, h))  # to ensure no duplicates
                break
            else:
                # If no object intersects with the line, revert the line color to green
                line_color = (0, 255, 0)

    # Write the processed frame to the output video
    out.write(frame)

    # Display the processed frame
    cv2.imshow("Video Original", frame)

    # Break the loop if the 'Esc' key is pressed
    if cv2.waitKey(1) == 27:
        break

# Release the video capture and writer objects and close all OpenCV windows
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Output video saved to {output_video_path}")
