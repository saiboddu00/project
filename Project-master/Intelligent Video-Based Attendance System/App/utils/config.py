import os

# path to capture faces
DATASET = r"D:\Main project-2\automatic-classroom-attendance-system-master\dataset"

# face encoding and attendance output path
ENCODINGS_PATH = r"D:\Main project-2\automatic-classroom-attendance-system-master\output\encodings2.pickle"
ATTENDANCE_PATH = r"D:\Main project-2\automatic-classroom-attendance-system-master\output\attendance.csv"

# face detector model
PROTOTXT_PATH = r"D:\Main project-2\automatic-classroom-attendance-system-master\model\deploy.prototxt.txt"
MODEL_PATH = r"D:\Main project-2\automatic-classroom-attendance-system-master\model\res10_300x300_ssd_iter_140000.caffemodel"

# capture duration
CAPTURE_DURATION = 10000 # 5 * 60 * 1000 = 30000ms or 5 minutes  