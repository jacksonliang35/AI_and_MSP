function [Probability,label] = knn(F,data,k)
%knn k-nearest-neighbor classification w/ 80 training samples into 4 categories
%   F Feature matrix, where each column is a feature
%   data The data to be labelled
%   k   The number of neighbors to be examined
%   label   Some number in {1,2,3,4} which represent A,B,C,D
dsqr = sum((F-repmat(data,1,40)).^2); % distance squared
[~,idx] = sort(dsqr,'ascend');
if data==F(:,idx(1))
    [Probability,label] = findLabel(idx(2:end),k);
else
    [Probability,label] = findLabel(idx,k);
end
end

