# ImageRecognition_OpenCV
Recognizing set-point temperature via Raspberry Pi based on OpenCV 

## Process Flow
The image recognition process follows these steps:

<p align="center">
  <img src="Image/0.png" width="200" height='300' alt="Process Flow">
</p>

1. Start
2. Take the image when people change temperature
3. Input image
4. Image contrast enhancement
5. Apply three techniques in parallel:
   - Threshold
   - Grayscale
   - Erode
6. Contour extraction
7. Contour only set-point temperature
8. Judgment with sample numbers
9. Output

## Example Images
<p align="center">
  <img src="Image/01.png" width="45%" alt="Example 2">
</p>
