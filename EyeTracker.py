import cv2,dlib
from math import hypot
font=cv2.FONT_HERSHEY_SIMPLEX
from scipy.spatial import distance as dist
from imutils import face_utils

def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)

def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])

	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])

	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)

	# return the eye aspect ratio
	return ear

class Detection:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(r"Resources\shape_predictor_68_face_landmarks.dat")
        self.yourEyes = 2400
        self.frames = 6
        (self.lStart, self.lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (self.rStart, self.rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


    def maxIn10Frames(self):
        dic = {
            'blank': 0,
            'right_blank': 0,
            'left_blank': 0,
            'open': 0
        }
        for i in range(self.frames):
            ret, frame = self.cap.read()
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, None, fx=0.76, fy=0.76)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.detector(gray,0)
            for face in faces:
                shape = self.predictor(gray, face)
                shape = face_utils.shape_to_np(shape)
                leftEye = shape[self.lStart:self.lEnd]
                rightEye = shape[self.rStart:self.rEnd]
                leftEAR = int(eye_aspect_ratio(leftEye)*10000)
                rightEAR = int(eye_aspect_ratio(rightEye)*10000)
                leftEAR,rightEAR=rightEAR,leftEAR                   #My Camera Flib video
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                cv2.putText(frame, str(leftEAR), (50, 150), font, 1, (0, 0, 255))
                cv2.putText(frame, str(rightEAR), (300, 150), font, 1, (0, 0, 255))
                if leftEAR < self.yourEyes and rightEAR < self.yourEyes:
                    dic['blank'] += 1
                elif leftEAR < self.yourEyes:
                    dic['left_blank'] += 1
                elif rightEAR < self.yourEyes:
                    dic['right_blank'] += 1
                else:
                    dic['open'] += 1
            cv2.imshow('frame', frame)
            if cv2.waitKey(1)>27:
                break
        mx = ('', 0)
        for key in dic:
            if dic[key] >= mx[1]:
                mx = (key, dic[key])
        # print(dic,mx[0])
        return mx[0]












if __name__=='__main__':
    d=Detection()
    pre = 'open'
    while True:
        cur = d.maxIn10Frames()
        if cur != pre and cur == 'open':
            print(pre)
        pre = cur

