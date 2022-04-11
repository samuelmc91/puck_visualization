import os
import cv2
import numpy as np
from sklearn import svm
import pickle
import random
from sklearn.model_selection import train_test_split
import sys

categories = ['empty', 'puck']
# Train directory
base_dir = os.path.join(os.getcwd(), 'train')

# Condensing the images
def make_image_pickle(categories, filename):
    data = []
    for category in categories:
        category_path = os.path.join(base_dir, category)
        label = categories.index(category)

        for img in os.listdir(category_path):
            img_path = os.path.join(category_path, img)
            img = cv2.imread(img_path)
            try:
                img_resize = cv2.resize(img, (50,50))
                img_flatten = np.array(img_resize).flatten()
                data.append([img_flatten, label])
            except Exception as e:
                pass

    print(len(data))

    pic_in = open('data1.pickle', 'wb')
    pickle.dump(data, pic_in)
    pic_in.close()

# Formating the image for prediction
def prediction_format(img):
    img = cv2.imread(img)
    img_resize = cv2.resize(img, (50,50))
    img_flatten = np.array(img_resize).flatten()
    return img_flatten

# Getting the pickle
pic_in = open('data1.pickle', 'rb')
data = pickle.load(pic_in)
pic_in.close()

random.shuffle(data)

features = []
labels = []

for feature, label in data:
    features.append(feature)
    labels.append(label)

x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, shuffle=True)

# Creating the support vector classifier 
svc = svm.SVC(C=1, kernel='poly', gamma='auto')
svc.fit(x_train, y_train)

prediction = svc.predict(x_test)

accuracy = svc.score(x_test, y_test)

print(accuracy)

# input_prediction = svc.predict(prediction_format(sys.argv[1]).reshape(1, -1))
# print(input_prediction)

if __name__ == '__main__':
    testing_images_empty = os.path.join(os.getcwd(), 'test')
    empty_testing_images = os.path.join(testing_images_empty, 'empty')

    testing_images_puck = os.path.join(os.getcwd(), 'test')
    puck_testing_images = os.path.join(testing_images_puck, 'puck')

    print_categories = ['Empty', 'Puck']

    f = open('Empty.txt', 'w')
    f.write('Empty Directory\n')
    for image in os.listdir(empty_testing_images):
        img = os.path.join(empty_testing_images, image)
        prediction = svc.predict(prediction_format(img).reshape(1, -1))
        f.write(print_categories[prediction[0]] + '\n')

    f.close()
    f = open('Puck.txt', 'w')
    f.write('Puck Directory\n')
    for image in os.listdir(puck_testing_images):
        img = os.path.join(puck_testing_images, image)
        prediction = svc.predict(prediction_format(img).reshape(1, -1))
        f.write(print_categories[prediction[0]] + '\n')

    f.close()