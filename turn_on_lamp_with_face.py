# USAGE
# python turn_on_lamp_with_face.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle

#make sure to save images of your own face into the dataset folder (in a  folder with your name on it).  Then perform encodings with your own face to add it to the encodings.

#commented print statements are for debugging

#good luck hitting q to disable and get the nice exit message.  Just kill it from the terminal window with ctrl-c

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import requests

#enter your ifttt webhook key after the last slash below. Remove stars
turn_on_link = "https://maker.ifttt.com/trigger/face_recognized/with/key/*****"

#enter your IFTTT webhook key after the last slash below. Remove stars
turn_off_link = "https://maker.ifttt.com/trigger/no_face_recognized/with/key/*****"

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", required=True,
	help = "path to where the face cascade resides")
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
args = vars(ap.parse_args())

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(args["encodings"], "rb").read())
detector = cv2.CascadeClassifier(args["cascade"])

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# start the FPS counter
fps = FPS().start()

#instantiate light status indicator, change marker, and delay counters
status = "off"
changed = "no"
change_counter = 0
shutoff_delay_counter = 0
start_delay_counter = 0

# loop over frames from the video file stream
while True:

	#Lets do 1fps
	time.sleep(1)

	# grab the frame from the threaded video stream and resize it
	# to 500px (to speedup processing)
	frame = vs.read()
	frame = imutils.resize(frame, width=500)
	
	# convert the input frame from (1) BGR to grayscale (for face
	# detection) and (2) from BGR to RGB (for face recognition)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	# detect faces in the grayscale frame
	rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
		minNeighbors=5, minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE)
	
	# OpenCV returns bounding box coordinates in (x, y, w, h) order
	# but we need them in (top, right, bottom, left) order, so we
	# need to do a bit of reordering
	boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

	# compute the facial embeddings for each face bounding box
	encodings = face_recognition.face_encodings(rgb, boxes)
	names = []
	
	#print(not boxes)
	#print(status)
	#print(changed)

	#make it restart on first count-through
	if change_counter == 0 and not boxes:
		start_delay_counter = 0

	#find out if we turn light off
	if not boxes and status == 'on' and changed == 'yes':
		#we don't want it to turn off immediately.  Only after 5 minutes of no recognition
		shutoff_delay_counter = shutoff_delay_counter + 1
		start_delay_counter = 0
		#if 5 minutes  have passed then set light_status to "off"
		if shutoff_delay_counter == 300:
			#print(turn_off_link)			
			r = requests.post(url = turn_off_link)
			change_counter = change_counter + 1
			changed = "no"
			status = "off"

	# loop over the facial embeddings
	for encoding in encodings:
		# attempt to match each face in the input image to our known
		# encodings
		matches = face_recognition.compare_faces(data["encodings"],
			encoding)
		name = "Unknown"

		# check to see if we have found a match
		if True in matches:
			shutoff_delay_counter = 0
			#we also don't want it to respond to single frame false positives.  We'll make it hit 5 before we let it turn on the lights.			
			start_delay_counter = start_delay_counter + 1
			#set light_status to "on"
			if status == 'off' and changed == 'no' and start_delay_counter == 5:
				#print(turn_on_link)
				r = requests.post(url = turn_on_link)
				change_counter = change_counter + 1
				changed = "yes"
				status = "on"

			# find the indexes of all matched faces then initialize a
			# dictionary to count the total number of times each face
			# was matched
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}

			# loop over the matched indexes and maintain a count for
			# each recognized face face
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1

			# determine the recognized face with the largest number
			# of votes (note: in the event of an unlikely tie Python
			# will select first entry in the dictionary)
			name = max(counts, key=counts.get)

		# update the list of names
		names.append(name)

	# loop over the recognized faces
	for ((top, right, bottom, left), name) in zip(boxes, names):
		# draw the predicted face name on the image
		cv2.rectangle(frame, (left, top), (right, bottom),
			(0, 255, 0), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			0.75, (0, 255, 0), 2)

	# display the image to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

	# update the FPS counter
	fps.update()
	print('shutoff delay counter = ' + str(shutoff_delay_counter))
	print('start delay counter = ' + str(start_delay_counter))

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
print("[INFO] POST request calls: " +  str(change_counter))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
