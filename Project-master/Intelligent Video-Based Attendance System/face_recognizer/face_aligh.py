import face_recognition
import numpy as np
import cv2

def alignFace(image, face_locations, face_landmarks):
    # Find the bounding box coordinates of the face
    (top, right, bottom, left) = face_locations

    # Calculate the center of the face
    face_center = ((left + right) // 2, (top + bottom) // 2)

    # Calculate the angle
    leftEyePts = face_landmarks['left_eye']
    rightEyePts = face_landmarks['right_eye']
    leftEyeCenter = np.array(leftEyePts).mean(axis=0).astype("int")
    rightEyeCenter = np.array(rightEyePts).mean(axis=0).astype("int")
    dY = rightEyeCenter[1] - leftEyeCenter[1]
    dX = rightEyeCenter[0] - leftEyeCenter[0]
    angle = np.degrees(np.arctan2(dY, dX))

    # Set desired left eye location
    desiredLeftEye = (0.35, 0.35)
    # Set the cropped image (face) size after rotation
    desiredFaceWidth = 128
    desiredFaceHeight = 128

    # Determine the scale of the new resulting image
    dist = np.sqrt((dX ** 2) + (dY ** 2))
    desiredDist = (1.0 - desiredLeftEye[0]) * desiredFaceWidth
    scale = desiredDist / dist

    # Calculate the rotation matrix
    M = cv2.getRotationMatrix2D(face_center, angle, scale)

    # Update the translation component of the matrix
    tX = desiredFaceWidth * 0.5
    tY = desiredFaceHeight * desiredLeftEye[1]
    M[0, 2] += (tX - face_center[0])
    M[1, 2] += (tY - face_center[1])

    # Apply the affine transformation
    output = cv2.warpAffine(image, M, (desiredFaceWidth, desiredFaceHeight), flags=cv2.INTER_CUBIC)

    return output



if __name__ == "__main__":
    # Path to the input image
    image_path = r"D:\Main project-2\automatic-classroom-attendance-system-master\dataset\rahul\00000.png"

    # Load image and find face locations
    image = cv2.imread(image_path)
    face_locations = face_recognition.face_locations(image, model="hog")
    
    # Detect 68 landmarks from image. This includes left eye, right eye, lips, eyebrows, nose, and chin
    face_landmarks = face_recognition.face_landmarks(image)

    for i in range(len(face_locations)):
        # Align faces
        faceAligned = alignFace(image, face_locations[i], face_landmarks[i])
            
        # Display the output images
        cv2.imshow("Original", image)
        cv2.imshow("Aligned", faceAligned)
        cv2.waitKey(0)
