function [time, rawSignal, respirationTransient, heartRateTransient, respRate, heartRate ] = SignalProcessorPeakFinding(fileName)

%% Configuration Details
cutoffFreq = 5;          %Highest Frequency to display (Hz)
fPassResp = .2;          %Beginning of passband for respiration rate (Hz)
fStopResp = .9;          %End of passpand for respiration rate (Hz)
fPassHeart = 1;          %Beginning of passband for heart rate (Hz)
fStopHeart = 2;          %End of passband for heart rate (Hz)
fRespWidth = .2;         %Width of respiration fdesign.bandpass filter
fHeartWidth = .5;        %Width of heartrate fdesign.bandpass filter
respFilterOrder = 8;     %Order of respiration bandpass filter
heartFilterOrder = 8;    %Order of heart rate bandpass filter

%% Read in raw data and save as time, I, and Q channels
rawData = xlsread(fileName);
time = rawData(:,1);
rawSignal = rawData(:,2);
Fs = 1/(time(2) - time(1));   %Sampling Frequency
L = length(rawSignal);   %Length of signals
NFFT = 2^nextpow2(L);   %Length of FFT
fNorm = Fs/2;           %normalized frequency for filter design

%% Eliminate Linear Shift in Data
rawSignal = detrend(rawSignal);

%% Take one sided FFT
fftSig = fft(rawSignal,NFFT)/L;        %FFT of signal
f = fNorm*linspace(0,1,NFFT/2+1);            %Frequency Range
oneSidedDFT = 2*abs(fftSig(1:NFFT/2+1));

%% Only display frequencies greater than the cutoff frequency
maskCutoff = f>cutoffFreq;
f(maskCutoff) = [];
oneSidedDFT(maskCutoff) = [];

%% Bandpass filter for respiration rate
respMask = f>fPassResp & f<fStopResp;
respDFT = oneSidedDFT;
respDFT(~respMask) = 0;

%% Determine Respiration Rate
[maxResp , respLoc] = max(respDFT);
respirationRate = f(respLoc);

%% Determine Heartrate using combined channel
[hrVal] = SignalProcessorPeakFinding(oneSidedDFT, f, .25, .1); 
heartRate = hrValCombined(1);

%% Use fdesign to filter out respiration rate transient
respBandpassDesign = fdesign.bandpass('N,F3dB1,F3dB2',...
    respFilterOrder,(respirationRate - fRespWidth)/fNorm, (respirationRate + fRespWidth)/fNorm);
respBandpass = design(respBandpassDesign);
combinedChannelRespFDesign = filter(respBandpass,rawSignal);

%% Use fdesign to filter out heart rate transient
heartBandpassDesign = fdesign.bandpass('N,F3dB1,F3dB2',...
    heartFilterOrder,(heartRate - fHeartWidth)/fNorm, (heartRate + fHeartWidth)/fNorm);
heartBandpass = design(heartBandpassDesign);
combinedChannelHeartFDesign = filter(heartBandpass,rawSignal);

%% Plot raw signals
figure
plot(time,abs(rawSignal))
xlabel('Time (s)')
ylabel('|c(t)|')
title('Combined Signals in Time Domain')

%% Plot one sided FFTs
figure
plot(f,oneSidedDFT) 
title('Single-Sided Amplitude Spectrum of Combined channels FFT')
xlabel('Frequency (Hz)')
ylabel('|C(f)|')

%% Plot respiration transients
figure
plot(time,abs(combinedChannelRespFDesign)) 
title('Combined Channel Respiration Rate Transient')
xlabel('Time (s)')
ylabel('c(t)')

%% Plot heart rate transients
figure
plot(time,abs(combinedChannelHeartFDesign)) 
title('Combined Channel Heart Rate Transient')
xlabel('Time (s)')
ylabel('c(t)')

%% Print out heart and respiration rates
endMessage1 = ['Heart Rate is ' num2str(heartRate) ...
    ' beats per second'];
endMessage2 = ['Respiration Rate is ' num2str(respirationRate) ...
    ' breaths per second'];
disp(endMessage1);
disp(endMessage2);


end