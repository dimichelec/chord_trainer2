import numpy as np
import pyaudio
from pprint import pprint
import re


class audio:

    # ----------------------------------------------------------------------------------------------
    #
    # Utilities

    # print the set of input or output audio devices
    def print_device_set(self, inout, filter=None, verbose=False):
        for device in range (self.audioinstance.get_device_count()):
            ins    = self.audioinstance.get_device_info_by_index(device)['maxInputChannels']
            outs   = self.audioinstance.get_device_info_by_index(device)['maxOutputChannels']
            rate   = self.audioinstance.get_device_info_by_index(device)['defaultSampleRate']
            inlat  = self.audioinstance.get_device_info_by_index(device)['defaultHighInputLatency']
            outlat = self.audioinstance.get_device_info_by_index(device)['defaultHighOutputLatency']
            name   = self.audioinstance.get_device_info_by_index(device)['name']
            name   = re.sub(r'[\r,\n]+',' ', name)
            if inout == 0:  # input devices
                if filter is None or filter in name:
                    if ins > 0 or verbose:
                        if verbose:
                            print()
                        print(f'{device}: {name} - {rate/1000:.1f}kHz - {inlat*1000:.0f}ms')
                        if verbose:
                            pprint(self.audioinstance.get_device_info_by_index(device), indent=2)
            else:   # output devices
                if filter is None or filter in name:
                    if outs > 0 or verbose:
                        if verbose:
                            print()
                        print(f'{device}: {name} - {rate/1000:.1f}kHz - {outlat*1000:.0f}ms')
                        if verbose:
                            pprint(self.audioinstance.get_device_info_by_index(device), indent=2)


    # print basic device list
    def print_devices(self, io=None, filter=None, verbose=False):
        if io in [None, 0]:
            print("\nIns:")
            self.print_device_set(0, filter, verbose)
        if io in [None, 1]:
            print("\nOuts:")
            self.print_device_set(1, filter, verbose)


    # get fastest devices by latency
    def get_fastest_devices(self, inout, filter=None):
        devices = []
        for device in range (self.audioinstance.get_device_count()):
            ins    = self.audioinstance.get_device_info_by_index(device)['maxInputChannels']
            outs   = self.audioinstance.get_device_info_by_index(device)['maxOutputChannels']
            rate   = self.audioinstance.get_device_info_by_index(device)['defaultSampleRate']
            inlat  = self.audioinstance.get_device_info_by_index(device)['defaultHighInputLatency']
            outlat = self.audioinstance.get_device_info_by_index(device)['defaultHighOutputLatency']
            name   = self.audioinstance.get_device_info_by_index(device)['name']
            name   = re.sub(r'[\r,\n]+',' ', name)
            if inout == 0:  # input devices
                if (filter is None or filter in name) and ins > 0:
                    devices.append((int(inlat*1000), device, name[:25], rate))
                    #print(f'{device}: {name} - {rate/1000:.1f}kHz - {inlat*1000:.0f}ms')
            else:   # output devices
                if (filter is None or filter in name) and outs > 0:
                    devices.append((int(outlat*1000), device, name[:25], rate))
                    #print(f'{device}: {name} - {rate/1000:.1f}kHz - {outlat*1000:.0f}ms')
        devices.sort()
        return devices


    # ----------------------------------------------------------------------------------------------


    def callback(self, in_data, frame_count, time_info, status):
        data = None
        if self.metronome.click_flag:
            if self.metronome.click_pos < (self.metronome.click_frames_n[self.metronome.click_index] - frame_count):
                data = self.metronome.click_data[self.metronome.click_index][
                    self.metronome.click_pos:self.metronome.click_pos + frame_count
                ]
                self.metronome.click_pos += frame_count
            else:
                data = np.pad(
                    self.metronome.click_data[self.metronome.click_index][self.metronome.click_pos:],
                    [0, frame_count - (self.metronome.click_frames_n[self.metronome.click_index] - self.metronome.click_pos)]
                )
                self.metronome.click_flag = False
                self.metronome.click_pos = 0

        return (data,pyaudio.paContinue)


    def set_metronome(self,metronome):
        self.metronome = metronome


    def start_stream(self):
        self.stream.start_stream()


    def is_active(self):
        return self.stream.is_active()


    def play_click(self):
        try:
            self.stream.stop_stream()
            self.stream.close()
        except:
            pass
        self.stream = self.audioinstance.open(
            format=pyaudio.paInt16,
            channels=1,
            output_device_index=self.device_out,
            rate=self.sampling_rate,
            output = True,
            stream_callback = self.callback
        )
        self.stream.start_stream()


    def __init__(self, device_out=None):
        self.audioinstance = pyaudio.PyAudio()

        if device_out == None: # or device_in == None
            return

        self.device_out = device_out
        self.sampling_rate = int(
            self.audioinstance.get_device_info_by_index(self.device_out)['defaultSampleRate']
        )


    def uninit(self):
        try:
            # stop stream 
            self.stream.stop_stream()
            self.stream.close()
        except:
            pass
        
        # close PyAudio 
        self.audioinstance.terminate()

