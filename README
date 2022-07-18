# QCast

Created as The Advanced Project for MSBI 31600 Winter 2022
Muhammad Aji Muharrom

The main function of this simple application is to enable Google Chromecast-enabled devices
to play certain verses of the Qur'an independently.
To put simply, the Qur'an can be thought of as an audiobook that contains several chapters,
where each chapter contain variable number of verses.
With this application, a user can choose certain verses and play them on a Cast device
connected on the same local network.

I create this little app for my own use, as I own a Google Home Mini and want this capability.
However, I could not find a readily available solution. Existing solutions include mobile applications
which can play certain verses on the device. To play it on the cast, I have to set the Cast as a bluetooth
speaker and connect it to my device. With this app, I do not need to keep my device connected to the Cast,
because it just sends instructions and the Cast is the one who downloads and plays the audio files.

The class themes I utilized in this project includes GUI (which in itself pertains a whole bunch
of OOP programming), OOP in using external library, and a little Networking.

What I would do differently, or rather, what I would improve, is certainly the user interface.
I would love to have a more pleasant app doing this capability. I was considering using Django
and create the interface using HTML and all the responsive web good stuff, but ended up
trying Kivy instead because I don't want the hassle of running a web server endlessly and
want to simply have an app I can run on my phone.
If I am to redo this project, I would probably try to use the "Kv Language", some sort of
layouting language that kivy provides to simplify the code for UI layouts.

## Running the project

First, make sure all dependencies are available.
This project is made and tested using Python 3.9.7, so no guarantee it will run on other python versions.
To be safe, create a conda environment using this version and activate it.

`conda create -n py397-qcast python=3.9.7`
`conda activate py397-qcast`

I believe `kivy` and `pychromecast` are the only external libraries I used here, 
other libraries such as `requests` were part of Python 3 standard distribution.

So first, install kivy by running `conda install -c conda-forge kivy=2.0.0`

Then, we need to install pychromecast. Unfortunately, it's not available in conda, so we need to use pip

`conda install pip`
`pip install pychromecast==10.3.0`

Then, on the project directory, execute `python app.py` to run the application.

Once the app runs, click "Discover" to start the device discovery process.
Cast-enabled device(s) found will appear on the selector. Select the device and click "connect" to use the device.

After chapters and verses are selected, click "Play" to play the selected verses on the device!

Note: I included requirements.txt as part of this project, which includes all the packages needed to run this app.
However, I could not find an easy way to create a conda environment out of the requirements due to
the package(s) availability -- I could not find a single conda repository that has every requirement.

## Challenges

Among the challenges that I have to overcome during the project is understanding the external libraries.

Though pychromecast is powerful, it lacks documentation.
Well, to be fair, even Google's Cast SDK docs are not that complete.
However, pychromecast does include a bunch of examples which were really useful to learn from.

Kivy has better documentation, though not as good as perhaps tkinter. However, it is enough
to at least get the app to work!

The Quran.com team provides a well-documented API.

Acknowledgements thus go to the authors and contributors to these cool libraries and APIs.

References:
- https://github.com/home-assistant-libs/pychromecast
- https://github.com/home-assistant-libs/pychromecast/tree/master/examples
- https://kivy.org/doc/stable/gettingstarted/intro.html
- https://quran.api-docs.io/v4/getting-started/introduction

Another challenge and learning I got from this project was doing asynchronous programming in Python.
Having some experiences with Javascript, I would say that async programming requires more work
in Python compared to JS.

## Extra Credit

Extra credits I attempted are the use of interesting external library - kivy, and also concepts slightly
covered in class: threading. I tried to implement more asynchronous programming to avoid the application hangs
while certain processes are being executed.

I also attempted try..except error checking, one of them is inside the DeviceComponents.on_button_play_release()
method. If the "Repeat count" selector value has not been set, thus raising ValueError when casted,
it will catch the error and assign the value to "1" before proceeding.
