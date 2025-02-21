# import the necessary packages
import sys
sys.path.append(".")
sys.path.append(r"D:\Main project-2\automatic-classroom-attendance-system-master")

# import the necessary packages
import cv2
import pickle
import face_recognition
import time

# Load face encodings
print("[INFO] Loading encodings...")
data = pickle.loads(open(r"D:\Main project-2\automatic-classroom-attendance-system-master\output\encodings2.pickle", "rb").read())

# Load input image
image = cv2.imread(r"D:\Main project-2\automatic-classroom-attendance-system-master\dataset\rahul\00000.png")
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Recognizing faces
print("[INFO] Detecting faces...")
start = time.time()
# Detect face locations
boxes = face_recognition.face_locations(rgb, model="hog")  # Or use model="cnn" for higher accuracy
end = time.time()
print("[INFO] Face detection took: {} ms".format((end - start) * 1000))

# Encoding faces
print("[INFO] Encoding faces...")
encodings = face_recognition.face_encodings(rgb, boxes)
names = []

# Loop over encodings
print("[INFO] Matching faces...")
for encoding in encodings:
    matches = face_recognition.compare_faces(data["encodings"], encoding, tolerance=0.5)
    name = "Unknown"
    if True in matches:
        matchIdxs = [i for (i, match) in enumerate(matches) if match]
        counts = {}
        for i in matchIdxs:
            name = data["names"][i]
            counts[name] = counts.get(name, 0) + 1
        name = max(counts, key=counts.get)
    names.append(name)

# Loop over the recognized faces
for ((top, right, bottom, left), name) in zip(boxes, names):
    # Draw the predicted face name on the image
    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
    y = top - 15 if top - 15 > 15 else top + 15
    cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                0.75, (0, 255, 0), 2)

# Show the output image
cv2.imwrite("output/output_image.jpg", image)
cv2.imshow("Image", image)
cv2.waitKey(0)


        