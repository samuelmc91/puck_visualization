import os
import cv2
import numpy as np
from sklearn import svm
import pickle
import random
from sklearn.model_selection import train_test_split
import sys

categories = ['bad_cap', 'good_cap']
# Train directory
base_dir = os.path.join(os.getcwd(), 'train')

# Condensing the images
def make_image_pickle(filename):
    data = []
    for category in categories:
        category_path = os.path.join(base_dir, category)
        label = categories.index(category)
        print(category_path)
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

    pic_in = open(filename, 'wb')
    pickle.dump(data, pic_in)
    pic_in.close()

# Formating the image for prediction
def prediction_format(img):
    img = cv2.imread(img)
    img_resize = cv2.resize(img, (50,50))
    img_flatten = np.array(img_resize).flatten()
    return img_flatten


filename = 'level_two_pickle.pickle'
if not os.path.exists(os.path.join(os.getcwd(), filename)):
    make_image_pickle(filename)
pic_in = open(filename, 'rb')
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
    testing_images_bad = os.path.join(os.getcwd(), 'test')
    bad_testing_images = os.path.join(testing_images_bad, 'bad_cap')

    testing_images_good = os.path.join(os.getcwd(), 'test')
    good_testing_images = os.path.join(testing_images_good, 'good_cap')

    print_categories = ['Bad Cap', 'Good Cap']

    f = open('Bad_Cap.txt', 'w')
    f.write('Bad Cap Directory\n')

    test_accuracy = 0
    good_cap = 0
    bad_cap = 0
    for image in os.listdir(bad_testing_images):
        img = os.path.join(bad_testing_images, image)
        prediction = svc.predict(prediction_format(img).reshape(1, -1))
        f.write('\nImage: {} \nPrediction: {}\n'.format(image, print_categories[prediction[0]]))
        # f.write(print_categories[prediction[0]] + '\n')
        if categories[prediction[0]] == 'good_cap':
            good_cap += 1
        else:
            bad_cap += 1
    test_accuracy = bad_cap / (bad_cap + good_cap)
    f.write('\nBad Caps: {} \nGood Caps: {}\n'.format(str(bad_cap), str(good_cap)))
    f.write('Real Time Accuracy: ' + str(test_accuracy))
    f.close()
    
    f = open('Good_Cap.txt', 'w')
    f.write('Good_Cap Directory\n')
    test_accuracy = 0
    good_cap = 0
    bad_cap = 0
    for image in os.listdir(good_testing_images):
        img = os.path.join(good_testing_images, image)
        prediction = svc.predict(prediction_format(img).reshape(1, -1))
        f.write('\nImage: {} \nPrediction: {}\n'.format(image, print_categories[prediction[0]]))
        # f.write(print_categories[prediction[0]] + '\n')
        if categories[prediction[0]] == 'good_cap':
            good_cap += 1
        else:
            bad_cap += 1
    test_accuracy = good_cap / (bad_cap + good_cap)
    f.write('\nBad Caps: {} \nGood Caps: {}\n'.format(str(bad_cap), str(good_cap)))
    f.write('Real Time Accuracy: ' + str(test_accuracy))
    f.close()