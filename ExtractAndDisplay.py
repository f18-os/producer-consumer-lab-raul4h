#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
import queue

# filename of clip to load
filename = 'clip.mp4'

#Maximum size for the buffer
MAX_SIZE = 10

#Semaphores
colorSemaphore = threading.Semaphore(MAX_SIZE)
graySemaphore = threading.Semaphore(MAX_SIZE)

# shared queue
extractionQueue = queue.Queue(MAX_SIZE)

#Grayscale Queue
grayscaleQueue = queue.Queue(MAX_SIZE)

def extractFrames():
    # Initialize frame count
    count = 0

    # open video file
    vidcap = cv2.VideoCapture(filename)

    # read first image
    success,image = vidcap.read()


    print("Reading frame {} {} ".format(count, success))
    while success:
        # get a jpg encoded frame
        success, jpgImage = cv2.imencode('.jpg', image)


        #encode the frame as base 64 to make debugging easier
        jpgAsText = base64.b64encode(jpgImage)

        # add the frame to the buffer
        extractionQueue.put(jpgAsText)
        colorSemaphore.acquire()

        success,image = vidcap.read()
        print('Reading frame {} {}'.format(count, success))
        count += 1

    print("Frame extraction complete")
    extractionQueue.put("done")


def convertToGrayscale():
    count = 0

    #Get first frame
    frameAsText = extractionQueue.get()
    colorSemaphore.release()

    # go through each frame in the buffer until the buffer is empty
    while frameAsText != "done":

        if(extractionQueue.empty()):
            pass

        # decode the frame
        jpgRawImage = base64.b64decode(frameAsText)

        # convert the raw frame to a numpy array
        jpgImage = np.asarray(bytearray(jpgRawImage), dtype=np.uint8)

        # get a jpg encoded frame
        img = cv2.imdecode( jpgImage ,cv2.IMREAD_UNCHANGED)

        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # get a jpg encoded frame
        success, jpgImage = cv2.imencode('.jpg', grayscaleFrame)

        #encode the frame as base 64 to make debugging easier
        jpgAsText = base64.b64encode(jpgImage)

        # add the frame to the buffer
        grayscaleQueue.put(jpgAsText)
        graySemaphore.acquire()

        print("Converting frame {}".format(count))

        count += 1

        #Get next frame
        frameAsText = extractionQueue.get()
        colorSemaphore.release()

    print("Finished converting all frames")
    grayscaleQueue.put("done")
    graySemaphore.acquire()

def displayFrames():
    # initialize frame count
    count = 0

    # get the first frame
    frameAsText = grayscaleQueue.get()
    graySemaphore.release()

    # go through each frame in the buffer until the buffer is empty
    while frameAsText != "done":

        if(grayscaleQueue.empty()):
            pass

        # decode the frame
        jpgRawImage = base64.b64decode(frameAsText)

        # convert the raw frame to a numpy array
        jpgImage = np.asarray(bytearray(jpgRawImage), dtype=np.uint8)

        # get a jpg encoded frame
        img = cv2.imdecode( jpgImage ,cv2.IMREAD_UNCHANGED)

        print("Displaying frame {}".format(count))

        # display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow("Video", img)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        count += 1

        # get the next frame
        frameAsText = grayscaleQueue.get()
        graySemaphore.release()

    print("Finished displaying all frames")
    # cleanup the windows
    cv2.destroyAllWindows()


#Threads
extractThread = threading.Thread(target=extractFrames)
grayThread = threading.Thread(target=convertToGrayscale)
displayThread = threading.Thread(target=displayFrames)


extractThread.start()
grayThread.start()
displayThread.start()

# extract the frames
# extractFrames(filename,extractionQueue)
#
# #convert the frames
# convertToGrayscale(extractionQueue, grayscaleQueue)
#
# # display the frames
# displayFrames(grayscaleQueue)
