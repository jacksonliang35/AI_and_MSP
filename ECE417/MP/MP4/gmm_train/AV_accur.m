function accuracy=AV_accur(AV_data,likelihood,posterior,w)
accuracy=zeros(5,1);
%% A
A_fuse=zeros(4,100);
for i=1:100
    %temp=exp(likelihood(:,AV_data.A(i,1)))./sum(exp(likelihood(:,AV_data.A(i,1))));
    A_fuse(:,i)=(exp(likelihood(:,AV_data.A(i,1))).^w).*(posterior(:,AV_data.A(i,2)).^(1-w));
    [~,idx]=max(A_fuse(:,i));
    if(idx==1)
        accuracy(1,1)=accuracy(1,1)+1;
    end
end

B_fuse=zeros(4,100);
for i=1:100
    B_fuse(:,i)=(exp(likelihood(:,AV_data.B(i,1))).^w).*(posterior(:,AV_data.B(i,2)).^(1-w));
    [~,idx]=max(B_fuse(:,i));
    if(idx==2)
        accuracy(2,1)=accuracy(2,1)+1;
    end
end

C_fuse=zeros(4,100);
for i=1:100
    C_fuse(:,i)=(exp(likelihood(:,AV_data.C(i,1))).^w).*(posterior(:,AV_data.C(i,2)).^(1-w));
    [~,idx]=max(C_fuse(:,i));
    if(idx==3)
        accuracy(3,1)=accuracy(3,1)+1;
    end
end

D_fuse=zeros(4,100);
for i=1:100
    D_fuse(:,i)=(exp(likelihood(:,AV_data.D(i,1))).^w).*(posterior(:,AV_data.D(i,2)).^(1-w));
    [~,idx]=max(D_fuse(:,i));
    if(idx==4)
        accuracy(4,1)=accuracy(4,1)+1;
    end
end
accuracy(end)=mean(accuracy(1:end-1));

end