# Hands_Up

Daniel Scheuermann

12/2022

## Summary

"Hands Up" is a party device which is meant to use the common phrase "Put your hands in the air" and use it to create a responsive party environment. The more hands in the air detected, the more the volume of the music will increase.

To use, attach a camera and make sure it has a span of the entire room. Run the script. Note that when more hands are detected, the volume of the device increases.

## Installations/Libraries

  - ctypes
  - datetime
  - cv2
  - mediapipe
  - comtypes
  - pycaw

## Known Bugs

    - In bad lighting, it may not detect the hands consistently
    - If hands move too fast, more hands might be detected than there are in the air

## Future Work

    - Implement method to reduce error from bad lighting. Perhaps thermal camera?
    - Create better UI
    - Make more usable in a party setting
