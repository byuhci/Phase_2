import cv2
"""
file_name = "detected_berries.png"

src = cv2.imread(file_name, 1)
tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
_,alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
b, g, r = cv2.split(src)
rgba = [b,g,r, alpha]
dst = cv2.merge(rgba,1)
cv2.imwrite("test.png", dst)
"""
def print_rect(n, m, c):
    row=n*c
    for a in range(m):
        print (row)
n=int(input("Enter the lenght of the rectangle: "))
m=int(input("Enter the width: "))
c="c"
print_rect(n, m, c)
input("Press enter to close")

