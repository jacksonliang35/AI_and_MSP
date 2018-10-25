
%datadir='/Users/zhangzixu/Google Drive/ECE 417/MP5/AV_DATA';
datadir='E:/Google Drive/ECE 417/MP5/AV_DATA';

%% load data
[Audio_data,Visual_data,AV_data]=loaddata(datadir); 
% eg: to get 2.4.a.fea, use Audio_data{1,4};
%% GMM Train
A_init=[0.8,  0.2,  0,  0,  0;...
        0,  0.8,  0.2,  0,  0;...
        0,  0,  0.8,  0.2,  0;...
        0,  0,  0,  0.8,  0.2;
        0,  0,  0,  0,  1];
N=5;
%%

[P0_a2,A_a2,mu_a2,sigma_a2] = ghmm_learn(Audio_data(1,:),N,A_init);
[P0_a5,A_a5,mu_a5,sigma_a5] = ghmm_learn(Audio_data(2,:),N,A_init);

[P0_v2,A_v2,mu_v2,sigma_v2] = ghmm_learn(Visual_data(1,:),N,A_init);
[P0_v5,A_v5,mu_v5,sigma_v5] = ghmm_learn(Visual_data(2,:),N,A_init);

[P0_av2,A_av2,mu_av2,sigma_av2] = ghmm_learn(AV_data(1,:),N,A_init);
[P0_av5,A_av5,mu_av5,sigma_av5] = ghmm_learn(AV_data(2,:),N,A_init);


%% calculate likelihood
accurate_a2=0;`
train=Audio_data(1,:);
for i=1:10
    temp=get_L(train,i,P0_a5,A_a5,mu_a5,sigma_a5,N,A_init);
    accurate_a2=accurate_a2+temp;
end


accurate_a5=0;
train=Audio_data(2,:);
for i=1:10
    temp=get_L(train,i,P0_a2,A_a2,mu_a2,sigma_a2,N,A_init);
    accurate_a5=accurate_a5+temp;
end

accurate_v2=0;
train=Visual_data(1,:);
for i=1:10
    temp=get_L(train,i,P0_v5,A_v5,mu_v5,sigma_v5,N,A_init);
    accurate_v2=accurate_v2+temp;
end

accurate_v5=0;
train=Visual_data(2,:);
for i=1:10
    temp=get_L(train,i,P0_v2,A_v2,mu_v2,sigma_v2,N,A_init);
    accurate_v5=accurate_v5+temp;
end


accurate_av2=0;
train=AV_data(1,:);
for i=1:10
    temp=get_L(train,i,P0_av5,A_av5,mu_av5,sigma_av5,N,A_init);
    accurate_av2=accurate_av2+temp;
end

accurate_av5=0;
train=AV_data(2,:);
for i=1:10
    temp=get_L(train,i,P0_av2,A_av2,mu_av2,sigma_av2,N,A_init);
    accurate_av5=accurate_av5+temp;
end

%% print Accuracy
Acc=[accurate_a2*10,accurate_v2*10,accurate_av2*10;...
    accurate_a5*10,accurate_v5*10,accurate_av5*10];
Acc=[Acc;mean(Acc)];


acc_table=array2table(Acc, 'VariableNames', {'Audio', 'Visual', 'AV'}, 'RowNames', {'Digit 2','Digit 5', 'Avg'}) 
