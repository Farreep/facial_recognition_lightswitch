#~~~~~~~~~~~~~

#Hey, so this was designed by lesreaper based on the instructions of Adrian (work and great instructions available here: https://www.pyimagesearch.com/2018/06/25/raspberry-pi-face-recognition/).  Find lesreaper's work at https://github.com/lesreaper/pi-face-recognition, including the raw facial recognition files.

#The only thing I did myself was the adjustments the file now titled turn_on_lamp_with_face.py  That includes the tags in there to enable the starting and ending delays, the commented out print statements, and added the post requests.

#In order for this service to work, I am using IFTTT webhooks.  You can find plenty of documentation on that online.  I got some help from BRUH Automation on youtube for the details.  It was this video in particular: https://www.youtube.com/watch?v=-Tkb04xRs-o

#The open_CV_installation_steps.sh file will actually compile, build, and install the facial recognition thing from scratch.  Pretty sweet work by lesreaper.  You can follow the same steps on any system, just change the python version number to make sure it's accurate.

#Essentially the python script recognizes my face and dose a POST call.  This is a message out to IFTTT with my key in it, along with a tag I set (the tag corresponds with the recipe using the webhooks applet).  I then linked that to send a request to my personal server running Home Assistant.  I used DuckDNS.org to provide the DDNS.

#Home Assistant then reaches out to my IKEA Tradfri lights, and turns on the appropriate one.  I've starred out the key I use for IFTTT, deleted my encodings.pickle file, and removed my images.  To do the encodings and prep for facial recognition to work, follow the instructions and replace the "your_name_here" folder in the "dataset" folder.

#Thanks, and good luck!
#-Farreep
#~~~~~~~~~~~~

# Getting started

To get this running on your Raspberry Pi, you will need to clone this repository and then install OpenCV. As of November 3rd, 2018, I have a script that does all of this for you on a fresh install of Raspian Stretch!
Open up your terminal and type:
```
git clone https://github.com/lesreaper/pi-face-recognition.git
cd pi-face-recognition
chmod +x installOpenCV.sh
./installOpenCV.sh
```
Go and take a rest. This will take from 6 - 8 hours to install. We're building openCV 3.4.0 from source using only 1 CPU core (to make sure we don't run into any race condition errors). It's slow, but accurate.

This will create a virtual environment called "cv". So, anytime you want to work with OpenCV enabled, when you first open your terminal you'll type:
```
workon cv
```

If this fails, go ahead and restart your terminal, or type:

```source ~/.profile```

# Once OpenCV is installed

You'll need to download some pictures of yourself, and put them in a folder you create with your name. If your name is Rich, and you downloaded images of yourself from the internet to your Downloads folder as "image1.jpg", etc, you would do that this way:

```
workon cv
cd ~/pi-face-recognition/dataset
mkdir Rich
--go and fetch your images and either save them to ~/pi-face-recognition/dataset/Rich/ or Downloads if you can't customize the download path
cd ~/Downloads
sudo mv image1.jpg ~/pi-face-recognition/dataset/Rich/image1.jpg
--repeat the line above for each image, or you can drag and drop your downloaded images via the file explorer icon in your top toolbar
```

Then, once you have all the images of you in your labeled folder, create your embeddings:
```
cd ~/pi-face-recognition/
python encode_faces.py --dataset dataset --encodings encodings.pickle \
	--detection-method hog
``` 

Finally, you're ready to run your webcam, or run it on an image to test it.
To run on webcam:
```
python pi_face_recognition.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle
```

To run on a single image:
```
python pi_face_recognition_image.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle --image 6892945.jpeg
```

You can download your own image for testing and replace the image name above (6892945.jpeg) with your downloaded image name (the path is relative to the location of the pi_face_recognition*.py file).

This is all taken for the most part from Adrian's awesome blog here:
https://www.pyimagesearch.com/2018/06/25/raspberry-pi-face-recognition/

Buy his stuff. I've never taken a course that hasn't paid for itself many times over.

