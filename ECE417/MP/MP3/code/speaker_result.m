%% test for speaker_accuracy
speaker_accuracy_raw=zeros(5,6);
for i=1:5
    speaker_accuracy_raw(:,i)=test_speaker(Raw_feature,i,K);
end
speaker_accuracy_raw(:,6)=mean(speaker_accuracy_raw(:,1:5),2);



%% get ceptrum of each signal
speaker_accuracy_cep_100=zeros(5,6);
for i=1:5
    speaker_accuracy_cep_100(:,i)=test_speaker(description_mat_cep_100,i,K);
end
speaker_accuracy_cep_100(:,6)=mean(speaker_accuracy_cep_100(:,1:5),2);


%% get ceptrum of each signal

speaker_accuracy_cep_500=zeros(5,6);
for i=1:5
    speaker_accuracy_cep_500(:,i)=test_speaker(description_mat_cep_500,i,K);
end
speaker_accuracy_cep_500(:,6)=mean(speaker_accuracy_cep_500(:,1:5),2);

%% get ceptrum of each signal
speaker_accuracy_cep_10000=zeros(5,6);
for i=1:5
    speaker_accuracy_cep_10000(:,i)=test_speaker(description_mat_cep_10000,i,K);
end
speaker_accuracy_cep_10000(:,6)=mean(speaker_accuracy_cep_10000(:,1:5),2);


%% get ceptrum of each signal
speaker_accuracy_mfcc_100=zeros(5,6);
for i=1:5
    speaker_accuracy_mfcc_100(:,i)=test_speaker(description_mat_mfcc_100,i,K);
end
speaker_accuracy_mfcc_100(:,6)=mean(speaker_accuracy_mfcc_100(:,1:5),2);

%% get ceptrum of each signal
speaker_accuracy_mfcc_500=zeros(5,6);
for i=1:5
    speaker_accuracy_mfcc_500(:,i)=test_speaker(description_mat_mfcc_500,i,K);
end
speaker_accuracy_mfcc_500(:,6)=mean(speaker_accuracy_mfcc_500(:,1:5),2);

%% get ceptrum of each signal
speaker_accuracy_mfcc_10000=zeros(5,6);
for i=1:5
    speaker_accuracy_mfcc_10000(:,i)=test_speaker(description_mat_mfcc_10000,i,K);
end
speaker_accuracy_mfcc_10000(:,6)=mean(speaker_accuracy_mfcc_10000(:,1:5),2);