function label = knn(F,x,k,mode)
%knn k-nearest-neighbor classification
%   F Feature matrix, Nr*100, where each column is a feature
%   x The data to be labelled
%   k   The number of neighbors to be compared
%   mode    'speech' or 'speaker'
%   label   speech: some in {1,2,3,4,5}
%           speaker: some in {1,2,3,4} representing {A,B,C,D}
assert(strcmp(mode,'speech')||strcmp(mode,'speaker'));

% Find the corresponding index of x in F
ind = find(all(F==x,1)==1);
assert(~isempty(ind));

if strcmp(mode,'speech')
    G = [F(:,1:floor((ind-1)/25)*25),F(:,ceil((ind)/25)*25+1:100)];   % G is Nr*75
    dsqr = sum((G-repmat(x,1,75)).^2); % distance squared
    [~,idx] = sort(dsqr,'ascend');
    label = findLabel(idx,k,mode);
else
    % Speaker
    digit = mod(ceil(ind/5)-1,5)+1;
    G = zeros(length(x),80); % G is Nr*80
    idx_list=zeros(1,80);
    for i = 0:3
        idx_list(:,20*i+1:20*(i+1))=[i*25+1:i*25+(digit-1)*5,i*25+digit*5+1:25*(i+1)];
        G(:,20*i+1:20*(i+1)) = [F(:,i*25+1:i*25+(digit-1)*5),F(:,i*25+digit*5+1:25*(i+1))];
    end
    dsqr = sum((G-repmat(x,1,80)).^2); % distance squared
    [~,idx] = sort(dsqr,'ascend');
    label = findLabel(idx,k,mode);
end
end

%% speech test


