# import the necessary packages
import sys
sys.path.append(".")
sys.path.append(r"D:\Main project-2\automatic-classroom-attendance-system-master")

from face_recognizer.detect_faces import face_detection
from imutils.video import VideoStream
from datetime import datetime
from imutils import paths
import face_recognition
import pandas as pd
import imutils
import pickle
import time
import cv2
import os

class FaceRecognizer():
    def __init__(self, prototxt, model):
        self.prototxt = prototxt
        self.model = model

    def encodeFace(self, image):
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        (boxes, confidences) = face_detection(image, self.prototxt, self.model)
        boxes = [(box[1], box[2], box[3], box[0]) for (i, box) in enumerate(boxes)]
        encodings = face_recognition.face_encodings(rgb, boxes)
        return (boxes, encodings)

    def matchFace(self, encodings, data, faceCounter):
        names = []
        for encoding in encodings:
            matches = face_recognition.compare_faces(
                data["encodings"], encoding, tolerance=0.5)
            name = "Unknown"
            if True in matches:
                matchIdxs = [i for (i, match) in enumerate(matches) if match]
                counts = {}
                for i in matchIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                name = max(counts, key=counts.get)
                faceCounter[name] = faceCounter.get(name, 0) + 1
            names.append(name)
        return names

    def drawFaceBB(self, image, boxes, names, ratio = 1):
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # resize the bounding boxes
            top = int(top * ratio)
            right = int(right * ratio)
            bottom = int(bottom * ratio)
            left = int(left * ratio)

            # draw the predicted face name on the frame
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (0, 255, 0), 2)
        return image

if __name__ == "__main__":
    # Specify file paths
    prototxt_path = r"D:\Main project-2\automatic-classroom-attendance-system-master\model\deploy.prototxt.txt"
    model_path = r"D:\Main project-2\automatic-classroom-attendance-system-master\model\res10_300x300_ssd_iter_140000.caffemodel"
    encodings_path = r"D:\Main project-2\automatic-classroom-attendance-system-master\output\encodings2.pickle"
    csv_path = r"D:\Main project-2\automatic-classroom-attendance-system-master\output\attendance.csv"
    output_path = r"D:\Main project-2\automatic-classroom-attendance-system-master\output\webcam_face_recognition.avi"

    # instanciate face recognizer
    faceRecognizer = FaceRecognizer(prototxt_path, model_path)

    # load face encodings
    print("[INFO] loading encodings...")
    data = pickle.loads(open(encodings_path, "rb").read())

    # initialize face occurrence counters
    faceCounter = {name: 0 for name in data["names"]}

    # start video stream and warm up the camera
    print("[INFO] start video stream...")
    vs = VideoStream(src=0).start()
    writer = None
    time.sleep(2)

    while True:
        # load current frame 
        frame = vs.read()

        # ensure frame is not None
        if frame is None:
            break

        # resize frame and convert it to rgb color
        frame = imutils.resize(frame, width=750)
        ratio = frame.shape[1] / float(frame.shape[1])

        (boxes, encodings) = faceRecognizer.encodeFace(frame)
        names = faceRecognizer.matchFace(encodings, data, faceCounter)
        frame = faceRecognizer.drawFaceBB(frame, boxes, names, ratio)

        # save the frame
        if writer is None and output_path is not None:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            writer = cv2.VideoWriter(output_path, fourcc, 20.0, (frame.shape[1], frame.shape[0]), True)

        if writer is not None:
            writer.write(frame)

        # show the output frame
        cv2.imshow("frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    # append current attendance result to the dataframe
    faceCounter = {key: 1 if value >= 30 else 0 for (key, value) in faceCounter.items()}
    date_col = datetime.now().strftime("%Y-%m-%d %H:%M")
    df = pd.read_csv(csv_path, index_col=0)
    df[date_col] = df["names"].map(lambda name: faceCounter[name])
    print(df)

    # cleaning up
    print("[INFO] cleaning up")
    cv2.destroyAllWindows()
    vs.stop()

    # save the frame
    if writer is None and output_path is not None:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(output_path, fourcc, 20.0, (frame.shape[1], frame.shape[0]), True)

# Futur works
# TODO: add face alignmnt
# TODO: use only a single image of a person for registration.
# TODO: improve the face detection model or use other model.
# TODO: add image enhancement feature
