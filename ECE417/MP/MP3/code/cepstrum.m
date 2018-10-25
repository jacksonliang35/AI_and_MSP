function CC = cepstrum(signal, Ncc, Nw, No)
% signal: speech signal (a vector)
% Nw: window size in samples
% No: overlap size in samples
% Ncc:  Number of cepstral coefficients
% CC = matrix of cepstral coeffs of size [Ncc x Nf], where Nf = num frames

% NFFT must meet the following conditions:
% a) NFFT is a number that is nearest to and >= Nw. 
% b) NFFT must also be a power of 2 (e.g. 2^1, 2^2, 2^3, 2^4 etc) 
NFFT = 2^nextpow2(Nw);%ceil(log2(Nw));   
alpha = 0.97;

% Preemphasis filtering
signal = filter([1 -alpha], 1, signal);

% Convert signal to frames
frames = sig2frames(signal, Nw, No);
[~, Nf] = size(frames); % Nf = number of frames
CC=zeros(NFFT,Nf);

% Compute real cepstrum from magnitude spectra = real part of inverse Fourier transform
% of the log magnitude spectrum
CC = real(ifft(log(abs(fft(frames,NFFT,1)))));
%{
for i=1:Nf
    %temp=imresize(frames(:,i),[NFFT,1]);
    CC(:,i) = real(ifft(log(abs(fft(frames(:,i),NFFT))))); % [NFFT x Nf]
end%test=rceps(frames(:,1));
%}
% Take only first Ncc coefficients since higher order coeffs are too small.
CC = CC(1:Ncc,:) ; % [Ncc x Nf]

CC=reshape(CC,Ncc*Nf,1);

end