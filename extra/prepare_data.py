import cv2
from utils import constants as cs
from utils import utility, os_utils
import os

def prepareTestData(drive):
    filenameListList = [filename for filename in (
        files for root, dirs, files in os.walk("/content/drive/MyDrive/data/videos/testing_data"))]

    filenameList = filenameListList[0]
    filenameList.sort()

    # print(filenameList)

    testStart = 0
    testEnd = 10
    testCurrent = 0

    for fName in filenameList[33:60]:
        path = "/content/drive/MyDrive/data/videos/testing_data/" + fName
        utility.write_test_videos(path, cs.DATA_TEST_VIDEOS,
                                  cs.DATA_BG_TEST_VIDEO, drive)


def prepareTrainData():
    IMAGE_SIZE = (12, 8)

    path_gen = os_utils.iterate_data(
        cs.BASE_DATA_PATH + cs.DATA_TRAIN_VIDEOS, ".mp4")

    page = 1
    size = 30

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

def main(drive):
  prepareTestData(drive)



# if __name__ == '__main__':
#     fg_bg = cv2.createBackgroundSubtractorMOG2()
#     IMAGE_SIZE = (12, 8)

#     path_gen = os_utils.iterate_data(cs.BASE_DATA_PATH + cs.DATA_TRAIN_VIDEOS, ".mp4")

#     for path in path_gen:
#         utility.write_videos(path, cs.DATA_TRAIN_VIDEOS, cs.DATA_BG_TRAIN_VIDEO)

#     path_gen = os_utils.iterate_test_data(cs.BASE_DATA_PATH + cs.DATA_TEST_VIDEOS, ".mp4")
#     for path in path_gen:
#         utility.write_videos(path, cs.DATA_TEST_VIDEOS, cs.DATA_BG_TEST_VIDEO)
