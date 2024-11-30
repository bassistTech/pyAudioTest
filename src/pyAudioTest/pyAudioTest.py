'''
Audio tone cluster generator and analyzer

Copyright 2024 Francis Deck

Permission is hereby granted, free of charge, to any person obtaining 
a copy of this software and associated documentation files 
(the “Software”), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, 
merge, publish, distribute, sublicense, and/or sell copies of 
the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be 
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Warning: Audio amplifiers and speakers can cause hearing damage, and 
excessive signal amplitudes can damage your equipment, including your
computer. Use appropriate hearing protection. Do not use this program
with equipment that could generate dangerous voltages.

Warning: Your computer could take control of the audio outputs at any
time (for instance to produce alert sounds), outisde the control of
this program.
'''

'''
Audio tone cluster generator and analyzer

(C) 2022 Francis Deck
MIT License

Warning: Audio amplifiers and speakers can cause hearing damage, and
excessive signal amplitudes can damage your equipment, including your
computer. Use appropriate hearing protection. Do not use this program
with equipment that could generate dangerous voltages.

Warning: Your computer could take control of the audio outputs at any
time (for instance to produce alert sounds), outisde the control of
this program.
'''

import numpy as np
import pyaudio

'''
Setup parameters
'''

blockLength = 16384  # Samples per FFT block, needs to be power of 2
sampleRateHz = 44100  # Audio sampling rate in Hz
numChannels = 2  # number of audio channels
plotColors = ['g', 'r']  # standard plotColors for the two channels
fmin = 10  # trial starting frequency for tone cluster
fmax = 20000  # upper frequency limit for tone cluster
ratio = 1.1  # approximate frequency ratio between tones

'''
Globals
'''

frequencyScale = np.fft.rfftfreq(blockLength, d=1/sampleRateHz)[:-1]
timeScale = np.linspace(0, blockLength/sampleRateHz, blockLength)
audioData = np.empty(blockLength*numChannels)
globals = {'cycle_count': 0, 'amplitude': 1.0, 'exptcycle': 0, 'generate': 0}

'''
Computation of tone cluster waveform, built one frequency at a time
'''

i = int(np.ceil(fmin*blockLength/sampleRateHz))  # Starting # of cycles per block
toneIndex = []  # List of index values for discrete tones
toneFrequency = []  # list of frequencies in Hz
waveform_tc = np.zeros((numChannels, blockLength))
waveform_sine = np.zeros((numChannels, blockLength))

sine_index = 22

while True:
    toneIndex.append(i)
    toneFrequency.append(frequencyScale[i])
    f = i*sampleRateHz/blockLength  # Get this frequency

    omega = 2*np.pi*f
    phase = np.random.rand()*2*np.pi
    waveform_tc[0] = waveform_tc[0] + np.sin(omega*timeScale + phase)

    if len(toneIndex) == sine_index:
        waveform_sine[0] = np.sin(omega*timeScale + phase)
        sine_frequency = f

    fnext = f*ratio  # Estimate the next frequency
    i = int(np.ceil(fnext*blockLength/sampleRateHz))  # Convert to next higher integer
    if fnext > fmax:
        break

print('sine frequency', sine_frequency)

'''
Apply maximum amplitudes to the waveforms, just short of 32k
'''

waveform_tc[0] = waveform_tc[0]*30000/max(abs(waveform_tc[0]))
waveform_sine[0] = waveform_sine[0]*30000/max(abs(waveform_sine[0]))

'''
Build stereo waveforms as needed. The 'F' order produces alternating left/right
values in the array, as needed by the audio library
'''

if numChannels == 2:
    waveform_tc = waveform_tc.reshape((blockLength*numChannels), order='F')
    waveform_sine = waveform_sine.reshape((blockLength*numChannels), order='F')

'''
Form into integer arrays, which are fed to the audio library
'''

tc_block = np.array(waveform_tc, dtype=np.int16)
sine_block = np.array(waveform_sine, dtype=np.int16)
zero_block = np.zeros_like(tc_block)

'''
By necessity the audio callback must manipulate a global variable
containing the raw audio data, because it has no other mechanism
for making the data available to the rest of the program.
'''


def audioCallback(in_data, frame_count, time_info, status):
    # pylint: disable=unused-argument
    '''
    This routine is called whenever the audio library has received
    frames of data, like an interrupt service routine.

    An "overrun" occurs if this program is too slow to proces the
    data frames as they are received, probably because your computer
    is too slow.
    '''

    if frame_count > blockLength:
        print('overrun', frame_count)
    audioData[:] = np.frombuffer(in_data, np.int16)
    globals['cycle_count'] = globals['cycle_count'] + 1

    '''
    Whatever gets returned by this function, is passed to the audio
    output generator
    '''

    if globals['generate'] == 1:
        return (tc_block, pyaudio.paContinue)
    elif globals['generate'] == 2:
        return (sine_block, pyaudio.paContinue)
    else:
        return (zero_block, pyaudio.paContinue)


def startAudio():
    audio = pyaudio.PyAudio()

    stream = audio.open(format=pyaudio.paInt16,
                        channels=numChannels,
                        rate=sampleRateHz,
                        output=True,
                        input=True,
                        frames_per_buffer=blockLength,
                        stream_callback=audioCallback,
                        start=False)  # delaying start until everything is ready

    stream.start_stream()

    return audio, stream


def stopAudio(stream):
    stream.stop_stream()
    stream.close()


def analyzeAudio(stream):
    data_raw = audioData.reshape((blockLength, numChannels)).transpose()
    data_sub = np.empty_like(data_raw)
    rawfft = np.empty((data_raw.shape[0], data_raw.shape[1]//2), dtype=np.cdouble)
    dbfft = np.empty((data_raw.shape[0], data_raw.shape[1]//2), dtype=float)
    for i in range(data_raw.shape[0]):
        data_sub[i] = data_raw[i] - np.average(data_raw[i])
        rawfft[i] = ((np.fft.rfft(data_sub[i])))[:-1]
        dbfft[i] = 20*np.log10(abs(rawfft[i]))
        dbfft[i, 0] = 0
    result = {'data': data_sub, 'rawfft': rawfft, 'dbfft': dbfft}
    return result

def waitCycle():
    cc = globals['cycle_count']
    while globals['cycle_count'] == cc:
        pass