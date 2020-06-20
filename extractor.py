import cv2
import numpy as np
import datetime

class Extractor(object):

    def __init__(self, path, debug=False):
        self.path = path
        self.debug = debug

    def extract(self, image):
        buffer = int(len(image) * 0.05)
        image = image[buffer:-buffer][buffer:-buffer]
        if self.debug: imdbg = image.copy()
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        threshold = cv2.threshold(grayscale, 228, 255, cv2.THRESH_BINARY_INV)[1]
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        results = list()

        for i, contour in enumerate(contours):
            _,_,w,h = cv2.boundingRect(contour)
            if w < 200 or h < 100:
                continue

            a, b, c, d = self._get_corners(contour)
            if self.debug:
                cv2.drawContours(imdbg, [contour], -1, (0, 128, 255), 3)
                cv2.line(imdbg, (0,0), a, (0, 255, 0), thickness=2)
                cv2.line(imdbg, (0,0), b, (255, 0, 0), thickness=2)
                cv2.line(imdbg, (0,0), c, (0, 0, 255), thickness=2)
                cv2.line(imdbg, (0,0), d, (0, 255, 255), thickness=2)

            old = np.float32([a,b,d,c])
            aa, bb, cc, dd = [0,0], [w,0], [w,h], [0,h]
            new = np.float32([aa,bb,dd,cc])
            trans = cv2.getPerspectiveTransform(old, new)
            result = cv2.warpPerspective(image, trans, (w,h))
            if self.debug:
                cv2.imshow(f"DEBUG: Result {i}", self._resize(result, width=600))
            results.append(result)


        if self.debug:
            cv2.imshow("DEBUG: Image", self._resize(imdbg, width=600))
            cv2.imshow("DEBUG: Grayscale", self._resize(threshold, width=600))
            cv2.waitKey(0)

        time = datetime.datetime.now()
        time = time.strftime("%Y-%m-%d_%H-%M")
        for i, result in enumerate(results):
            cv2.imwrite(f"{self.path}/scan_{time}_{i}.png", result)
        return len(results)

    def _resize(self, image, width=None, height=None, inter=cv2.INTER_AREA):
        h, w = image.shape[:2]
        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))

        return cv2.resize(image, dim, interpolation=inter)

    def _get_corners(self, contour):
        ay = min(c[0][1] for c in contour)
        axr = [c[0][0] for c in contour if c[0][1] == ay]
        axm = np.mean(axr)

        bx = max(c[0][0] for c in contour)
        cy = max(c[0][1] for c in contour)
        dx = min(c[0][0] for c in contour)

        if abs(axm - dx) > abs(axm - bx):
            # d and c are left
            ax = max(axr)
            by = max(c[0][1] for c in contour if c[0][0] == bx)
            cx = min(c[0][0] for c in contour if c[0][1] == cy)
            dy = min(c[0][1] for c in contour if c[0][0] == dx)
            return (dx, dy), (ax, ay), (bx, by), (cx, cy)
        else:
            # a and d are left
            ax = min(axr)
            by = min(c[0][1] for c in contour if c[0][0] == bx)
            cx = max(c[0][0] for c in contour if c[0][1] == cy)
            dy = max(c[0][1] for c in contour if c[0][0] == dx)
            return (ax, ay), (bx, by), (cx, cy), (dx, dy)

if __name__ == "__main__":
    ext = Extractor(".", True)
    image = cv2.imread("out.png")
    ext.extract(image)