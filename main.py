import argparse, sys, os
from classes.ImgDataAug import ImgDataAug

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", type=str, help="Path to the input image")
parser.add_argument("-s", "--size", type=int, help="Size of output image in pixel")
parser.add_argument("-n", "--num", type=int, help="Number of output image")
# parser.add_argument("-o", "--output", type=str, help="Path to the output image")

args = vars(parser.parse_args())
IMAGE_PATH = args["image"]
SIZE = args["size"]
NUM = args["num"]

if IMAGE_PATH and SIZE and NUM:
    
    comList = []

    while (len(comList) < NUM):
    
        imgDataAug = ImgDataAug(IMAGE_PATH, SIZE)
        combination, f, r, xT, yT, xG, yG, nM, nV = imgDataAug.generateAllCombination()

        if ((combination in comList) is False):
            comList.append(combination)
            modeTuple = (f, r, xT, yT, xG, yG, nM, nV)
            print('com list '+ str(comList))
            print('mode tuple' + str(modeTuple))
            
            imgDataAug.executeImgProcessing(modeTuple)
            print('new combination' + combination)
            print(imgDataAug.imgPath)

        print("comList = " + str(comList))
        print("length of comList = " + str(len(comList)))
else:
    print("Please enter required arguments(image path, size, number of output image) before execution!")