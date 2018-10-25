
%% get ceptrum of each signal
[~,num_data]=size(Raw_feature);
Ncc=12;
Nw=100;
No=floor(0.1*Nw);
len = length(Raw_feature(:,1));
Nf  = floor( (len - No)/(Nw - No) );
description_mat_cep_100=zeros(Nf*Ncc,num_data);

for i=1:num_data
    description_mat_cep_100(:,i)=cepstrum(Raw_feature(:,i),Ncc, Nw, No);
end

%% get ceptrum of each signal
[~,num_data]=size(Raw_feature);
Ncc=12;
Nw=500;
No=floor(0.1*Nw);
len = length(Raw_feature(:,1));
Nf  = floor( (len - No)/(Nw - No) );
description_mat_cep_500=zeros(Nf*Ncc,num_data);

for i=1:num_data
    description_mat_cep_500(:,i)=cepstrum(Raw_feature(:,i),Ncc, Nw, No);
end

%% get ceptrum of each signal
[~,num_data]=size(Raw_feature);
Ncc=12;
Nw=10000;
No=floor(0.1*Nw);
len = length(Raw_feature(:,1));
Nf  = floor( (len - No)/(Nw - No) );
description_mat_cep_10000=zeros(Nf*Ncc,num_data);

for i=1:num_data
    description_mat_cep_10000(:,i)=cepstrum(Raw_feature(:,i),Ncc, Nw, No);
end

%% get ceptrum of each signal
[~,num_data]=size(Raw_feature);
Ncc=12;
Nw=100;
No=floor(0.1*Nw);
len = length(Raw_feature(:,1));
Nf  = floor( (len - No)/(Nw - No) );
description_mat_mfcc_100=zeros(Nf*Ncc,num_data);
for i=1:num_data
    description_mat_mfcc_100(:,i)=mfcc(Raw_feature(:,i),Ncc, 'Nw', Nw, 'No', No, 'Fs', fs, 'M', 26, 'R',  [0 fs/2], 'alpha', 0.97);
end


%% get ceptrum of each signal
[~,num_data]=size(Raw_feature);
Ncc=12;
Nw=500;
No=floor(0.1*Nw);
len = length(Raw_feature(:,1));
Nf  = floor( (len - No)/(Nw - No) );
description_mat_mfcc_500=zeros(Nf*Ncc,num_data);
for i=1:num_data
    description_mat_mfcc_500(:,i)=mfcc(Raw_feature(:,i),Ncc, 'Nw', Nw, 'No', No, 'Fs', fs, 'M', 26, 'R',  [0 fs/2], 'alpha', 0.97);
end


%% get ceptrum of each signal
[~,num_data]=size(Raw_feature);
Ncc=12;
Nw=10000;
No=floor(0.1*Nw);
len = length(Raw_feature(:,1));
Nf  = floor( (len - No)/(Nw - No) );
description_mat_mfcc_10000=zeros(Nf*Ncc,num_data);
for i=1:num_data
    description_mat_mfcc_10000(:,i)=mfcc(Raw_feature(:,i),Ncc, 'Nw', Nw, 'No', No, 'Fs', fs, 'M', 26, 'R',  [0 fs/2], 'alpha', 0.97);
end
