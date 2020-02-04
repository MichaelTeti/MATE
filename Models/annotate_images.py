import cv2, os, imageio, csv
import numpy as np
from random import shuffle
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('input_dir',
    type=str,
    help='Path to the input video directories.')
parser.add_argument('annotation_output_dir',
    type=str,
    help='Path to the desired output annotation directory.')
parser.add_argument('image_output_dir',
    type=str,
    help='Path to the desired image output directory.')
parser.add_argument('n_classes',
    type=int,
    help='The number of classes you are going to identify.')
parser.add_argument('--img_size',
    type=int,
    default=416,
    help='Size to make the image.')
args = parser.parse_args()

args.input_dir = os.path.abspath(args.input_dir)
args.annotation_output_dir = os.path.abspath(args.annotation_output_dir)
args.image_output_dir = os.path.abspath(args.image_output_dir)

if not os.path.isdir(args.annotation_output_dir):
    os.mkdir(args.annotation_output_dir)
if not os.path.isdir(args.image_output_dir):
    os.mkdir(args.image_output_dir)

assert(args.n_classes > 0), 'n_classes must be greater than 0, but it is {}.'.format(args.n_classes)


def shape_selection(event, x, y, flags, param):
    # grab references to the global variables
    global ref_point, crop, n_labels_per_class, display_name

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being performed
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        ref_point.append((x, y))

        # draw a rectangle around the region of interest
        cv2.rectangle(img, ref_point[0], ref_point[1], (0, 255, 0), 1)
        cv2.imshow(display_name, img)
        ref_points.append(ref_point)
        n_labels_per_class[i_class] += 1


img_fnames = [os.path.join(root, f) for root,_,files in os.walk(args.input_dir) for f in files]
print('[INFO] FOUND {} IMAGES IN THE INPUT DIRECTORY.'.format(len(img_fnames)))

shuffle(img_fnames) # shuffle them up so they're not in any particular order to increase labeling efficiency
current_output_files = os.listdir(args.annotation_output_dir)


for i_img_fname, img_fname in enumerate(img_fnames):
    if os.path.split(img_fname)[1].split('.')[0] + '.txt' not in current_output_files:
        display_name = os.path.split(img_fname)[1]
        img = cv2.imread(img_fname)  # read in each image one at a time
        img = img[..., :-1] if img.shape[-1] == 4 else img
        h, w = img.shape[:2]

        if h != w:
            if h < w:
                img = np.pad(img, ((0, w-h), (0, 0), (0, 0)))
            elif w < h:
                img = np.pad(img, ((0, 0), (0, h-w), (0, 0)))

        img = cv2.resize(img, (args.img_size, args.img_size))

        img_save = img.copy()
        img_h, img_w = img.shape[:2]
        ref_point, ref_points = [], []
        annotation_file = os.path.join(args.annotation_output_dir, os.path.split(img_fname)[1].split('.')[0] + '.txt')

        clone = img.copy()
        cv2.namedWindow(display_name)
        cv2.setMouseCallback(display_name, shape_selection)
        n_labels_per_class = [0] * args.n_classes


        for i_class in range(args.n_classes):
            print('SELECT ALL INSTANCES OF CLASS {}'.format(i_class))

            while True:
                # display the image and wait for a keypress
                cv2.imshow(display_name, img)
                key = cv2.waitKey(1) & 0xFF

                # press 'r' to reset the window
                if key == ord("r"):
                    img = clone.copy()
                    ref_points = []

                # if the 'c' key is pressed, break from the loop
                elif key == ord("c"):
                    break

        # close all open windows
        cv2.destroyAllWindows()

        if ref_points != []:
            txtfile = open(os.path.join(args.annotation_output_dir, annotation_file), 'a')
            writer = csv.writer(txtfile, delimiter=' ')
            current_class = 0

            for i_box, box in enumerate(ref_points):
                x_start, y_start = box[0][0] / img_w, box[0][1] / img_h
                x_end, y_end = box[1][0] / img_w, box[1][1] / img_h
                box_w, box_h = x_end - x_start, y_end - y_start
                box_cx, box_cy = x_start + (box_w / 2), y_start + (box_h / 2)
                box_w, box_h = np.absolute(box_w), np.absolute(box_h)

                if i_box + 1 > sum(n_labels_per_class[:current_class+1]):
                    current_class += 1

                writer.writerow([current_class, box_cx, box_cy, box_w, box_h])

            txtfile.close()

            cv2.imwrite(os.path.join(args.image_output_dir, os.path.split(img_fname)[1]), img_save)

    else:
        print('[INFO] SKIPPING FILE. ANNOTATION ALREADY EXISTS.')
