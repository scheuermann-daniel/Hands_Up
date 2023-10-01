# import libraries
from ctypes import cast, POINTER
from datetime import datetime
import cv2
import mediapipe as mp
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# initialize audio device
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None
)
volume = cast(interface, POINTER(IAudioEndpointVolume))
minVolume = -30
volumeRange = int(str(volume.GetVolumeRange())[1:4]) - minVolume

# initialize model
maxNumHands = 8
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode = False,
    model_complexity = 1,
    min_detection_confidence = 0.75,
    min_tracking_confidence = 0.75,
    max_num_hands = maxNumHands
)

# capture video
cap = cv2.VideoCapture(0)

# declare variables for hand consistency
numHands = 0
startTime = datetime.now()

while True:

    # read frame
    success, img = cap.read()

    # flip img
    img = cv2.flip(img, 1)

    # convert to rgb
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # process img
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:

        if len(results.multi_handedness) >= numHands:
            numHands = len(results.multi_handedness)
            cv2.putText(img, str(numHands), (250, 50),
                        cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)
            
            # change volume
            setVolume = volumeRange - (volumeRange*(numHands/maxNumHands)**(1/2))
            volume.SetMasterVolumeLevel(setVolume, None)

            # change start time
            startTime = datetime.now()

        elif len(results.multi_handedness) < numHands and (datetime.now()-startTime).total_seconds() >= 5:

            numHands = len(results.multi_handedness)
            cv2.putText(img, str(numHands), (250, 50),
                        cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)
            
            # change volume
            setVolume = volumeRange - (volumeRange*(numHands/maxNumHands)**(1/2))
            volume.SetMasterVolumeLevel(setVolume, None)

            # change start time
            startTime = datetime.now()
        
    if (not results.multi_hand_landmarks) and (datetime.now()-startTime).total_seconds() >= 5:
        startTime = datetime.now()
        volume.SetMasterVolumeLevel(minVolume, None)
        
    
    # display video and end if 'q'' is pressed
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
