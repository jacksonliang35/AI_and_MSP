testII=totalII(:,:,127:end);
testrects=totalrects(127:end,17:48);
[num_test,~]=size(testrects);
F=zeros(num_test,8,40);
single_classify=zeros(num_test,8,40);
scaled_classify=zeros(num_test,8,40);
Y_test = [ones(num_test,4),-ones(num_test,4)];
for t=1:40
    F(:,:,t) = rectfeature(testII,testrects,besth(t,1:4),besth(t,5),besth(t,6));
    alpha=-log(beta(t));
    single_classify(:,:,t)=besth(t,end).*sign(besth(t,end-1)-F(:,:,t));
    scaled_classify(:,:,t)=alpha.*single_classify(:,:,t);
    %class_label=class_label+alpha.*(2*(besth(t,8)*F<besth(t,8)*besth(t,7))-1);
end
final_classify=cumsum(scaled_classify,3);
totalerr=zeros(40,1);
singleerr=zeros(40,1);
for t=1:40
    totalerr(t)=mean(mean(sign(final_classify(:,:,t))~= Y_test));
    singleerr(t)=mean(mean(sign(single_classify(:,:,t))~= Y_test));
end