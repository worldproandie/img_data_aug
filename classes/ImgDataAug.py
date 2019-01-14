import cv2
import numpy as np
import random
from matplotlib import pyplot as plt
from skimage import img_as_float, img_as_ubyte
from skimage.util import random_noise

class ImgDataAug:
    def __init__(self, imgPath, size = 64):
        self.imgPath = imgPath
        self.img = cv2.imread(imgPath).copy()
        self.combination = ""
        self.size = size

    def getModes(self):
        return self.combination.split('-') 

    def convertCV_Ski(self, cvImg):
        return img_as_float(cvImg)

    def convertSki_CV(self, skiImg):
        return img_as_ubyte(skiImg)

    def updateCombination(self, string):
        self.combination += string

    def outputFileName(self):
        return self.imgPath[:-4] + "-" + self.combination + "-s" + str(self.size) + ".png"

    def randomFlipMode(self):
        mode = random.randint(0,2)
        self.updateCombination("f" + str(mode))
        return mode

    def imgFlip(self, modeIndex):
        mode = [0, 1, -1] # horizontal, vertical, both
        flip = cv2.flip(self.img, mode[modeIndex])
        self.img = flip

        print('flip mode' + str(mode))

    def randomRotateDegree(self):
        degree = round(random.uniform(0, 361),2)
        self.updateCombination("-r" + str(degree).replace('.','_'))
        return degree
       
    def imgRotate(self, degree):
        rows, cols = self.img.shape[:2]
        M = cv2.getRotationMatrix2D((cols/2,rows/2),degree,1)
        dst = cv2.warpAffine(self.img,M,(cols,rows))
        self.img = dst

        print('rotated by ' + str(degree))


    def randomXYTranslateMode(self):
        tMax = 10
        xTS = random.randint(0,1) 
        yTS = random.randint(0,1)

        xT = round(random.uniform(0, 10), 2)
        yT = round(random.uniform(0, 10), 2)

        x = xT if (xTS > 0) else -xT
        y = yT if (yTS > 0) else -yT

        self.updateCombination("-xt" + str(x).replace('.','_').replace('-','n') +
                             "-yt" + str(y).replace('.','_').replace('-','n'))
        return x, y

    def imgXYTranslate(self, x, y):
        rows, cols = self.img.shape[:2]
        M = np.float32([[1,0,x],[0,1,y]])
        dst = cv2.warpAffine(self.img, M, (cols,rows))
        self.img = dst

        print('x translate ' + str(x))
        print('y translate ' + str(y))

    def randomXYGaussianBlurMode(self):
        gbMax = 19

        x = random.randrange(1, gbMax+1, 2)
        y = random.randrange(1, gbMax+1, 2)

        self.updateCombination("-xg" + str(x) +
                             "-yg" + str(y))
        return x, y

    def imgXYGaussianBlur(self, x, y):
        blur = cv2.GaussianBlur(self.img,(x,y),0)
        self.img = blur

        print('x GaussianBlur ' + str(x))
        print('y GaussianBlur ' + str(y))
        
    def randomNoiseMode(self):
        ms =['g', 's']
        modes = ['gaussian', 'speckle']
        vMax = 0.01

        m = random.randint(0,1)
        v = round(random.uniform(0, vMax), 4)
        self.updateCombination("-n" + ms[m] + str(v).replace('.', '_'))

        return modes[m], v

    def imgNoise(self, nMode, variance):
        skiImg = self.convertCV_Ski(self.img)
        noiseImg = self.convertSki_CV(random_noise(skiImg, mode=nMode, seed=None, clip=True, mean=0, var=variance))
        self.img = noiseImg

        print('noise mode = ' + nMode + ' var = ' + str(variance))

    def generateAllCombination(self):
        f = self.randomFlipMode()
        r = self.randomRotateDegree()
        xT, yT = self.randomXYTranslateMode()
        xG, yG = self.randomXYGaussianBlurMode()
        nM, nV = self.randomNoiseMode()
        return self.combination, f, r, xT, yT, xG, yG, nM, nV

    def executeImgProcessing(self, modeTuple):
        f, r, xT, yT, xG, yG, nM, nV = modeTuple
        self.imgFlip(f)
        self.imgRotate(r)
        self.imgXYTranslate(xT, yT)
        self.imgXYGaussianBlur(xG, yG)
        self.imgNoise(nM, nV)
        self.saveImg()

    def saveImg(self):
        filename = self.outputFileName()
        resize = cv2.resize(self.img, (self.size, self.size))
        cv2.imwrite(filename , resize)

        print('file saved : ' + filename)
