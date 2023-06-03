import cv2
g1 = cv2.imread('Screenshot_61.png')[447:472, 520:530]
g2 = cv2.imread('looting.png')[447:472, 520:530]
diff = cv2.absdiff(g1, g2)
similarity = cv2.mean(diff)[0]
print(similarity)
cv2.imwrite('32.png', g1)
cv2.imwrite('33.png', g2)