#ultralytics-- has YOLO
from ultralytics import YOLO
import cv2
model=YOLO("yolov8n.pt")
cap=cv2.VideoCapture(r"C:\Users\rajah\Desktop\gaya3\python projects\YOLOmodel\WhatsApp Video 2026-06-05 at 10.05.31 AM.mp4")

while True:
    ret, frame= cap.read()
    if not ret:
        break

    results=model.track(
        frame,
        persist=True,
        classes=[0]
    )

    annotated_frame=results[0].plot()
    cv2.imshow("Person Tracking",annotated_frame)
    if cv2.waitKey(1) & 0xFF ==27:
        break

cap.release()
cv2.destroyAllWindows()