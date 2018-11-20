# producer-consumer-lab-raul4h

## How To Run The Lab

In the command line once in the root folder of this lab please enter:
* python3 ExtractAndDisplay.py

## Explanation

In order to convert the video to grayscale and display it in the screen, I had to do three things:
* Create a method that would take the frames in color and convert them to grayscale
* Create a new queue that will contain the grayscale images, this in order for the color Queue to not be altered while displaying
* Create three separate threads for each of the steps in the process to work concurrently

Each thread except for the extraction of frames runs infinately until there is a signal from the previous thread that it is done, in the meantime it just waits for input for the previous thread
