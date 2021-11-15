import sys
from typing import final                      # System bindings
import cv2                      # OpenCV bindings
import numpy as np
from collections import Counter
import math
from PIL import Image, ImageDraw

class BackgroundColorDetector():
    def __init__(self, imageLoc):
        self.img = cv2.imread(imageLoc, 1)
        self.manual_count = {}
        self.w, self.h, self.channels = self.img.shape
        self.total_pixels = self.w*self.h

    def count(self):
        for y in range(0, self.h):
            for x in range(0, self.w):
                RGB = (self.img[x, y, 2], self.img[x, y, 1], self.img[x, y, 0])
                if RGB in self.manual_count:
                    self.manual_count[RGB] += 1
                else:
                    self.manual_count[RGB] = 1

    def average_colour(self):
        red = 0
        green = 0
        blue = 0
        sample = 10
        for top in range(0, sample):
            red += self.number_counter[top][0][0]
            green += self.number_counter[top][0][1]
            blue += self.number_counter[top][0][2]

        average_red = red / sample
        average_green = green / sample
        average_blue = blue / sample
        print("Average RGB for top ten is: (", average_red,
              ", ", average_green, ", ", average_blue, ")")

    def twenty_most_common(self):
        self.count()
        self.number_counter = Counter(self.manual_count).most_common(20)
        for rgb, value in self.number_counter:
            print(rgb, value, ((float(value)/self.total_pixels)*100))

    def detect(self):
        self.twenty_most_common()
        self.percentage_of_first = (
            float(self.number_counter[0][1])/self.total_pixels)
        print(self.percentage_of_first)
        if self.percentage_of_first > 0.5:
            print("Background color is ", self.number_counter[0][0])
        else:
            self.average_colour()


if __name__ == "__main__":
    if (len(sys.argv) != 5):                        # Checks if image was given as cli argument
        print("error: syntax is 'python main.py /example/image/location.jpg'")
    else:
        originAddr = sys.argv[1]
        tReq = sys.argv[2]
        w = int(sys.argv[3])
        h = int(sys.argv[4])

        BackgroundColor = BackgroundColorDetector(originAddr + "/" + tReq + ".png")
        BackgroundColor.detect()
        bgColor = BackgroundColor.number_counter[0][0]
        color_hex = '#{:02x}{:02x}{:02x}'.format(*bgColor)

        shape = [(0, 0), (w, h)]
        
        # creating new Image object
        img = Image.new("RGB", (w, h))
        
        # create rectangle image
        img1 = ImageDraw.Draw(img)  
        img1.rectangle(shape, fill = color_hex, outline = None)

        # img.save(originAddr + "/" + tReq + ".png","png")
        img2 = Image.open(originAddr + "/" + tReq + ".png")
        
        new_width  = int(w)
        new_height = int(new_width * img2.height / img2.width)
        img2 = img2.resize((new_width, new_height), Image.ANTIALIAS)

        img_w, img_h = img2.size
        bg_w, bg_h = img.size
        offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
        img.paste(img2,offset)
        img.save(originAddr + "/" + tReq + "_export.png")
        # im = np.array(img)×
        
        # finalImage = cv2.add(im,BackgroundColor.img)
        # cv2.imshow(finalImage)