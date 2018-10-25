function [accuracy]=test_speech(data,speaker,K)
mode='speech';
accuracy=zeros(6,1);
train_data=data;
for i=1:5
    for j=1:5
       idx=(speaker-1)*25+(i-1)*5+j;
       test_data=data(:,idx);
       label=knn(train_data,test_data,K,mode);
       if(label==i)
           accuracy(i)=accuracy(i)+1;
       end
    end
end
accuracy(end)=sum(accuracy(1:5))*100/25;
accuracy(1:5)=accuracy(1:5).*100./5;


end

