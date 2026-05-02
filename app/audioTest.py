'''
GUI based audio analyzer

Francis Deck, 11-30-2024

This is an extremely crude and ugly audio analyzer based on my pyAudioTest and 
uglyGui libraries. I wrote it to have an audio analyzer on an old notebook
PC in my workshop. Use and enjoy. Please heed my warning, that this program
takes control of your audio hardware, and may generate very loud signals,
which could damage your equipment and your hearing. In addition, the OS may
also produce audio signals during your testing, which my program does not
control.
'''

import numpy as np

import pyAudioTest as pat
import uglyGui as ug
import config
import json
#import os

'''
Monkey patch... we're among friends
'''

pat.globals['baseline'] = np.zeros_like(pat.frequencyScale)

def plot_waveform(data):
    graph.axes[0].clear()
    graph.axes[0].plot(pat.timeScale, data['data'][0])
    if cb_clipboard.get() == 1:
        blob = {'timeScale': pat.timeScale.tolist(), 'data': data['data'][0].tolist()}
        md.clipboard_clear()
        md.clipboard_append(json.dumps(blob))
        cb_clipboard.upd(0)

def plot_db(data):
    if cb_set_baseline.get() == 1:
        pat.globals['baseline'] = data['dbfft'][0]
        cb_set_baseline.upd(0)
    data_sub = data['dbfft'][0] - pat.globals['baseline']
    graph.axes[1].clear()
    if pat.globals['generate'] != 1:   
        graph.axes[1].semilogx(pat.frequencyScale, data_sub)
        blob = {'frequencyScale': pat.frequencyScale.tolist(), 'data_sub': data_sub.tolist()}
    if rb_generate.get() == 1:
        blob = {'frequencyScale': pat.frequencyScale.tolist(), 'dbfft': data['dbfft'][0].tolist()}
        graph.axes[1].semilogx(pat.toneFrequency, data_sub[pat.toneIndex], marker = '.')
    if cb_clipboard.get() == 1:
        md.clipboard_clear()
        md.clipboard_append(json.dumps(blob))
        cb_clipboard.upd(0)

def plot_linear(data):
    graph.axes[1].clear()
    graph.axes[1].semilogx(pat.frequencyScale, np.abs(data['rawfft'][0]))

def go_single():
    if cb_clear_baseline.get() == 1:
        pat.globals['baseline'] = pat.globals['baseline']*0
        cb_clear_baseline.upd(0)
    pat.waitCycle()
    data = pat.analyzeAudio(stream)
    plot_waveform(data)
    if cb_db.get() == 1:
        plot_db(data)
    else:
        plot_linear(data)
    graph.update()

def go_free_run():
    if cb_free_run.get() == 1:
        go_single()
        md.after(500, go_free_run)

def go_generate():
    pat.globals['generate'] = rb_generate.get()

md = ug.MainDialog('pyAudioTest')
graph = ug.Graph(md, 2, 1)
cb_db = ug.CheckBox(md, 'dB scale', 0, None)
cb_set_baseline = ug.CheckBox(md, 'Set baseline', 0, None)
cb_clear_baseline = ug.CheckBox(md, 'Clear baseline', 0, None)
rb_generate = ug.RadioButtons(md, 'Signal generator', ['Off', 'ToneCluster', 'Sine'], 
                              0, False, go_generate)
b_single = ug.Button(md, 'Single reading', go_single)
cb_free_run = ug.CheckBox(md, 'Free run', 0, go_free_run)
cb_clipboard = ug.CheckBox(md, 'Copy to clipboard', 0, None)
input_device = config.input_device
output_device = config.output_device
stream = pat.startAudio()
md.show()
pat.stopAudio(stream)