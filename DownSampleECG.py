import numpy as np
import math
import matplotlib.pyplot as plt



class DownSampleECG:
    def __init__(self, ECG, current_sampling_rate, resampling_rate):
        self.ECG = ECG # 2D shape (Voltages, Channels)
        self.current_sampling_rate = current_sampling_rate
        self.resampling_rate = resampling_rate
    def get_downsampled_ECG(self):
        sec = int(self.ECG.shape[0] / self.current_sampling_rate)
        rate = self.current_sampling_rate/self.resampling_rate 
        
        values = np.empty([self.resampling_rate*sec, self.ECG.shape[1]])
        for channel in range(self.ECG.shape[1]):
            dicts = {}
            keys = range(self.ECG.shape[0])
            for i in keys:
                dicts[i] = self.ECG[:,channel][i]
            if self.current_sampling_rate % self.resampling_rate == 0:
                values[:,channel] = list( map(dicts.get, np.arange(0,len(self.ECG), int(rate))))
            else: #here
                key_up = np.arange(0,len(self.ECG), rate)                  
                                   
                resampled = {}

                for i in key_up:
                    if i % 1 == 0:
                        resampled[i] = dicts[int(i)]
                    else:
                        floor = math.floor(i)
                        ceil = math.ceil(i)
                        
                        m = (dicts[ceil] - dicts[floor]) / (ceil-floor) # Get Slope of the line
                        resampled[i] = m*(i-floor) + dicts[floor] # get y value at location i. (interpolated value)

                values[:,channel] = list(resampled.values())
        return values
                                   
                                   
    def Plot_ECGs(self, figure_size = (25,7), save=False, fig_name = "EX.tiff", channel=0):
        import matplotlib.pyplot as plt
        downsampled = self.get_downsampled_ECG()
        original = self.ECG


        plt.figure(figsize=figure_size)


        ecg = downsampled[:,channel]
        frequency = self.resampling_rate

        # calculating time data with ecg size along with frequency
        time_data = np.arange(len(ecg)) / frequency

        # plotting time and ecg 
        plt.plot(time_data, ecg, color="red", label="Resampled at " + str(frequency) + ' Hz')



        ecg2 = original[:,channel]
        frequency2 = self.current_sampling_rate

        # calculating time data with ecg size along with frequency
        time_data2 = np.arange(len(ecg2)) / frequency2

        # plotting time and ecg model
        plt.plot(time_data2, ecg2, color="blue", label="Original at "+str(frequency2) + ' Hz')


        plt.xlabel("Channel(or Lead) "+channel+ " of an example ECG")
        plt.legend(loc='upper center')
        #plt.axis('off')
        # display
        #
        if save == True:                       
            plt.savefig(fig_name, bbox_inches='tight', dpi = 300)
        plt.show()

