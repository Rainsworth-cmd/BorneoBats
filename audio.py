#-*- coding: utf-8 -*-
import os
import wave
from time import sleep
import numpy as np
import scipy.io.wavfile
import scipy.signal

SUCCESS = 0
FAIL = 1

def ZCR(curFrame):
    tmp1 = curFrame[:-1]
    tmp2 = curFrame[1:]
    sings = (tmp1 * tmp2 <= 0)
    diffs = (tmp1 - tmp2) > 0.02
    zcr = np.sum(sings * diffs)
    return zcr


def STE(curFrame):
    amp = np.sum(np.abs(curFrame))
    return amp


class Vad(object):


    def __init__(self):
        self.amp1 = 0
        self.amp2 = 0
        self.zcr1 = 0
        self.zcr2 = 0
        self.maxsilence = 100
        self.minlen = 40
        self.offsets = 40
        self.offsete = 40
        self.max_en = 20000
        self.status = 0
        self.count = 0
        self.silence = 0
        self.frame_len = 256
        self.frame_inc = 128
        self.cur_status = 0
        self.frames = []
        self.frames_start = []
        self.frames_start_num = 0
        self.frames_end = []
        self.frames_end_num = 0
        self.cache_frames = []
        self.cache = ""
        self.cache_frames_num = 0
        self.end_flag = False
        self.wait_flag = False
        self.on = True
        self.callback = None
        self.callback_res = []
        self.callback_kwargs = {}
        self.all_noise = False
    def clean(self):
        self.frames = []
        self.frames_start = []
        self.frames_start_num = 0
        self.frames_end = []
        self.frames_end_num = 0
        self.cache_frames = []
        self.cache_frames_num = 0
        self.end_flag = False
        self.wait_flag = False

    def go(self):
        self.wait_flag = False

    def wait(self):
        self.wait_flag = True

    def stop(self):
        self.on = False

    def add(self, frame, wait=True):
        if wait:
            print( 'wait')
            frame = self.cache + frame

        while len(frame) > self.frame_len:
            frame_block = frame[:self.frame_len]
            self.cache_frames.append(frame_block)
            frame = frame[self.frame_len:]
        if wait:
            self.cache = frame
        else:
            self.cache = ""
            self.cache_frames.append(-1)

    def run(self,hasNum):
        print ("START EVALUATION")
        step = self.frame_len - self.frame_inc
        num = 0
        while 1:
            if self.wait_flag:
                sleep(1)
                continue
            if len(self.cache_frames) < 2:
                sleep(0.05)
                continue

            if self.cache_frames[1] == -1:
                print( '----------------ALL NOISE--------------')
                self.all_noise = True
                break
            # Read data from buffer
            record_stream = b"".join(self.cache_frames[:2])
            #wave_data = np.fromstring(record_stream, dtype=np.int16)
            wave_data = np.frombuffer(record_stream, dtype=np.int16)
            wave_data = wave_data * 1.0 / self.max_en
            data = wave_data[np.arange(0, self.frame_len)]
            speech_data = self.cache_frames.pop(0)
            zcr = ZCR(data)
            amp = STE(data) ** 2
            res = self.speech_status(amp, zcr)

            if res == 2:
                hasNum += 1

            if hasNum > 10:
                print( '+++++++++++++++++++++++++HAS SOUND++++++++++++++++++++++++')
                break
            num = num + 1
            #test frame by frame
            self.frames_start.append(speech_data)
            self.frames_start_num += 1
            if self.frames_start_num == self.offsets:
                self.frames_start.pop(0)
                self.frames_start_num -= 1
            if self.end_flag:
                self.frames_end_num += 1
                if res == 2 or self.frames_end_num == self.offsete:
                    speech_stream = b"".join(self.frames + self.frames_end)
                    self.callback_res.append(self.callback(speech_stream, **self.callback_kwargs))
                    # self.clean()
                    self.end_flag = False

                    self.frames = []
                    self.frames_end_num = 0
                    self.frames_end = []

                self.frames_end.append(speech_data)
            if res == 2:
                if self.cur_status in [0, 1]:
                    self.frames.append(b"".join(self.frames_start))
                self.frames.append(speech_data)
            if res == 3:
                print ('Test ENDS')
                self.frames.append(speech_data)
                self.end_flag = True

            self.cur_status = res
            # return self.callback_res

    def speech_status(self, amp, zcr):
        status = 0
        # 0= slience/noise， 1=possible sound, 2=sound confirm
        if self.cur_status in [0, 1]:
            if amp > self.amp1:
                status = 2
                self.silence = 0
                self.count += 1
            elif amp > self.amp2 or zcr > self.zcr2:
                status = 1
                self.count += 1
            else:
                status = 0
                self.count = 0
                self.count = 0
        elif self.cur_status == 2:
            if amp > self.amp2 or zcr > self.zcr2:
                self.count += 1
                status = 2
            else:
                self.silence += 1
                if self.silence < self.maxsilence:
                    self.count += 1
                    status = 2
                elif self.count < self.minlen:
                    status = 0
                    self.silence = 0
                    self.count = 0
                else:
                    status = 3
                    self.silence = 0
                    self.count = 0
        return status


def read_file_data(filename):
    read_file = wave.open(filename, "r")
    params = read_file.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    data = read_file.readframes(nframes)
    return nchannels, sampwidth, framerate, data

class FileParser(Vad):
    def __init__(self):
        self.block_size = 256
        Vad.__init__(self)
    def read_file(self, filename):
        if not os.path.isfile(filename):
            print ("File %s Does not Exist!!!!" % filename)
            return FAIL
        datas = read_file_data(filename)[-1]
        self.add(datas, False)
        fs, wave = scipy.io.wavfile.read(filename)
        Vad.amp1 = 3* np.std(wave)
        Vad.amp2 = 4*np.std(wave)

if __name__ == "__main__":
    input_path = r"enter folder path here"
    stream_test = FileParser()
    for file in os.listdir(input_path):
        file_path = os.path.join(input_path, file)
        result = stream_test.read_file(file_path)
        if result != FAIL:
            stream_test.run(0)
            if (stream_test.all_noise == False):
                des_filename = os.path.join(input_path, 'modified-'+file)