import time
import cv2
import PE_module as pm

cap = cv2.VideoCapture('video.mp4')
pTime = 0
decorator = pm.poseDetector()
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
