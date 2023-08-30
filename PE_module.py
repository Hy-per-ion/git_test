import time
import cv2
import mediapipe as mp


class poseDetector:
    def __init__(self, mode=False, com=1, smooth=True, e_smooth=False, s_smooth=True, detectionCon=0.5,
                 trackingCon=0.5):
        self.results = None
        self.mode = mode
        self.com = com
        self.smooth = smooth
        self.e_smooth = e_smooth
        self.s_smooth = s_smooth
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.com, self.smooth, self.e_smooth, self.s_smooth, self.detectionCon,
                                     self.trackingCon)

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return lmList


def main():
    cap = cv2.VideoCapture('video.mp4')
    pTime = 0
    decorator = poseDetector()
    while True:
        success, img = cap.read()
        img = decorator.findPose(img)
        lmList = decorator.findPosition(img)
        if len(lmList) != 0:
            print(lmList[14])  # 14- elbow can be used to track a particular point
            cv2.circle(img, (lmList[14][1], lmList[14][2]), 8, (0, 0, 255), cv2.FILLED)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit the program
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
