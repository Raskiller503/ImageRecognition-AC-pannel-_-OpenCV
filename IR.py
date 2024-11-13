import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime
import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from paho.mqtt import client as mqtt_client

now = datetime.datetime.now()
time_string = now.strftime("%Y/%m/%d %H:%M:%S")

def plt_show0(img):
    b, g, r = cv2.split(img)
    img = cv2.merge([r, g, b])
    plt.imshow(img)
    plt.show()
def plt_show(img):
    plt.imshow(img, cmap='gray')
    plt.show()
def gray_guss(image):
    # image = cv2.GaussianBlur(image,(3,3),0)
    image = cv2.blur(image, (9, 16), 0)
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return gray_image

def get_image_in_folder(folder_path):
    """Get the only image in a given folder."""
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):  
            return cv2.imread(os.path.join(folder_path, filename))
    return None

img1 = get_image_in_folder("E:/Set_point/test")
plt.imshow(img1)

lab= cv2.cvtColor(img1, cv2.COLOR_BGR2LAB)
l_channel, a, b = cv2.split(lab)

clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(50,40))
cl = clahe.apply(l_channel)

limg = cv2.merge((cl,a,b))

enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

result = np.hstack((img1, enhanced_img))
plt_show(result)

gray_image = gray_guss(enhanced_img)
Sobel_x= cv2.Sobel(gray_image, cv2.CV_16S,1,0)
absX = cv2.convertScaleAbs(Sobel_x)
image =absX
ret, image = cv2.threshold(image,0,255,cv2.THRESH_OTSU)
plt_show(image)

kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 1))
kernelY = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 30))
image = cv2.dilate(image, kernelX)
image = cv2.erode(image, kernelX)
image = cv2.erode(image, kernelY)
image = cv2.dilate(image, kernelY)
plt_show(image)

kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 17))
image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernelX,iterations = 4)
plt_show(image)

kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 1))
kernelY = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
image = cv2.dilate(image, kernelX)
image = cv2.erode(image, kernelX)
image = cv2.erode(image, kernelY)
image = cv2.dilate(image, kernelY)
image = cv2.medianBlur(image, 21)
plt_show(image)

contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

filtered_images = []

for item in contours:
    rect = cv2.boundingRect(item)
    x = rect[0]
    y = rect[1]
    width = rect[2]
    height = rect[3]

    target_region = img1[y:y + height, x:x + width]


    if (700 < width < 800) and (600 < height < 800) and (width > 150):

        filtered_images.append(target_region)

if len(filtered_images) > 0:
    plt_show0(filtered_images[0])
else:
    print("no suitable area")

image_controller = filtered_images[0]
image = image_controller.copy()
plt_show0(image)

lab= cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
l_channel, a, b = cv2.split(lab)

clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(50,40))
cl = clahe.apply(l_channel)

limg = cv2.merge((cl,a,b))

enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

result = np.hstack((image, enhanced_img))
plt_show(result)

gray_image = gray_guss(enhanced_img)
Sobel_x= cv2.Sobel(gray_image, cv2.CV_16S,1,0)
absX = cv2.convertScaleAbs(Sobel_x)
image =absX
ret, image = cv2.threshold(image,0,255,cv2.THRESH_OTSU)
plt_show(image)

kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 10))
image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernelX,iterations = 2)
plt_show(image)

kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (90, 1))
kernelY = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 10))
image = cv2.dilate(image, kernelX)
image = cv2.erode(image, kernelX)
image = cv2.erode(image, kernelY)
image = cv2.dilate(image, kernelY)
image = cv2.medianBlur(image, 21)
plt_show(image)

contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

filtered_screens = []

for item in contours:
    rect = cv2.boundingRect(item)
    x = rect[0]
    y = rect[1]
    weight = rect[2]
    height = rect[3]
    if (weight > (height * 1.5)) and (weight < (height * 1.9)):
        image_screen = image_controller[y:y + height, x:x + weight]
        filtered_screens.append(image_screen)
        plt_show0(image_screen)


image = image_screen.copy()
plt_show(image)
lab= cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
l_channel, a, b = cv2.split(lab)

clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(1,1))
cl = clahe.apply(l_channel)

limg = cv2.merge((cl,a,b))

enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

result = np.hstack((image, enhanced_img))
plt_show(result)

plt_show(enhanced_img)

image = cv2.GaussianBlur(enhanced_img,(3,3),0)
gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
Sobel_x= cv2.Sobel(gray_image, cv2.CV_16S,1,0)
absX = cv2.convertScaleAbs(Sobel_x)
image =absX
ret, image = cv2.threshold(image,0,255,cv2.THRESH_OTSU)
plt_show(image)

kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
kernelY = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 2))
image = cv2.dilate(image, kernelX)
image = cv2.erode(image, kernelX)
image = cv2.erode(image, kernelY)
image = cv2.dilate(image, kernelY)
plt_show(image)

kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
image_1 = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernelX,iterations = 6)
image_1 = cv2.blur(image_1,(1,1),0)
plt_show(image_1)

kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 1))
kernelY = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 10))
image = cv2.dilate(image_1, kernelX)
image = cv2.erode(image, kernelX)
image = cv2.erode(image, kernelY)
image = cv2.dilate(image, kernelY)
image = cv2.medianBlur(image, 21)
plt_show(image)

contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# filtered_screens = []

for item in contours:
    rect = cv2.boundingRect(item)
    x = rect[0]
    y = rect[1]
    weight = rect[2]
    height = rect[3]
    print(x,y,weight,height)
    if (weight > (height * 1)) and (weight < (height * 1.5)) and height > 30:
        image_digit = enhanced_img[y:y + height, x:x + weight]
        # filtered_screens.append(image_screen)
        plt_show0(image_digit)
contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for item in contours:
    rect = cv2.boundingRect(item)
    x, y, weight, height = rect

    if (weight > (height * 1)) and (weight < (height * 1.5)) and height > 30:
        image_digit = enhanced_img[y:y + height, x:x + weight]
        lab = cv2.cvtColor(image_digit, cv2.COLOR_BGR2LAB)
        l_channel, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(clipLimit=7.0, tileGridSize=(7,7))
        cl = clahe.apply(l_channel)

        limg = cv2.merge((cl, a, b))
        enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

        result = np.hstack((image_digit, enhanced_img))
        plt.imshow(result)
        plt.show()

Inverse_frame_gray = cv2.bitwise_not(enhanced_img)
plt_show(Inverse_frame_gray)

image = cv2.blur(Inverse_frame_gray,(3,5),0)
gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
ret, image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU)
plt_show(image)


contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
words = []
word_images = []

n=0
for item in contours:
    n=n+1
    print(n)
    word = []
    rect = cv2.boundingRect(item)
    x = rect[0]
    y = rect[1]
    weight = rect[2]
    height = rect[3]
    word.append(x)
    word.append(y)
    word.append(weight)
    word.append(height)
    words.append(word)

words = sorted(words,key=lambda s:s[0],reverse=False)
i = 0

for word in words:

    if (word[3] > (word[2] * 1.5)) and (word[3] < (word[2] * 30)) and (word[2] > 10):
        i = i+1
        splite_image = image[word[1]:word[1] + word[3], word[0]:word[0] + word[2]]
        word_images.append(splite_image)
        print(i)
print(words)

for i,j in enumerate(word_images):
    plt.subplot(1,7,i+1)
    plt.imshow(word_images[i],cmap='gray')
# plt.show()


template = ['0','1','2','3','4','5','6','7','8','9']


def read_directory(directory_name):
    referImg_list = []
    for filename in os.listdir(directory_name):
        referImg_list.append(directory_name + "/" + filename)
    return referImg_list



def get_num_list():
    num_list = []
    for i in range(0,10):
        word = read_directory('E:/refer1/refer1/'+ template[i])
        num_list.append(word)
    return num_list
nums_list = get_num_list()



def template_score(template,image):

    template_img=cv2.imdecode(np.fromfile(template,dtype=np.uint8),1)
    template_img = cv2.cvtColor(template_img, cv2.COLOR_RGB2GRAY)

    ret, template_img = cv2.threshold(template_img, 0, 255, cv2.THRESH_OTSU)
#     height, width = template_img.shape
#     image_ = image.copy()
#     image_ = cv2.resize(image_, (width, height))
    image_ = image.copy()

    height, width = image_.shape

    template_img = cv2.resize(template_img, (width, height))

    result = cv2.matchTemplate(image_, template_img, cv2.TM_CCOEFF)
    return result[0][0]


def template_matching(word_images):
    results = []

    for word_image in word_images:
        best_score = []
        for num_list in nums_list:
            score = []
            for num in num_list:
                result = template_score(num,word_image)
                score.append(result)
            best_score.append(max(score))
        i = best_score.index(max(best_score))
        # print(template[i])
        r = template[i]
        results.append(r)
    return results
word_images_ = word_images.copy()

result = template_matching(word_images_)
print(result)

digital="".join(result)

########## broker info #############
broker_address = "broker.emqx.io"
ClientID='#########'
user='########'
password='##########'
topic='#####'
port = 1883

def main(folder_path):
    """Main function."""
    img = get_image_in_folder(folder_path)
    if img is None:
        print(f"No images found in {folder_path}")
        return

    ########### Data Transmission start ##################
    data = {
        'Time': time_string,
        'Set_point': digital
    }

    paylord = json.dumps(data, sort_keys=True).encode('utf-8')
    print('send message %s on topic %s' % (topic, paylord))
    publish.single(topic, payload=paylord, hostname='broker.emqx.io')

if __name__ == "__main__":
    main("E:/Set_point/a") 
