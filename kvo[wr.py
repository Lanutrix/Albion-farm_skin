import cv2 as cv

maper = cv.imread('map\\Screenshot_64.png')[554:660, 1086:1191]
mape = cv.imread('map\\Screenshot_63.png')[554:660, 1086:1191]
diff = cv.absdiff(maper, mape)
similarity = cv.mean(diff)[0]
print(similarity)