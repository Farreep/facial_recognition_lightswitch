echo "[Start]: Go do something else, this is going to take awhile..."
cd ~
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install build-essential cmake pkg-config -y
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev -y
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev -y
sudo apt-get install libxvidcore-dev libx264-dev -y
sudo apt-get install libgtk2.0-dev -y
sudo apt-get install libatlas-base-dev gfortran -y
sudo apt-get install python2.7-dev python3-dev -y
cd ~
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.4.0.zip
unzip opencv.zip
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.4.0.zip
unzip opencv_contrib.zip
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo pip install virtualenv virtualenvwrapper
sudo rm -rf ~/.cache/pip
echo -e "\n# virtualenv and virtualenvwrapper" >> ~/.profile
echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.profile
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.profile
source ~/.profile
mkvirtualenv cv -p python3
workon cv
pip install numpy
cd ~/opencv-3.4.0/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D ENABLE_PRECOMPILED_HEADERS=OFF \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.4.0/modules \
    -D BUILD_EXAMPLES=ON ..
make
sudo make install
sudo ldconfig
cd /usr/local/lib/python3.5/site-packages/
sudo mv cv2.cpython-35m-arm-linux-gnueabihf.so cv2.so
cd ~/.virtualenvs/cv/lib/python3.5/site-packages/
ln -s /usr/local/lib/python3.5/site-packages/cv2.so cv2.so
cd ~
source ~/.profile
workon cv
echo "[Complete]: Test your OpenCV install by typing 'python', 'import cv2', and then 'cv2.__version__'"
echo "[Complete]: It should say: 3.4.0"
echo "[Complete]: If the command 'python' loads Python 2.7.*, this is wrong. The virtual environment didn't load. "
echo "[Complete]: Type: 'source ~/.profile' and 'workon cv'. Then, try again."
