function [hrVal] = SignalProcessorPeakFinding(inputFFT, f, threshold, leeWay) 
% Finds the spectral peaks due to the Heart Beat

%threshold = 0.25;
%leeWay = 0.1;
%f = f;

%% Plot of FFT
figure;
plot(f, inputFFT);

%% Isolating Freqs to be Tested
[~, respInd] = max(inputFFT);
respFreq = f(respInd);

lowMask = f>0.8;
highMask = f<1.6;
mask = lowMask & highMask;

fNew = f(mask);
testRange = inputFFT(mask);

%% Plotting Range of Data to be Tested
figure;
plot(fNew, testRange);

%% Setting a threshold and ordering Peaks
initVal = max(testRange);
thresVal = threshold.*initVal;

[pks, loc] = findpeaks(testRange, fNew);
[pksNew, pksInd] = sort(pks, 'descend');

%% Building Likely Heart Rate Values
hrVal = [];

for ind = 1:length(pksInd)
    
    pkInd = pksInd(ind);
    pk = pks(pkInd);
    pkLoc = loc(pkInd);
    
    if pk>=thresVal
        
        mult = pkLoc./respFreq;
        rem = abs(mult-round(mult));
        
        if (rem<=leeWay)
        
        else
            hrVal = [hrVal pkLoc];
        end
    end
end

hrEmpty = isempty(hrVal);
%Checking to see if all values are below threshold

if hrEmpty
    hrVal = initVal;
end

end
