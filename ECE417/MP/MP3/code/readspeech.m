function [X,fs,filename] = readspeech(path,T)
%readspeech Read the given 100 speech files from the selected path
%   Read the speech from the given path and interpolate it into a matrix
%   path The path to read the audio files
X = zeros(10000,100);
filename=cell(100,1);
for i = 1:4
    for j = 1:5
        for k = 1:5
            [x,fs] = audioread([path,char(i+'A'-1),int2str(j),char(k+'a'-1),'.wav']);   % fs is the same for every file
            filename((i-1)*25+(j-1)*5+k)={[char(i+'A'-1),int2str(j),char(k+'a'-1),'.wav']};
            %X(:,(i-1)*25+(j-1)*5+k) = interp1(x(:,1),linspace(1,length(x(:,1)),10000));
            X(:,(i-1)*25+(j-1)*5+k)=imresize(x(:,1),[T,1]);
        end
    end
end

end

