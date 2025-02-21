import numpy as np
import argparse
import imutils
import time
import cv2


def face_detection(image, prototxt, model, min_confidence=0.5):
    (h, w) = image.shape[:2]

    # note: we need to resize to image to the desired size
    resized = cv2.resize(image, (300, 300))
    blob = cv2.dnn.blobFromImage(resized, scalefactor=1.0, size=(
        300, 300), mean=(104.0, 177.0, 123.0))

    # load the pretrained model
    net = cv2.dnn.readNetFromCaffe(prototxt, model)

    # pass the processed image through the network
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    boxes = []
    confidences = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > min_confidence:
            # get the bounding box
            box = detections[0, 0, i, 3:7]*np.array([w, h, w, h])
            boxes.append(box.astype("int"))
            confidences.append(confidence)

    return boxes, confidences


if __name__ == "__main__":
    image_path = r"D:\Main project-2\automatic-classroom-attendance-system-master\dataset\aman\IMG_20200907_082833.jpg"
    prototxt_path = r"D:\Main project-2\automatic-classroom-attendance-system-master\model\deploy.prototxt.txt"
    model_path = r"D:\Main project-2\automatic-classroom-attendance-system-master\model\res10_300x300_ssd_iter_140000.caffemodel"
    min_confidence = 0.5

    start = time.time()
    (image, boxes, confidences) = face_detection(image_path, prototxt_path, model_path, min_confidence)

    for ((startX, startY, endX, endY), confidence) in zip(boxes, confidences):
        cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
        text = "{:.2f}".format(confidence * 100)
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.putText(image, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    end = time.time()
    print("[INFO] Face detection took: {:.2f} seconds".format(end - start))

    cv2.imshow("Face Detection", image)
    cv2.waitKey(0)
