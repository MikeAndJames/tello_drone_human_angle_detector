
from cv2.dnn import DetectionModel
from djitellopy import Tello
import cv2
import time
import winsound

# 1. Load the built-in face detector once at the top of your code
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


drone = Tello()
drone.connect()
print("🔋 Battery:", drone.get_battery(), "%")
print("🌡️ Temp   :", drone.get_temperature(), "°C")



# start camera stream

# # Force highest video quality and 30 FPS
# drone.set_video_bitrate(drone.BITRATE_5MBPS)
# drone.set_video_resolution(drone.RESOLUTION_720P)
# drone.set_video_fps(drone.FPS_30)


drone.streamon()
frame_read = drone.get_frame_read()

drone.takeoff()

#show a picture, rotate 90 degrees, show another picture
while True:
    #get next frame
    frame = frame_read.frame
    # Flip RGB to BGR so colors are natural!
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # 🧼 Real-time Denoise Filter (Cleans grain while keeping edges sharp!)
    frame = cv2.bilateralFilter(frame, d=7, sigmaColor=50, sigmaSpace=50)

    # Convert frame to grayscale (face detection is faster in black & white)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Search the frame for faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=7)

    if len(faces) > 0:
        # faces contains [(x , y, w h)]
        # draw yellow target box around the enemy
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 3)
    
        angle = drone.get_yaw()
        # 3. (Optional) Draw alert text right on the live video window!
        cv2.putText(frame, f"TARGET LOCKED: {angle} DEG", (30, 60), 
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        drone.send_rc_control(0, 0, 0, 0)  # Stop spinning and fire missile!
        winsound.Beep(1800, 120)  # High lock tone!

            
    else: # no faces detected
        drone.send_rc_control(0, 0, 0, 33) #  rotate at 10% speed 

    # Read battery and draw green HUD text at top-left (X=30, Y=30)
    batt = drone.get_battery()
    cv2.putText(frame, f"BATTERY: {batt}%", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # draw on screen
    cv2.imshow("Live Drone Feed", frame)

    #check keyboard input 
    key = cv2.waitKey(1) & 0xFF
    
    #if ESC key is pressed, break the loop
    if key == ord("q"):
        break
    elif key == ord("s"):
        cv2.imwrite("screenshot.jpg",frame)
        print("Screenshot saved")

# land and clean up windows
drone.land()
cv2.destroyAllWindows()
drone.streamoff()
print("flight complete")

