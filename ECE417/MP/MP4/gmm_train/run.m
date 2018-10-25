%function [aud_table,img_table,av_table]=run(datadir)
function run(datadir)
%% load data
%datadir='/Users/zhangzixu/Google Drive/ECE 417/MP4';
%datadir='E:/Google Drive/ECE 417/MP4';
Ncc=12;
Nw=500;
T=10000;
PCA_energy=0.95;
[aud_train_data,aud_test_data,img_train_data,img_test_data,AV_data]=load_data(datadir,T,Ncc,Nw,PCA_energy);

%% audio train
M=2;
[~,Nf]=size(aud_train_data.cep(:,:,1));
cepsA=reshape(aud_train_data.cep(:,:,1:15),Ncc,Nf*15);
cepsB=reshape(aud_train_data.cep(:,:,16:30),Ncc,Nf*15);
cepsC=reshape(aud_train_data.cep(:,:,31:45),Ncc,Nf*15);
cepsD=reshape(aud_train_data.cep(:,:,46:60),Ncc,Nf*15);
aud_GMM(1) = gmm_train (cepsA', M);
aud_GMM(2) = gmm_train (cepsB', M);
aud_GMM(3) = gmm_train (cepsC', M);
aud_GMM(4) = gmm_train (cepsD', M);

%% test audio GMM
[aud_accuracy,likelihood_list]=audio_accuracy(aud_test_data,aud_GMM);
fprintf('\n--------- Person ID Accuracy: Audio -----------\n');
aud_table=array2table(aud_accuracy(:,2).*100,'RowNames', {'A','B','C', 'D', 'Avg'})
fprintf('--------------------\n'); 
%% visual test
posterior_pr=zeros(4,40);
img_accuracy=zeros(5,2);
for i=1:40
    [Probability,label]=knn(img_train_data.PCA,img_test_data.PCA(:,i),10);
    posterior_pr(:,i)=Probability;
    p=ceil(i/10);
    if(label==p)
       img_accuracy(p,1)= img_accuracy(p,1)+1;
    end 
end
    img_accuracy(end,1)=sum(img_accuracy(1:end-1,1));
    img_accuracy(1:end-1,2)=img_accuracy(1:end-1,1)./10;
    img_accuracy(end,end)=img_accuracy(end,1)./40;
    
fprintf('\n--------- Person ID Accuracy: Visual -----------\n');
img_table=array2table(img_accuracy(:,2).*100,'RowNames', {'A','B','C', 'D', 'Avg'})
fprintf('--------------------\n'); 
%% Audio-visual
AV_accuracy=zeros(5,9);
for i=1:9
    AV_accuracy(:,i)=AV_accur(AV_data,likelihood_list,posterior_pr,i/10);
end
fprintf('\n--------- Person ID Accuracy: Audio + Visual -----------\n');
av_table=array2table(AV_accuracy, 'VariableNames', {'w_01', 'w_02', 'w_03', 'w_04' , 'w_05', 'w_06', 'w_07', 'w_08', 'w_09'}, 'RowNames', {'A','B','C', 'D', 'Avg'})  
fprintf('--------------------\n'); 
end