clear variables
close all

%% Configuration Details
fileNum = 3;      %2-5
numSecondsBeginning = 5; %Number of seconds to eliminate from beginning of signal
numSecondsEnd = 5;       %Number of seconds to eliminate from end of signal
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
fileName = ['tek000' num2str(fileNum) 'ALL.csv'];
rawData = csvread(fileName,21);
t = rawData(:,1);
iChannel = rawData(:,3);
qChannel = rawData(:,4);
combinedChannel = iChannel + 1j.*qChannel;
Fs = 1/(t(2) - t(1));   %Sampling Frequency
L = length(iChannel);   %Length of signals
NFFT = 2^nextpow2(L);   %Length of FFT
fNorm = Fs/2;           %normalized frequency for filter design


%% Eliminate numSecondsBeginning of bad data at beginning
numSamplesBeginning = round(numSecondsBeginning*Fs);
t(1:numSamplesBeginning) = [];
iChannel(1:numSamplesBeginning) = [];
qChannel(1:numSamplesBeginning) = [];
combinedChannel(1:numSamplesBeginning) = [];

%% Eliminate numSecondsEnd of bad data at end
numSamplesEnd = round(numSecondsEnd*Fs);
t(end:-1:(end-numSamplesEnd)) = [];
iChannel(end:-1:(end-numSamplesEnd)) = [];
qChannel(end:-1:(end-numSamplesEnd)) = [];
combinedChannel(end:-1:(end-numSamplesEnd)) = [];

%% Eliminate Linear Shift in Data
iChannel = detrend(iChannel);
qChannel = detrend(qChannel);
combinedChannel = detrend(combinedChannel);

%% Take one sided FFT
fftI = fft(iChannel,NFFT)/L;                %FFT of I channel
fftQ = fft(qChannel,NFFT)/L;                %FFT of Q channel
fftCombined = fft(combinedChannel,NFFT)/L;  %FFT of Q channel
f = Fs/2*linspace(0,1,NFFT/2+1);            %Frequency Range
oneSidedIDFT = 2*abs(fftI(1:NFFT/2+1));
oneSidedQDFT = 2*abs(fftQ(1:NFFT/2+1));
oneSidedCombinedDFT = 2*abs(fftCombined(1:NFFT/2+1));

%% Only display frequencies greater than the cutoff frequency
maskCutoff = f>cutoffFreq;
f(maskCutoff) = [];
oneSidedIDFT(maskCutoff) = [];
oneSidedQDFT(maskCutoff) = [];
oneSidedCombinedDFT(maskCutoff) = [];

%% Bandpass filter for respiration rate
respMask = f>fPassResp & f<fStopResp;
iChannelRespDFT = oneSidedIDFT;
qChannelRespDFT = oneSidedQDFT;
combinedRespDFT = oneSidedCombinedDFT;
iChannelRespDFT(~respMask) = 0;
qChannelRespDFT(~respMask) = 0;
combinedRespDFT(~respMask) = 0;

%% Determine Respiration Rate
[maxIResp , iRespLoc] = max(iChannelRespDFT);
[maxQResp , qRespLoc] = max(qChannelRespDFT);
[maxCombinedResp , combinedRespLoc] = max(combinedRespDFT);

respirationRate = f(combinedRespLoc);
respChoice = 'Combined Channel';

if(maxIResp > maxQResp && maxIResp > maxCombinedResp)
    respirationRate = f(iRespLoc);
    respChoice = 'I channel';
end
if(maxQResp > maxIResp && maxQResp > maxCombinedResp)
    respirationRate = f(qRespLoc);
    respChoice = 'Q channel';
end

%% Determine Heartrate using combined channel
[hrValCombined] = SignalProcessorPeakFinding(oneSidedCombinedDFT, f, .25, .1); 
heartRate = hrValCombined(1);
heartChoice = 'combined channels';

%% Use fdesign to filter out respiration rate transient
respBandpassDesign = fdesign.bandpass('N,F3dB1,F3dB2',...
    respFilterOrder,(respirationRate - fRespWidth)/fNorm, (respirationRate + fRespWidth)/fNorm);
respBandpass = design(respBandpassDesign);
iChannelRespFDesign = filter(respBandpass,iChannel);
qChannelRespFDesign = filter(respBandpass,qChannel);
combinedChannelRespFDesign = filter(respBandpass,combinedChannel);

%% Use fdesign to filter out heart rate transient
heartBandpassDesign = fdesign.bandpass('N,F3dB1,F3dB2',...
    heartFilterOrder,(heartRate - fHeartWidth)/fNorm, (heartRate + fHeartWidth)/fNorm);
heartBandpass = design(heartBandpassDesign);
iChannelHeartFDesign = filter(heartBandpass,iChannel);
qChannelHeartFDesign = filter(heartBandpass,qChannel);
combinedChannelHeartFDesign = filter(heartBandpass,combinedChannel);

%% Plot raw signals
figure
subplot(3,1,1)
plot(t,iChannel)
xlabel('Time (s)')
ylabel('|i(t)|')
title('I Channel in Time Domain')
subplot(3,1,2)
plot(t,qChannel)
xlabel('Time (s)')
ylabel('|q(t)|')
title('Q Channel in Time Domain')
subplot(3,1,3)
plot(t,abs(combinedChannel))
xlabel('Time (s)')
ylabel('|c(t)|')
title('Combined Signals in Time Domain')

%% Plot one sided FFTs
figure
subplot(3,1,1)
plot(f,oneSidedIDFT) 
title('Single-Sided Amplitude Spectrum of I channel FFT')
xlabel('Frequency (Hz)')
ylabel('|I(f)|')
subplot(3,1,2)
plot(f,oneSidedQDFT) 
title('Single-Sided Amplitude Spectrum of Q channel FFT')
xlabel('Frequency (Hz)')
ylabel('|Q(f)|')
subplot(3,1,3)
plot(f,oneSidedCombinedDFT) 
title('Single-Sided Amplitude Spectrum of Combined channels FFT')
xlabel('Frequency (Hz)')
ylabel('|C(f)|')

%% Plot respiration transients
figure
subplot(3,1,1)
plot(t,iChannelRespFDesign) 
title('I Channel Respiration Rate Transient')
xlabel('Time (s)')
ylabel('i(t)')
subplot(3,1,2)
plot(t,qChannelRespFDesign) 
title('Q Channel Respiration Rate Transient')
xlabel('Time (s)')
ylabel('q(t)')
subplot(3,1,3)
plot(t,real(combinedChannelRespFDesign)) 
title('Combined Channel Respiration Rate Transient')
xlabel('Time (s)')
ylabel('c(t)')

%% Plot heart rate transients
figure
subplot(3,1,1)
plot(t,iChannelHeartFDesign) 
title('I Channel Heart Rate Transient')
xlabel('Time (s)')
ylabel('i(t)')
subplot(3,1,2)
plot(t,qChannelHeartFDesign) 
title('Q Channel Heart Rate Transient')
xlabel('Time (s)')
ylabel('q(t)')
subplot(3,1,3)
plot(t,real(combinedChannelHeartFDesign)) 
title('Combined Channel Heart Rate Transient')
xlabel('Time (s)')
ylabel('c(t)')

%% Print out heart and respiration rates
endMessage1 = ['Heart Rate is ' num2str(heartRate) ...
    ' beats per second using the ' heartChoice];
endMessage2 = ['Respiration Rate is ' num2str(respirationRate) ...
    ' breaths per second using the ' respChoice];
disp(endMessage1);
disp(endMessage2);

