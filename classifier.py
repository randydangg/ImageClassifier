from PIL import Image
import random
import math

def getVector(imgName):
    im = Image.open(imgName).convert("L")
    width, height = im.size

    white1 = 1
    white2 = 1
    white3 = 1
    white4 = 1
    white5 = 1
    white6 = 1
    white7 = 1
    white8 = 1
    white9 = 1

    black1 = 1
    black2 = 1
    black3 = 1
    black4 = 1
    black5 = 1
    black6 = 1
    black7 = 1
    black8 = 1
    black9 = 1

    x1 = width/3
    x2 = 2*x1

    y1 = height/3
    y2 = 2*y1

    # Sectors
    # 1 2 3
    # 4 5 6
    # 7 8 9
    for i in range(width):
        for j in range(height):
           #Sector 1
            if i<x1 and j<y1:
                if im.getpixel((i,j)) > 127:
                    white1 += 1
                else:
                    black1 += 1
            #Sector 2
            if x1<i and i<x2 and j<y1:
                if im.getpixel((i,j))>127:
                    white2 += 1
                else:
                    black2 += 1
            #Sector 3
            if i>x2 and j<y1:
                if im.getpixel((i,j))>127:
                    white3 += 1
                else:
                    black3 += 1
            #Sector 4
            if i<x1 and j>y1 and j<y2:
                if im.getpixel((i,j))>127:
                    white4 += 1
                else:
                    black4 += 1
            #Sector 5
            if x1<i and i<x2 and j>y1 and j<y2:
                if im.getpixel((i,j))>127:
                    white5 += 1
                else:
                    black5 += 1
            #Sector 6
            if i>x2 and j>y1 and j<y2:
                if im.getpixel((i,j))>127:
                    white6 += 1
                else:
                    black6 += 1
            #Sector 7
            if i<x1 and j>y2:
                if im.getpixel((i,j))>127:
                    white7 += 1
                else:
                    black7 += 1
            #Sector 8
            if x1<i and i<x2 and j>y2:
                if im.getpixel((i,j))>127:
                    white8 += 1
                else:
                    black8 += 1
            #Sector 9
            if i>x2 and j>y2:
                if im.getpixel((i,j))>127:
                    white9 += 1
                else:
                    black9 += 1
    featureVector = [black1/white1,black2/white2,black3/white3,black4/white4,black5/white5,black6/white6,black7/white7,black8/white8,black9/white9]
    return featureVector

def getCenterMass(featureVectors):
#Inputs: featureVectors: A list of feature vectors containing all the featureVectors
#for one digit
#Outputs: center_mass: The average vector of a given set of vectors
    center_mass = []
    for x in range(9):
        sum = 0
        for y in range (len(featureVectors) - 1):
            sum += featureVectors[y][x]
        center_mass.append(sum/(len(featureVectors)))
    return center_mass

def getEDistance(centerMass,featureVector):
#Inputs: featureVector: The feature vector of the image we want to classify
#        centerMass : The average vector of a given set of vectors
#Outputs: distance: The euclidean distance between the feature vector and the
# centermass.
    distance = 0
    for x in range (9):   #Distance
        distance += pow((featureVector[x]-centerMass[x]), 2)
    distance = math.sqrt(distance)
    return distance

def classifyNumber(featureVector,centerMasses):
#Inputs: featureVector: The feature vector of the image we want to classify
#       centerMasses: A list containing feature vectors for numbers 1-10
#Outputs: number: the number the program thinks the image is of
#The function finds the center of mass with the minimium euclidian distance to the
#feature vector. The center mass with the minimium distance is decided to be the number
    min_distance = 9999999
    for x in range (10):   #Distance
        distance = getEDistance(centerMasses[x],featureVector)
        if distance < min_distance:
            min_distance = distance
            number = x
    return number


#Main

#Training
#Loads 5 images selected randomly from a pool of 10 images for each number to train the algorithm
seed = list(range(0, 10))
random.shuffle(seed)
centerMass = []
centerMasses = []
featureVectors = []
temp = []
for i in range(10):
    for j in range(5):
        #Image file names will be follow the format [digit][image number].png
        #The 4th image of a number 2 would be named 24.png
        imgFileName = str(i) + str(seed[j]) +".png"
        temp.append(getVector(imgFileName))
    featureVectors.append(temp)
    temp = []
for i in range(10):
    centerMasses.append(getCenterMass(featureVectors[i]))

#Testing
#Create feature vectors of all reamining images and classify them by comparing them to
#the center of masses for each digit that was found during training
featureVectors = []
temp = []
img_file_name = []
temp_file_name = []
img_number =[]
actual_number =[]
for i in range(10):
    for j in range(5,10):
        #Image file names will be follow the format [digit][image number].png
        #The 4th image of a number 2 would be named 24.png
        imgFileName = str(i) + str(seed[j]) +".png"
        img_number.append(i)
        temp_file_name.append(imgFileName)
        temp.append(getVector(imgFileName))
    featureVectors.append(temp)
    img_file_name.append(temp_file_name)
    actual_number.append(img_number)
    temp_file_name = []
    img_number = []
    temp = []
#Classify each number in testing set
correct = 1
incorrect = 1
for i in range(10):
    for j in range(len(featureVectors[i])):
        numberGuess = classifyNumber(featureVectors[i][j],centerMasses)
        # print("Correct: " + str(correct-1) + " Incorrect: " +str(incorrect-1) + " %: " + str((correct/incorrect)*100))
        print(img_file_name[i][j] + " Number Guess: {0:d} Actual Number: {1:d}".format(numberGuess,actual_number[i][j]))
        if (numberGuess == i):
            correct += 1
        else:
            incorrect += 1
correctPercentage = (correct/incorrect)*100
print("Correct/Incorrect%: {0:.2f}".format(correctPercentage))
