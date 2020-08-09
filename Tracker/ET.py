import cv2, numpy as np, dlib, time
from math import hypot


class Detection:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.frame = None
        self.gray = None
        self.blank = 0

    def midpoint(self, p1, p2):
        return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)

    def get_gaze_ratio(self, eye_points, facial_landmarks):
        eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                               (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                               (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                               (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                               (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                               (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)],
                              np.int32)

        height, width, _ = self.frame.shape
        # make a mask that full of zeros
        # zeros donate black and none zeros are white
        mask = np.zeros((height, width), np.uint8)
        h=cv2.polylines(mask, [eye_region], True, 255, 2)
        cv2.fillPoly(mask, [eye_region], 255)
        eye = cv2.bitwise_and(self.gray, self.gray, mask=mask)

        min_x = np.min(eye_region[:, 0])
        max_x = np.max(eye_region[:, 0])
        min_y = np.min(eye_region[:, 1])
        max_y = np.max(eye_region[:, 1])

        gray_eye = eye[min_y: max_y, min_x: max_x]
        # Here we detect the white region of the eye and separate them into right and left regions
        _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
        threshold_eye = cv2.resize(threshold_eye, None, fx=5, fy=5)
        # eye = cv2.resize(gray_eye, None, fx=5, fy=5)
        # cv2.imshow("Eye", eye)
        # cv2.imshow("Threshold", threshold_eye)
        # cv2.imshow("Left eye", eye_region)
        height, width = threshold_eye.shape
        left_side_threshold = threshold_eye[0: height, 0: int(width / 2)]
        left_side_white = cv2.countNonZero(left_side_threshold)

        right_side_threshold = threshold_eye[0:height, int(width / 2): width]
        right_side_white = cv2.countNonZero(right_side_threshold)
        # cv2.imshow("",right_side_threshold)
        if right_side_white == 0:
            return 10
        else:
            return left_side_white / right_side_white

    def get_blinking_ratio(self, eye_points, facial_landmarks):
        left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
        right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
        center_top = self.midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
        center_bottom = self.midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

        hor_line_length = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
        ver_line_length = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
        ratio = 0
        if (ver_line_length != 0):
            ratio = hor_line_length / ver_line_length
        return ratio

    def get_operator(self, landmark):
        right_eye_ratio = self.get_blinking_ratio([36, 37, 38, 39, 40, 41], landmark)
        left_eye_ratio = self.get_blinking_ratio([42, 43, 44, 45, 46, 47], landmark)
        blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

        gaze_ratio_right_eye = self.get_gaze_ratio([36, 37, 38, 39, 40, 41], landmark)
        gaze_ratio_left_eye = self.get_gaze_ratio([42, 43, 44, 45, 46, 47], landmark)
        gaze_ratio = (gaze_ratio_left_eye + gaze_ratio_right_eye) / 2
        # print(gaze_ratio)


        if blinking_ratio >= 5.2 and self.blank < 10:
            self.blank += 1
        if self.blank>=10:
            self.blank = 0
            return 'blank'
        elif gaze_ratio <= .8:
            self.blank = 0
            return 'right'
        elif gaze_ratio >= 1.5:
            self.blank = 0
            return 'left'
        elif right_eye_ratio < 6 and left_eye_ratio >= 6:
            self.blank = 0
            return 'right_blank'
        elif right_eye_ratio >= 6 and left_eye_ratio < 6:
            self.blank = 0
            return 'left_blank'
        else : return None

    def run(self):
        pre=None
        while True:
            _, self.frame = self.cap.read()
            self.frame = cv2.flip(self.frame, 1)
            self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            faces = self.detector(self.gray)
            for face in faces:
                landmarks = self.predictor(self.gray, face)
                ret = self.get_operator(landmarks)
                if pre!=ret and pre!=None:
                    print(pre)
                pre=ret

                # print(ret)
            cv2.imshow("Frame", self.frame)

            key = cv2.waitKey(6)
            if key == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    d = Detection()
    d.run()
