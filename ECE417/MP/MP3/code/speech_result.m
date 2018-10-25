%% test for speech_accuracy
speech_accuracy_raw=zeros(6,5);
for i=1:4
    speech_accuracy_raw(:,i)=test_speech(Raw_feature,i,K);
end
speech_accuracy_raw(:,5)=mean(speech_accuracy_raw(:,1:4),2);



%% get ceptrum of each signal
speech_accuracy_cep_100=zeros(6,5);
for i=1:4
    speech_accuracy_cep_100(:,i)=test_speech(description_mat_cep_100,i,K);
end
speech_accuracy_cep_100(:,5)=mean(speech_accuracy_cep_100(:,1:4),2);


%% get ceptrum of each signal

speech_accuracy_cep_500=zeros(6,5);
for i=1:4
    speech_accuracy_cep_500(:,i)=test_speech(description_mat_cep_500,i,K);
end
speech_accuracy_cep_500(:,5)=mean(speech_accuracy_cep_500(:,1:4),2);

%% get ceptrum of each signal
speech_accuracy_cep_10000=zeros(6,5);
for i=1:4
    speech_accuracy_cep_10000(:,i)=test_speech(description_mat_cep_10000,i,K);
end
speech_accuracy_cep_10000(:,5)=mean(speech_accuracy_cep_10000(:,1:4),2);


%% get ceptrum of each signal
speech_accuracy_mfcc_100=zeros(6,5);
for i=1:4
    speech_accuracy_mfcc_100(:,i)=test_speech(description_mat_mfcc_100,i,K);
end
speech_accuracy_mfcc_100(:,5)=mean(speech_accuracy_mfcc_100(:,1:4),2);

%% get ceptrum of each signal
speech_accuracy_mfcc_500=zeros(6,5);
for i=1:4
    speech_accuracy_mfcc_500(:,i)=test_speech(description_mat_mfcc_500,i,K);
end
speech_accuracy_mfcc_500(:,5)=mean(speech_accuracy_mfcc_500(:,1:4),2);

%% get ceptrum of each signal
speech_accuracy_mfcc_10000=zeros(6,5);
for i=1:4
    speech_accuracy_mfcc_10000(:,i)=test_speech(description_mat_mfcc_10000,i,K);
end
speech_accuracy_mfcc_10000(:,5)=mean(speech_accuracy_mfcc_10000(:,1:4),2);