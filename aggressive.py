from scipy.io.wavfile import read
from scipy.io.wavfile import write
from scipy import signal
import matplotlib.pyplot as plt
#get_ipython().magic('matplotlib inline')
import pylab as pl
import numpy as np
import sys
import wave as we

(Frequency, array) = read('test28.wav')

len(array)


NewSound = array
wn1 = 30000/ 250000
wn2 = 150000/250000
b,a = signal.butter(10,[wn1, wn2], btype='bandpass')

filteredSignal = signal.lfilter(b,a,NewSound)

write("output.wav", Frequency, np.int16(filteredSignal/np.max(np.abs(filteredSignal)) * 32767))


def wavread(path):
     wavfile =  we.open(path,"rb")
     params = wavfile.getparams()
     framesra,frameswav= params[2],params[3]
     nchannels, sampwidth, framesra, frameswav = params[:4]
     print("nchannels:%d" % nchannels)
     print("sampwidth:%d" % sampwidth)
     datawav = wavfile.readframes(frameswav)
     wavfile.close()
     datause = np.fromstring(datawav,dtype = np.short)
     print(len(datause))
     if nchannels == 2:
         datause.shape = -1,2
     datause = datause.T
     time = np.arange(0, frameswav) * (1.0/framesra)
     return datause,time,nchannels
def main():
     path = "./output.wav"
     wavdata,wavtime,nchannels = wavread(path)

     N=len(wavdata)
     framerate = 16000
     start=0
     df = 1
     freq = [df*n for n in range(0,len(wavdata))]
     print(len(wavdata))
     print(len(wavtime))

     c=np.fft.fft(wavdata)*nchannels
     d=int(len(c)/2)
     print(len(c))

     fig, ax = plt.subplots(2, 1)


     ax[0].plot(wavtime,wavdata,color = 'green')
     ax[0].set_xlabel('Time')
     ax[0].set_ylabel('Amplitude')


     ax[1].plot(freq,abs(c),color = 'red')
     ax[1].set_xlabel('Freq(HZ)')
     ax[1].set_ylabel('Y(freq)')

     plt.show()

main();