import cv2
from imutils import face_utils
import numpy as np
import argparse
import imutils
#import dlib
import math
from datetime import datetime

face_cascade = cv2.CascadeClassifier('Cascades/frontal-face.xml')

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
#detector = dlib.get_frontal_face_detector()
#predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def detectFace(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    numfaces = 0
    crop_img = []
    for (x,y,w,h) in faces:
        height, width, na =frame.shape

        y = y - 100
        h = h + 200
        if (y < 0):
            y = 0
        
        if((y +h) > height):

            h = height - (y +1)
        
        x = x - 100
        w = w + 200
        if (x < 0):
            x = 0

        if((x +w) > width):

            x = width - (w + 1)
        
        crop_img.append(frame[y:y+h, x:x+w].copy())

#cv2.imwrite('images/'+str(datetime.now())+'.jpeg',crop_img)

#cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
#   roi_gray = gray[y:y+h, x:x+w]
#       roi_color = frame[y:y+h, x:x+w]
        numfaces = numfaces + 1
        
    return numfaces, crop_img

def head_pose_estimation(image):

    image = imutils.resize(image, width=500)
    size = image.shape
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale image
    rects = detector(gray, 1)

    landmarks = -1

    # loop over the face detections
    for (i, rect) in enumerate(rects):
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        landmarks = face_utils.shape_to_np(shape)

    #2D image points. If you change the image, you need to change vector
    image_points = np.array([
                             (landmarks[33][0], landmarks[33][1]),     # Nose tip
                             (landmarks[57][0], landmarks[57][1]),     # Chin
                             (landmarks[36][0], landmarks[36][1]),     # Left eye left corner
                             (landmarks[45][0], landmarks[45][1]),     # Right eye right corne
                             (landmarks[48][0], landmarks[48][1]),     # Left Mouth corner
                             (landmarks[54][0], landmarks[54][1])      # Right mouth corner
                             ], dtype="double")

    # 3D model points.
    model_points = np.array([
                             (0.0, 0.0, 0.0),             # Nose tip
                             (0.0, -330.0, -65.0),        # Chin
                             (-225.0, 170.0, -135.0),     # Left eye left corner
                             (225.0, 170.0, -135.0),      # Right eye right corne
                             (-150.0, -150.0, -125.0),    # Left Mouth corner
                             (150.0, -150.0, -125.0)      # Right mouth corner
                             
                             ])

    # Camera internals

    focal_length = size[1]
    center = (size[1]/2, size[0]/2)
    camera_matrix = np.array(
                             [[focal_length, 0, center[0]],
                              [0, focal_length, center[1]],
                              [0, 0, 1]], dtype = "double"
                             )

    dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion
    (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=0)


    # Project a 3D point (0, 0, 1000.0) onto the image plane.
    # We use this to draw a line sticking out of the nose


    (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)

#for p in image_points:

#cv2.circle(image, (int(p[0]), int(p[1])), 3, (0,0,255), -1)


    p1 = ( int(image_points[0][0]), int(image_points[0][1]))
    p2 = ( int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))

# cv2.line(image, p1, p2, (255,0,0), 2)

                    
    # Display image
#cv2.imshow("Output", image);
    rotation_value =  math.sqrt(abs(rotation_vector[0]*rotation_vector[0]) + abs(rotation_vector[1]*rotation_vector[0]) + abs(rotation_vector[2]*rotation_vector[2])) * 100

    cv2.imwrite(str(rotation_value)+'.jpeg',image)

    return rotation_value
#cv2.waitKey(0);
