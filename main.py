try:
    from PIL import Image
except ImportError:
    import Image
from cv2 import cv2
import pytesseract 
import numpy as np
from imutils.object_detection import non_max_suppression


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
faceCascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

def findText(img, i):
    # @TODO
    # make ROI from found texts and return a array of imgs. Then try recon text by pytesseract
    image = img
    orig = image.copy()
    (H, W) = image.shape[:2]

    # set the new width and height and then determine the ratio in change
    # for both the width and height
    (newW, newH) = (320, 320)
    rW = W / float(newW)
    rH = H / float(newH)

    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]

    # define the two output layer names for the EAST detector model that
    # we are interested -- the first is the output probabilities and the
    # second can be used to derive the bounding box coordinates of text
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]

    # load the pre-trained EAST text detector
    print("[INFO] loading EAST text detector...")
    net = cv2.dnn.readNet('./EAST/frozen_east_text_detection.pb')

    # construct a blob from the image and then perform a forward pass of
    # the model to obtain the two output layer sets
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                                 (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)

    # grab the number of rows and columns from the scores volume, then
    # initialize our set of bounding box rectangles and corresponding
    # confidence scores
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []

    # loop over the number of rows
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the geometrical
        # data used to derive potential bounding box coordinates that
        # surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]

        # loop over the number of columns
        for x in range(0, numCols):
            # if our score does not have sufficient probability, ignore it
            if scoresData[x] < 0.5:
                continue

            # compute the offset factor as our resulting feature maps will
            # be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)

            # extract the rotation angle for the prediction and then
            # compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            # use the geometry volume to derive the width and height of
            # the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]

            # compute both the starting and ending (x, y)-coordinates for
            # the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            # add the bounding box coordinates and probability score to
            # our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])

    # apply non-maxima suppression to suppress weak, overlapping bounding
    # boxes
    boxes = non_max_suppression(np.array(rects), probs=confidences)

    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
        # scale the bounding box coordinates based on the respective
        # ratios
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)

        # draw the bounding box on the image
        cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

    # show the output image
    cv2.imshow("Text Detection_"+str(i), orig)


# MAIN PROGRAM

image = cv2.imread('imgs/bib_01.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30)
)

faceNumber = len(faces)
# print('znaleziono '+str(faceNumber)+' twarzy \n')
ROI = [0] * faceNumber

for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

i = 0
for (x, y, w, h) in faces:
    x = int( x - (3*w/4) )
    y = int(y + 1.5*h)
    w = int(2.5*w)
    h = int(3.5*h)
    if x < 0:
        x = 1
    # cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
    # print('y = '+str(y)+', y+h = '+str(y+h)+', x = '+str(x)+', x+w = '+str(x+w)+'\n')
    crop_img = image[y:y+h, x:x+w]
    ROI[i] = crop_img
    # cv2.imshow("cropped_"+str(i), crop_img[i])
    i = i + 1

i = 0
for x in ROI:
    findText(x, i)
    # x = cv2.cvtColor(x,cv2.COLOR_BGR2GRAY)
    # kernel = np.ones((1,1), np.uint8)
    # x = cv2.dilate(x, kernel, iterations = 1)
    # x = cv2.erode(x, kernel, iterations=1)
    # x = cv2.adaptiveThreshold(x, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # cv2.imshow("Text Detection_"+str(i), orig)
    # cv2.imshow("cropped_"+str(i), x)
    # cv2.imwrite("cropped_"+str(i)+"_thres.jpg", x)
    # result = pytesseract.image_to_string(Image.open("cropped_"+str(i)+"_thres.jpg"))
    # print(result)
    i = i + 1

cv2.imshow("Faces found", image)
cv2.waitKey()

#print(pytesseract.image_to_string(Image.open('imgs/bib_01.jpg')))
