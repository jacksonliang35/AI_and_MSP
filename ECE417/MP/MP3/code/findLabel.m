function label = findLabel(idx,k,mode)
% Find Label from given sorted index list
% Speech: {1,2,3,4,5}
% Speaker: {1,2,3,4} representing {A,B,C,D}
if k > length(idx)
    k = length(idx);
end

if strcmp(mode,'speech')
    lablist = mod(ceil(idx(1:k)./5)-1,5)+1;
    occur=zeros(5,1);
    for i=1:5
        occur(i)=length(lablist(lablist==i));
    end
    [sorted_occur,idlist] = sort(occur,'descend');
    if sorted_occur(2)==sorted_occur(1) && k < length(idx)
        label = findLabel(idx,k+1,mode);
    else
        label = idlist(1);
    end
else
    % Speaker
    lablist = ceil(idx(1:k)./20);
    occur=zeros(4,1);
    for i=1:4
        occur(i)=length(lablist(lablist==i));
    end
    [sorted_occur,idlist] = sort(occur,'descend');
    if sorted_occur(2)==sorted_occur(1) && k < length(idx)
        label = findLabel(idx,k+1,mode);
    else
        label = idlist(1);
    end
end
end

