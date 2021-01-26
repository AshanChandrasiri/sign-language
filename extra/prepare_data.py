import cv2
from utils import constants as cs
from utils import utility, os_utils


def main(drive):

    IMAGE_SIZE = (12, 8)

    path_gen = os_utils.iterate_data(
        cs.BASE_DATA_PATH + cs.DATA_TRAIN_VIDEOS, ".mp4")

    page = 0
    size = 1

    current = 0

    start = page * size
    end = start + size

    for path in path_gen:

        if(start <= current and current < end):
            print('********** start excuting *********** ' + str(current))
            utility.write_videos(path, cs.DATA_TRAIN_VIDEOS,
                                 cs.DATA_BG_TRAIN_VIDEO, drive)
        elif(current >= end):
            print('**********loop terminate***********')
            break

        current = current + 1
    #path_gen = os_utils.iterate_test_data(cs.BASE_DATA_PATH + cs.DATA_TEST_VIDEOS, ".mp4")
    # for path in path_gen:
       #   utility.write_videos(path, cs.DATA_TEST_VIDEOS, cs.DATA_BG_TEST_VIDEO)

# if __name__ == '__main__':
#     fg_bg = cv2.createBackgroundSubtractorMOG2()
#     IMAGE_SIZE = (12, 8)

#     path_gen = os_utils.iterate_data(cs.BASE_DATA_PATH + cs.DATA_TRAIN_VIDEOS, ".mp4")

#     for path in path_gen:
#         utility.write_videos(path, cs.DATA_TRAIN_VIDEOS, cs.DATA_BG_TRAIN_VIDEO)

#     path_gen = os_utils.iterate_test_data(cs.BASE_DATA_PATH + cs.DATA_TEST_VIDEOS, ".mp4")
#     for path in path_gen:
#         utility.write_videos(path, cs.DATA_TEST_VIDEOS, cs.DATA_BG_TEST_VIDEO)
