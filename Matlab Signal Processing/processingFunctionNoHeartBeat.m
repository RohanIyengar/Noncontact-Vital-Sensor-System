function [time, rawSignal, respirationTransient, heartRateTransient, respirationRate, heartRate ] = processingFunctionNoHeartBeat(fileName)

%% Configuration Details
cutoffFreq = 5;          %Highest Frequency to display (Hz)
fPassResp = .2;          %Beginning of passband for respiration rate (Hz)
fStopResp = .9;          %End of passpand for respiration rate (Hz)
fRespWidth = .2;         %Width of respiration fdesign.bandpass filter
respFilterOrder = 8;     %Order of respiration bandpass filter

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

%% Heartrate undetectable, set to zero by default
heartRate = 0;

%% Use fdesign to filter out respiration rate transient
respBandpassDesign = fdesign.bandpass('N,F3dB1,F3dB2',...
    respFilterOrder,(respirationRate - fRespWidth)/fNorm, (respirationRate + fRespWidth)/fNorm);
respBandpass = design(respBandpassDesign);
respirationTransient = filter(respBandpass,rawSignal);

%% Set heartrate transient to all zeros
heartRateTransient = zeros(1,length(respirationTransient));

end