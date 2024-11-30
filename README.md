# pyAudioTest

Francis Deck, Nov. 10, 2024

This is my support libary for controlling the audio hardware on a Windows PC. *I hope it also works under Linux, but haven't tested it yet.* It's a wrapper around the **pyAudio** library.

**Expect it to be difficult to use** and crash-prone, since it creates a background process. However, since I've begun using it routinely, it has stabilied, because I tend to use the same scripts over and over.

**Warning**: Audio amplifiers and speakers can cause hearing damage, and 
excessive signal amplitudes can damage your equipment, including your
computer. Use appropriate hearing protection. Do not use this program
with equipment that could generate dangerous voltages.

**Warning**: Your computer could take control of the audio outputs at any
time (for instance to produce alert sounds), outisde the control of
this program. Don't trust your computer to protect your hearing or equipment.

**How to get it**: Navigate to a convenient folder for storing this repo, and execute:

	git clone https://github.com/bassistTech/pyAudioTest.git
	cd pyAudioTest
	pip install -e .

Note that I chose the "editable" mode, which leaves the code in the location where you placed it, and lets you make changes. You can also install without that option, which puts it in your site-packages folder.

If you look at my **requirements.txt** file, you'll notice that there are no version numbers for the libraries. This is by intent. Dependency hell used to be a big problem for Python programmers, and remains one at the cutting edge (e.g., machine learning). But things have gotten a lot better for mainstream scientific programming, especially since the key libraries -- **numpy/scipy** and **matlotlib** have matured. I haven't run into a dependency issue in years, unless I've dug up some old Python 2 code.