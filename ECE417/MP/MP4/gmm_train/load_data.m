function [aud_train_data,aud_test_data,img_train_data,img_test_data,AV_data]=load_data(datadir,T,Ncc,Nw,energy)

if(~strcmp(datadir(end),'/'))
    datadir=[datadir,'/'];
end

img_train_dir=[datadir,'trainimg/'];
aud_train_dir=[datadir,'trainspeech/'];
img_test_dir=[datadir,'testimg/'];
aud_test_dir=[datadir,'testspeech/'];

No=floor(0.1*Nw);
Nf  = floor( (T - No)/(Nw - No) );

%% load audio train data 15 audio files/person 4 persons
aud_train_raw=zeros(T,60);
aud_train_cep=zeros(Ncc,Nf,60);
aud_train_filename=cell(60,1);
for i=1:4
    for j=1:15
        address=[aud_train_dir,char('A'+i-1),int2str(j),'.wav'];
        temp=audioread(address);
        temp=imresize(temp(:,1),[T,1]);
        aud_train_raw(:,(i-1)*15+j)=temp;
        aud_train_cep(:,:,(i-1)*15+j)=cepstrum(temp,Ncc, Nw, No);
        aud_train_filename((i-1)*15+j)={address};
    end
end

aud_train_data.raw=aud_train_raw;
aud_train_data.cep=aud_train_cep;
aud_train_data.filename=aud_train_filename;


%% load audio test data 10 audio files/person 4 persons
aud_test_raw=zeros(T,40);
aud_test_cep=zeros(Ncc,Nf,40);
aud_test_filename=cell(40,1);
for i=1:4
    for j=1:10
        address=[aud_test_dir,char('A'+i-1),int2str(j),'.wav'];
        temp=audioread(address);
        temp=imresize(temp(:,1),[T,1]);
        aud_test_raw(:,(i-1)*10+j)=temp;
        aud_test_cep(:,:,(i-1)*10+j)=cepstrum(temp,Ncc, Nw, No);
        aud_test_filename((i-1)*10+j)={address};
    end
end

aud_test_data.raw=aud_test_raw;
aud_test_data.cep=aud_test_cep;
aud_test_data.filename=aud_test_filename;

%% load img train data
img_train_raw=zeros(70*90,40);
img_train_filename=cell(40,1);
for i=1:4
    for j=1:10
        address=[img_train_dir,char('A'+i-1),int2str(j),'.jpg'];
        temp=im2double(rgb2gray(imread(address)));
        temp=reshape(temp,[6300,1]);
        img_train_raw(:,(i-1)*10+j)=temp;
        img_train_filename((i-1)*10+j)={address};
    end
end
%[img_train_PCA,img_train_eigVal]=calc_PCA(img_train_raw,energy);

img_train_data.raw=img_train_raw;
%img_train_data.PCA=img_train_PCA;
%img_train_data.eigV=img_train_eigVal;
img_train_data.filename=img_train_filename;


%% load img test data
img_test_raw=zeros(70*90,40);
img_test_filename=cell(40,1);
for i=1:4
    for j=1:10
        address=[img_test_dir,char('A'+i-1),int2str(j+10),'.jpg'];
        temp=im2double(rgb2gray(imread(address)));
        temp=reshape(temp,[6300,1]);
        img_test_raw(:,(i-1)*10+j)=temp;
        img_test_filename((i-1)*10+j)={address};
    end
end
[img_PCA,~]=calc_PCA([img_train_raw,img_test_raw],energy);
%[img_test_PCA,img_test_eigVal]=calc_PCA(img_test_raw,energy);


img_train_data.PCA=img_PCA(:,1:40);
img_test_data.PCA=img_PCA(:,41:80);


img_test_data.raw=img_test_raw;
img_test_data.filename=img_test_filename;

%% Audio-Visual data idx
%% first column: idx in aud_test_data, second column idx in img_test_data
AV_data.A=[sort(repmat((1:10)',[10,1])),repmat((1:10)',[10,1])];
AV_data.B=[sort(repmat((11:20)',[10,1])),repmat((11:20)',[10,1])];
AV_data.C=[sort(repmat((21:30)',[10,1])),repmat((21:30)',[10,1])];
AV_data.D=[sort(repmat((31:40)',[10,1])),repmat((31:40)',[10,1])];



end