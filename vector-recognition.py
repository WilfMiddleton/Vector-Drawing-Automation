#-------------------------------------------------------------------------------
# Name:        Vector-Recognition
# Purpose:
# Creates contour list of all residential buildings found in a satelite photo.
# Based on Bing maps photos of Labe in Gambia, using brightly coloured
# rectangular roofs as indicators of residential buildings.

# Author:      Wilf Middleton
#
# Created:     31/12/2016
# Copyright:   (c) WilfM 2016
#-------------------------------------------------------------------------------

import cv2
import numpy
import imutils

# ------------------------------Load Image ----------------------------------- #

img = cv2.imread('bing3.PNG')
cv2.imshow('Map',img)
img2 = cv2.imread('bing3.PNG',0)
cv2.imshow('Grey Map',img2)

# ------ Clean image using blur. Varying blur sensitivity could improve ------ #
# ------- threshing process. Perfect blur-level is picture dependent. -------- #

blurred = cv2.GaussianBlur(img2,(1,1),0)
cv2.imshow('blurred',blurred)

cv2.waitKey()

# --- Thresh blurred image with [    ] value of kk, rising from zero --- #

HowManyContours = 0
kk = 0
AA = numpy.matrix([HowManyContours])
counter = 1
while kk <= 255:
    kk = kk + counter
    print kk, '= kk'
    LastHowMany = HowManyContours
    LastButOne = LastHowMany
    threshedblurred = cv2.threshold(blurred, kk, 250, cv2.THRESH_BINARY_INV)[1]
    imcontours, contours, hierarchy = cv2.findContours(threshedblurred, \
    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# - Best threshing is: most contours produced within chosen roof size range  - #

    min_area = 100                # Smaller than this: unhelpful object or noise
    max_area = 1600         # Larger than this: roads, fields, unhelpful objects
    GoodContours = []
    print len(contours), ' = no. of contours'
    for cnt in contours:
        area = cv2.contourArea(cnt)

        if min_area <= area <= max_area:
            GoodContours.append(cnt)

    GoodContMat = numpy.array(GoodContours)

# ------------------------------ Show output --------------------------------- #

    cv2.imshow('threshed blurred', threshedblurred)
    cv2.imshow('contoured blurred', imcontours)
    HowManyContours = len(GoodContMat)
    print 'HowManyContours', HowManyContours
    cv2.waitKey(1)

# ----------------- List contour numbers for each threshing ------------------ #

    newrow = [HowManyContours]
    AA = numpy.vstack([AA, newrow])

# -----------------------------  Sense check  -------------------------------- #

    MaxContGuess = 400

  # Quick guess of max possible buildings in picture
  # If exceeded, either guess is too low or threshing takes wrong sized contours

    if HowManyContours > MaxContGuess:
        print 'problem with guess or threshing'
    else:
        continue

# -------- Find max value(s) of HowManyContours & position(s) in list -------- #

maxcont = max(AA)
indices = [index for index, val in enumerate(AA) if val == maxcont]

# --------------------- Re-do Optimum Thresh for picture --------------------- #

print indices
threshed2 = cv2.threshold(blurred, min(indices), 250,cv2.THRESH_BINARY)[1]

cv2.imshow('threshed & blurred', threshed2)
imcontours, contours, hierarchy = cv2.findContours(threshedblurred, \
cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


# ---------------------------------  Ending ---------------------------------- #

cv2.waitKey()
cv2.destroyAllWindows()




