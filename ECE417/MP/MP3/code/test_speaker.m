function [accuracy]=test_speaker(data,digit,K)
mode='speaker';
accuracy=zeros(5,1);
train_data=data;
for i=1:4 % speaker {A,B,C,D}
    for j=1:5 % case {a,b,c,d,e}
       idx=(i-1)*25+(digit-1)*5+j;
       test_data=data(:,idx);
       label=knn(train_data,test_data,K,mode);
       if(label==i)
           accuracy(i)=accuracy(i)+1;
       end
    end
end
accuracy(end)=sum(accuracy(1:4)).*100./20;
accuracy(1:4)=accuracy(1:4).*100./5;


end

