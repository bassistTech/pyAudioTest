# pyAudioTest

Francis Deck, Nov. 10, 2024

This is my support libary for controlling the audio hardware on a Windows or Linux PC. It's a wrapper around the **pyAudio** library.

**Expect it to be difficult to use** and crash-prone, since it creates a background process. However, since I've begun using it routinely, it has stabilized, because I tend to use the same scripts over and over.

**Warning**: Audio amplifiers and speakers can cause hearing damage, and 
excessive signal amplitudes can damage your equipment, including your
computer. Use appropriate hearing protection. Do not use this program
with equipment that could generate dangerous voltages.

**Warning**: Your computer could take control of the audio outputs at any
time (for instance to produce alert sounds), outisde the control of
this program. Don't trust your computer to protect your hearing or equipment.

**How to get the library**: Navigate to a convenient folder for storing this repo, and execute:

	git clone https://github.com/bassistTech/pyAudioTest.git
	cd pyAudioTest
	pip install -e .
	cd ..

**How to use the app**: You need to get my ugly GUI generator

	git clone https://github.com/bassistTech/uglyGui.git
	cd uglyGui
	pip install -e

Note that I chose the "editable" mode, which leaves the code in the location where 
you placed it, and lets you make changes. You can also install without that option, 
which puts it in your site-packages folder.

If you look at my **requirements.txt** file, you'll notice that there are no version 
numbers for the libraries. This is by intent. Dependency hell used to be a big problem 
for Python programmers, and remains one at the cutting edge (e.g., machine learning). 
But things have gotten a lot better for mainstream scientific programming, especially 
since the key libraries -- **numpy/scipy** and **matlotlib** have matured. I haven't 
run into a dependency issue in years, unless I've dug up some old Python 2 code.

Depending on your Python installation, you may need more packages. This software 
is simple enough that you can follow the typical rule of thumb, which is that 
if a package is missing, install it with **pip install** and try agin.

**Windows** works with just plain **pyAudio** library.

**Linux** requires a somewhat more complicated installation. I've now tested the program
on a fresh Lubuntu installation, and admittedly, it's arduous. I've made it a bit more
complicated by using a virtual environment, but the benefit is that you can wipe it
clean if it doesn't work. I'm assuming a folder **gitRepos** which is how I installed it.

	sudo apt update
	sudo apt install python3-venv
	
	mkdir gitRepos
	cd gitRepos

	udo apt install python3-dev
	sudo apt install python3-pip
	sudo apt install portaudio19-dev
	pip3 install pyaudio
	sudo apt install python3-tk

	python3 -m venv venv
	source ./venv/bin/activate

	git clone https://github.com/bassistTech/uglyGui.git
	cd uglyGui
	pip3 install -e .
	cd ..

	git clone https://github.com/bassistTech/pyAudioTest.git
	cd pyAudioTest
	pip3 install -e .
	cd ..

The last thing is to run your preferred development environment, or use **spyder**.
By working inside the virtual environment, spyder will live there as well, and can
be deleted at will

	pip3 install spyder
	spyder
