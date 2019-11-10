try:
    from PIL import Image
except ImportError:
    import Image
from cv2 import cv2
import pytesseract 
import numpy

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
faceCascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

image = cv2.imread('imgs/bib_01.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30)
)

faceNumber = len(faces)
print('znaleziono '+str(faceNumber)+' twarzy \n')
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
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
    # print('y = '+str(y)+', y+h = '+str(y+h)+', x = '+str(x)+', x+w = '+str(x+w)+'\n')
    print('wycinam tors nr '+str(i+1)+'.') 
    crop_img = image[y:y+h, x:x+w]
    ROI[i] = crop_img
    # cv2.imshow("cropped_"+str(i), crop_img[i])
    i = i + 1

i = 0
for x in ROI:
    print('wyswietlam tors nr '+str(i)+'.')
    cv2.imshow("cropped_"+str(i), x)
    i = i + 1

cv2.imshow("Faces found", image)
cv2.waitKey()

#print(pytesseract.image_to_string(Image.open('imgs/bib_01.jpg')))
