import cv2
import numpy as np

# Read image
def read_image(path):
    img = cv2.imread(path)
    return img

# get edges
def get_edges(img):
    canny = cv2.Canny(img, 200, 300)
    return canny

# get contours
def get_contours(canny):
    contours = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    return contours

# filter out small regions
def filter_small_regions(contours,canny):
    cimg = np.zeros_like(canny)
    for cntr in contours:
        area = cv2.contourArea(cntr)
        if area > 50:
            cv2.drawContours(cimg, [cntr], 0, 255, 1)
    return cimg

# draw convex hull as filled mask
def get_convex_hull_mask(hull, cimg):
    mask = np.zeros_like(cimg, dtype=np.uint8)
    cv2.fillPoly(mask, [hull], 255)
    return mask

# blacken out input using mask
def mask_image(img, mask):
    mimg = img.copy()
    mimg = cv2.bitwise_and(mimg, mimg, mask=mask)
    return mimg

def get_left_right(cimg):
    points = np.column_stack(np.where(cimg.transpose() > 0))
    hull = cv2.convexHull(points)

    left = {}
    right = {}

    left = np.min(hull, axis = 0)
    right = np.max(hull, axis = 0)

    return tuple(left[0]),tuple(right[0])

def center_of_texts(path):
    img = read_image(path)
    edges = get_edges(img)
    contours = get_contours(edges)
    filtered = filter_small_regions(contours,edges)
    leftmost,rightmost = get_left_right(filtered)

    print("leftmost: ",leftmost)
    print("rigthmost: ",rightmost)
    center = (int((leftmost[0] + rightmost[0])/2), int((leftmost[1] + rightmost[1])/2))
    return center


def save_images(mask, edges, filtered, himg, final):
    cv2.imwrite('receipt_mask.jpg', mask)
    cv2.imwrite('receipt_edges.jpg', edges)
    cv2.imwrite('receipt_filtered_edges.jpg', filtered)
    cv2.imwrite('receipt_himg.jpg', himg)
    cv2.imwrite('receipt_final.jpg', final)
    cv2.imshow('canny', edges)
    cv2.imshow('cimg', filtered)
    cv2.imshow('himg', himg)
    cv2.imshow('mask', mask)
    cv2.imshow('final', final)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def crop_image(path,center):
        img = cv2.imread(path)
        #cv2.imshow("original", img)
        print(center[0],center[1])
        print(type(center[0]))
        # Cropping an image
        cropped_image_left = img[0:, 0: center[0]]
        cropped_image_right = img[0:, center[0] :]
        
        # Display cropped image
        cv2.imshow("cropped_left", cropped_image_left)
        cv2.imshow("cropped_right", cropped_image_right)
        
        # Save the cropped image
        #cv2.imwrite("Cropped_image_left.jpg", cropped_image_left)
        #cv2.imwrite("Cropped_image_right.jpg", cropped_image_right)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()

#borrar
#center = center_of_texts('tests/test6.png')
#crop_image('tests/test6.png',center)
