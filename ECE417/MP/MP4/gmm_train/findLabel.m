function [Probability,label] = findLabel(idx,k)
% Find Label from given sorted index list
if k > length(idx)
    k = length(idx);
end
lablist = ceil(idx(1:k)./10);
occur=zeros(4,1);
for i=1:4
    occur(i)=length(lablist(lablist==i));
end
Probability=occur./k;
[sorted_occur,idlist] = sort(occur,'descend');
label = idlist(1);
%{
if sorted_occur(2)==sorted_occur(1)
    [~,label] = findLabel(idx,k+1);
else
    label = idlist(1);
end
%}
end

