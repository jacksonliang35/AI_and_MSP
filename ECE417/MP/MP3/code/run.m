%% run this code as run('path to audio data')
function run(filepath)

%[Results_speech_ceptrum_1NN,Results_speech_mfcc_1NN,Results_Speaker_ceptrum_1NN,Results_Speaker_mfcc_1NN,...
    %Results_speech_ceptrum_5NN,Results_speech_mfcc_5NN,Results_Speaker_ceptrum_5NN,Results_Speaker_mfcc_5NN]=run(filepath)
if(strcmp(filepath(end),'/'))
    [Raw_feature,fs,filename] = readspeech(filepath,10000);   % X is 10000*100
else
     [Raw_feature,fs,filename] = readspeech([filepath,'/'],10000);   % X is 10000*100
end
    
   

get_description_matrix;

%% get result for 1NN
K=1;
speech_result;
speaker_result;

%% print out result
fprintf('Ceptrum\nSpeech Recognition\n%i-NN\n',K)
fprintf('    Raw  W=100  W=500  W=10000\n')
fprintf('D1: %.2i   %.2i     %.2i     %.2i\n',speech_accuracy_raw(1,end), speech_accuracy_cep_100(1,end), speech_accuracy_cep_500(1,end), speech_accuracy_cep_10000(1,end));
fprintf('D2: %.2i   %.2i     %.2i     %.2i\n',speech_accuracy_raw(2,end), speech_accuracy_cep_100(2,end), speech_accuracy_cep_500(2,end), speech_accuracy_cep_10000(2,end));
fprintf('D3: %.2i   %.2i     %.2i     %.2i\n',speech_accuracy_raw(3,end), speech_accuracy_cep_100(3,end), speech_accuracy_cep_500(3,end), speech_accuracy_cep_10000(3,end));
fprintf('D4: %.2i   %.2i     %.2i     %.2i\n',speech_accuracy_raw(4,end), speech_accuracy_cep_100(4,end), speech_accuracy_cep_500(4,end), speech_accuracy_cep_10000(4,end));
fprintf('D5: %.2i   %.2i     %.2i     %.2i\n',speech_accuracy_raw(5,end), speech_accuracy_cep_100(5,end), speech_accuracy_cep_500(5,end), speech_accuracy_cep_10000(5,end));
fprintf('Ave:%.2i   %.2i     %.2i     %.2i\n',speech_accuracy_raw(6,end), speech_accuracy_cep_100(6,end), speech_accuracy_cep_500(6,end), speech_accuracy_cep_10000(6,end));

Results_speech_ceptrum_1NN=[speech_accuracy_raw(1,end), speech_accuracy_cep_100(1,end), speech_accuracy_cep_500(1,end), speech_accuracy_cep_10000(1,end);...
                            speech_accuracy_raw(2,end), speech_accuracy_cep_100(2,end), speech_accuracy_cep_500(2,end), speech_accuracy_cep_10000(2,end);...
                            speech_accuracy_raw(3,end), speech_accuracy_cep_100(3,end), speech_accuracy_cep_500(3,end), speech_accuracy_cep_10000(3,end);...
                            speech_accuracy_raw(4,end), speech_accuracy_cep_100(4,end), speech_accuracy_cep_500(4,end), speech_accuracy_cep_10000(4,end);...
                            speech_accuracy_raw(5,end), speech_accuracy_cep_100(5,end), speech_accuracy_cep_500(5,end), speech_accuracy_cep_10000(5,end);...
                            speech_accuracy_raw(6,end), speech_accuracy_cep_100(6,end), speech_accuracy_cep_500(6,end), speech_accuracy_cep_10000(6,end)];
    
fprintf('\n\n\n')
fprintf('MFCC\nSpeech Recognition\n%i-NN\n',K)
fprintf('    Raw  W=100  W=500  W=10000\n')
fprintf('D1: %.2i   %.2i     %.2i     %.2i\n',speech_accuracy_raw(1,end), speech_accuracy_mfcc_100(1,end), speech_accuracy_mfcc_500(1,end), speech_accuracy_mfcc_10000(1,end));
fprintf('D2: %.2i   %.2i     %.2i     %.2i\n',speech_accuracy_raw(2,end), speech_accuracy_mfcc_100(2,end), speech_accuracy_mfcc_500(2,end), speech_accuracy_mfcc_10000(2,end));
fprintf('D3: %.2i   %.2i     %.2i    %.2i\n',speech_accuracy_raw(3,end), speech_accuracy_mfcc_100(3,end), speech_accuracy_mfcc_500(3,end), speech_accuracy_mfcc_10000(3,end));
fprintf('D4: %.2i   %.2i     %.2i     %.2i\n',speech_accuracy_raw(4,end), speech_accuracy_mfcc_100(4,end), speech_accuracy_mfcc_500(4,end), speech_accuracy_mfcc_10000(4,end));
fprintf('D5: %.2i   %.2i     %.2i     %.2i\n',speech_accuracy_raw(5,end), speech_accuracy_mfcc_100(5,end), speech_accuracy_mfcc_500(5,end), speech_accuracy_mfcc_10000(5,end));
fprintf('Ave:%.2i   %.2i     %.2i     %.2i\n',speech_accuracy_raw(6,end), speech_accuracy_mfcc_100(6,end), speech_accuracy_mfcc_500(6,end), speech_accuracy_mfcc_10000(6,end));

Results_speech_mfcc_1NN=[speech_accuracy_raw(1,end), speech_accuracy_mfcc_100(1,end), speech_accuracy_mfcc_500(1,end), speech_accuracy_mfcc_10000(1,end);...
                        speech_accuracy_raw(2,end), speech_accuracy_mfcc_100(2,end), speech_accuracy_mfcc_500(2,end), speech_accuracy_mfcc_10000(2,end);...
                        speech_accuracy_raw(3,end), speech_accuracy_mfcc_100(3,end), speech_accuracy_mfcc_500(3,end), speech_accuracy_mfcc_10000(3,end);...
                        speech_accuracy_raw(4,end), speech_accuracy_mfcc_100(4,end), speech_accuracy_mfcc_500(4,end), speech_accuracy_mfcc_10000(4,end);...
                        speech_accuracy_raw(5,end), speech_accuracy_mfcc_100(5,end), speech_accuracy_mfcc_500(5,end), speech_accuracy_mfcc_10000(5,end);...
                        speech_accuracy_raw(6,end), speech_accuracy_mfcc_100(6,end), speech_accuracy_mfcc_500(6,end), speech_accuracy_mfcc_10000(6,end)];

fprintf('\n\n\n')
fprintf('Ceptrum\nSpeaker Recognition\n%i-NN\n',K)
fprintf('    Raw  W=100  W=500  W=10000\n')
fprintf('A:  %.2i   %.2i     %.2i     %.2i\n',speaker_accuracy_raw(1,end), speaker_accuracy_cep_100(1,end), speaker_accuracy_cep_500(1,end), speaker_accuracy_cep_10000(1,end));
fprintf('B:  %.2i   %.2i     %.2i     %.2i\n',speaker_accuracy_raw(2,end), speaker_accuracy_cep_100(2,end), speaker_accuracy_cep_500(2,end), speaker_accuracy_cep_10000(2,end));
fprintf('C:  %.2i   %.2i     %.2i     %.2i\n',speaker_accuracy_raw(3,end), speaker_accuracy_cep_100(3,end), speaker_accuracy_cep_500(3,end), speaker_accuracy_cep_10000(3,end));
fprintf('D:  %.2i   %.2i     %.2i     %.2i\n',speaker_accuracy_raw(4,end), speaker_accuracy_cep_100(4,end), speaker_accuracy_cep_500(4,end), speaker_accuracy_cep_10000(4,end));
fprintf('Ave:%.2i   %.2i     %.2i     %.2i\n',speaker_accuracy_raw(5,end), speaker_accuracy_cep_100(5,end), speaker_accuracy_cep_500(5,end), speaker_accuracy_cep_10000(5,end));

Results_Speaker_ceptrum_1NN=[speaker_accuracy_raw(1,end), speaker_accuracy_cep_100(1,end), speaker_accuracy_cep_500(1,end), speaker_accuracy_cep_10000(1,end);...
                            speaker_accuracy_raw(2,end), speaker_accuracy_cep_100(2,end), speaker_accuracy_cep_500(2,end), speaker_accuracy_cep_10000(2,end);...
                            speaker_accuracy_raw(3,end), speaker_accuracy_cep_100(3,end), speaker_accuracy_cep_500(3,end), speaker_accuracy_cep_10000(3,end);...
                            speaker_accuracy_raw(4,end), speaker_accuracy_cep_100(4,end), speaker_accuracy_cep_500(4,end), speaker_accuracy_cep_10000(4,end);...
                            speaker_accuracy_raw(5,end), speaker_accuracy_cep_100(5,end), speaker_accuracy_cep_500(5,end), speaker_accuracy_cep_10000(5,end)];

fprintf('\n\n\n')
fprintf('MFCC\nSpeaker Recognition\n%i-NN\n',K)
fprintf('    Raw  W=100  W=500  W=10000\n')
fprintf('A:  %.2i   %.2i     %.2i     %.2i\n',speaker_accuracy_raw(1,end), speaker_accuracy_mfcc_100(1,end), speaker_accuracy_mfcc_500(1,end), speaker_accuracy_mfcc_10000(1,end));
fprintf('B:  %.2i   %.2i     %.2i     %.2i\n',speaker_accuracy_raw(2,end), speaker_accuracy_mfcc_100(2,end), speaker_accuracy_mfcc_500(2,end), speaker_accuracy_mfcc_10000(2,end));
fprintf('C:  %.2i   %.2i     %.2i     %.2i\n',speaker_accuracy_raw(3,end), speaker_accuracy_mfcc_100(3,end), speaker_accuracy_mfcc_500(3,end), speaker_accuracy_mfcc_10000(3,end));
fprintf('D:  %.2i   %.2i     %.2i     %.2i\n',speaker_accuracy_raw(4,end), speaker_accuracy_mfcc_100(4,end), speaker_accuracy_mfcc_500(4,end), speaker_accuracy_mfcc_10000(4,end));
fprintf('Ave:%.2i   %.2i     %.2i     %.2i\n',speaker_accuracy_raw(5,end), speaker_accuracy_mfcc_100(5,end), speaker_accuracy_mfcc_500(5,end), speaker_accuracy_mfcc_10000(5,end));

Results_Speaker_mfcc_1NN=[speaker_accuracy_raw(1,end), speaker_accuracy_mfcc_100(1,end), speaker_accuracy_mfcc_500(1,end), speaker_accuracy_mfcc_10000(1,end);...
                        speaker_accuracy_raw(2,end), speaker_accuracy_mfcc_100(2,end), speaker_accuracy_mfcc_500(2,end), speaker_accuracy_mfcc_10000(2,end);...
                        speaker_accuracy_raw(3,end), speaker_accuracy_mfcc_100(3,end), speaker_accuracy_mfcc_500(3,end), speaker_accuracy_mfcc_10000(3,end);...
                        speaker_accuracy_raw(4,end), speaker_accuracy_mfcc_100(4,end), speaker_accuracy_mfcc_500(4,end), speaker_accuracy_mfcc_10000(4,end);...
                        speaker_accuracy_raw(5,end), speaker_accuracy_mfcc_100(5,end), speaker_accuracy_mfcc_500(5,end), speaker_accuracy_mfcc_10000(5,end)];

%% get result for 5NN
K=5;
speech_result;
speaker_result;

%% print out result
fprintf('\n\n\n')
fprintf('Ceptrum\nSpeech Recognition\n%i-NN\n',K)
fprintf('    Raw  W=100  W=500  W=10000\n')
fprintf('D1: %.2i   %.2i     %.2i     %.2i\n',speech_accuracy_raw(1,end), speech_accuracy_cep_100(1,end), speech_accuracy_cep_500(1,end), speech_accuracy_cep_10000(1,end));
fprintf('D2: %.2i   %.2i     %.2i     %.2i\n',speech_accuracy_raw(2,end), speech_accuracy_cep_100(2,end), speech_accuracy_cep_500(2,end), speech_accuracy_cep_10000(2,end));
fprintf('D3: %.2i   %.2i     %.2i     %.2i\n',speech_accuracy_raw(3,end), speech_accuracy_cep_100(3,end), speech_accuracy_cep_500(3,end), speech_accuracy_cep_10000(3,end));
fprintf('D4: %.2i   %.2i     %.2i     %.2i\n',speech_accuracy_raw(4,end), speech_accuracy_cep_100(4,end), speech_accuracy_cep_500(4,end), speech_accuracy_cep_10000(4,end));
fprintf('D5: %.2i   %.2i     %.2i     %.2i\n',speech_accuracy_raw(5,end), speech_accuracy_cep_100(5,end), speech_accuracy_cep_500(5,end), speech_accuracy_cep_10000(5,end));
fprintf('Ave:%.2i   %.2i     %.2i     %.2i\n',speech_accuracy_raw(6,end), speech_accuracy_cep_100(6,end), speech_accuracy_cep_500(6,end), speech_accuracy_cep_10000(6,end));

Results_speech_ceptrum_5NN=[speech_accuracy_raw(1,end), speech_accuracy_cep_100(1,end), speech_accuracy_cep_500(1,end), speech_accuracy_cep_10000(1,end);...
                            speech_accuracy_raw(2,end), speech_accuracy_cep_100(2,end), speech_accuracy_cep_500(2,end), speech_accuracy_cep_10000(2,end);...
                            speech_accuracy_raw(3,end), speech_accuracy_cep_100(3,end), speech_accuracy_cep_500(3,end), speech_accuracy_cep_10000(3,end);...
                            speech_accuracy_raw(4,end), speech_accuracy_cep_100(4,end), speech_accuracy_cep_500(4,end), speech_accuracy_cep_10000(4,end);...
                            speech_accuracy_raw(5,end), speech_accuracy_cep_100(5,end), speech_accuracy_cep_500(5,end), speech_accuracy_cep_10000(5,end);...
                            speech_accuracy_raw(6,end), speech_accuracy_cep_100(6,end), speech_accuracy_cep_500(6,end), speech_accuracy_cep_10000(6,end)];
    
fprintf('\n\n\n')
fprintf('MFCC\nSpeech Recognition\n%i-NN\n',K)
fprintf('    Raw  W=100  W=500  W=10000\n')
fprintf('D1: %.2i   %.2i     %.2i     %.2i\n',speech_accuracy_raw(1,end), speech_accuracy_mfcc_100(1,end), speech_accuracy_mfcc_500(1,end), speech_accuracy_mfcc_10000(1,end));
fprintf('D2: %.2i   %.2i     %.2i     %.2i\n',speech_accuracy_raw(2,end), speech_accuracy_mfcc_100(2,end), speech_accuracy_mfcc_500(2,end), speech_accuracy_mfcc_10000(2,end));
fprintf('D3: %.2i   %.2i     %.2i    %.2i\n',speech_accuracy_raw(3,end), speech_accuracy_mfcc_100(3,end), speech_accuracy_mfcc_500(3,end), speech_accuracy_mfcc_10000(3,end));
fprintf('D4: %.2i   %.2i     %.2i     %.2i\n',speech_accuracy_raw(4,end), speech_accuracy_mfcc_100(4,end), speech_accuracy_mfcc_500(4,end), speech_accuracy_mfcc_10000(4,end));
fprintf('D5: %.2i   %.2i     %.2i     %.2i\n',speech_accuracy_raw(5,end), speech_accuracy_mfcc_100(5,end), speech_accuracy_mfcc_500(5,end), speech_accuracy_mfcc_10000(5,end));
fprintf('Ave:%.2i   %.2i     %.2i     %.2i\n',speech_accuracy_raw(6,end), speech_accuracy_mfcc_100(6,end), speech_accuracy_mfcc_500(6,end), speech_accuracy_mfcc_10000(6,end));

Results_speech_mfcc_5NN=[speech_accuracy_raw(1,end), speech_accuracy_mfcc_100(1,end), speech_accuracy_mfcc_500(1,end), speech_accuracy_mfcc_10000(1,end);...
                        speech_accuracy_raw(2,end), speech_accuracy_mfcc_100(2,end), speech_accuracy_mfcc_500(2,end), speech_accuracy_mfcc_10000(2,end);...
                        speech_accuracy_raw(3,end), speech_accuracy_mfcc_100(3,end), speech_accuracy_mfcc_500(3,end), speech_accuracy_mfcc_10000(3,end);...
                        speech_accuracy_raw(4,end), speech_accuracy_mfcc_100(4,end), speech_accuracy_mfcc_500(4,end), speech_accuracy_mfcc_10000(4,end);...
                        speech_accuracy_raw(5,end), speech_accuracy_mfcc_100(5,end), speech_accuracy_mfcc_500(5,end), speech_accuracy_mfcc_10000(5,end);...
                        speech_accuracy_raw(6,end), speech_accuracy_mfcc_100(6,end), speech_accuracy_mfcc_500(6,end), speech_accuracy_mfcc_10000(6,end)];

fprintf('\n\n\n')
fprintf('Ceptrum\nSpeaker Recognition\n%i-NN\n',K)
fprintf('    Raw  W=100  W=500  W=10000\n')
fprintf('A:  %.2i   %.2i     %.2i     %.2i\n',speaker_accuracy_raw(1,end), speaker_accuracy_cep_100(1,end), speaker_accuracy_cep_500(1,end), speaker_accuracy_cep_10000(1,end));
fprintf('B:  %.2i   %.2i     %.2i     %.2i\n',speaker_accuracy_raw(2,end), speaker_accuracy_cep_100(2,end), speaker_accuracy_cep_500(2,end), speaker_accuracy_cep_10000(2,end));
fprintf('C:  %.2i   %.2i     %.2i     %.2i\n',speaker_accuracy_raw(3,end), speaker_accuracy_cep_100(3,end), speaker_accuracy_cep_500(3,end), speaker_accuracy_cep_10000(3,end));
fprintf('D:  %.2i   %.2i     %.2i     %.2i\n',speaker_accuracy_raw(4,end), speaker_accuracy_cep_100(4,end), speaker_accuracy_cep_500(4,end), speaker_accuracy_cep_10000(4,end));
fprintf('Ave:%.2i   %.2i     %.2i     %.2i\n',speaker_accuracy_raw(5,end), speaker_accuracy_cep_100(5,end), speaker_accuracy_cep_500(5,end), speaker_accuracy_cep_10000(5,end));

Results_Speaker_ceptrum_5NN=[speaker_accuracy_raw(1,end), speaker_accuracy_cep_100(1,end), speaker_accuracy_cep_500(1,end), speaker_accuracy_cep_10000(1,end);...
                            speaker_accuracy_raw(2,end), speaker_accuracy_cep_100(2,end), speaker_accuracy_cep_500(2,end), speaker_accuracy_cep_10000(2,end);...
                            speaker_accuracy_raw(3,end), speaker_accuracy_cep_100(3,end), speaker_accuracy_cep_500(3,end), speaker_accuracy_cep_10000(3,end);...
                            speaker_accuracy_raw(4,end), speaker_accuracy_cep_100(4,end), speaker_accuracy_cep_500(4,end), speaker_accuracy_cep_10000(4,end);...
                            speaker_accuracy_raw(5,end), speaker_accuracy_cep_100(5,end), speaker_accuracy_cep_500(5,end), speaker_accuracy_cep_10000(5,end)];

fprintf('\n\n\n')
fprintf('MFCC\nSpeaker Recognition\n%i-NN\n',K)
fprintf('    Raw  W=100  W=500  W=10000\n')
fprintf('A:  %.2i   %.2i     %.2i     %.2i\n',speaker_accuracy_raw(1,end), speaker_accuracy_mfcc_100(1,end), speaker_accuracy_mfcc_500(1,end), speaker_accuracy_mfcc_10000(1,end));
fprintf('B:  %.2i   %.2i     %.2i     %.2i\n',speaker_accuracy_raw(2,end), speaker_accuracy_mfcc_100(2,end), speaker_accuracy_mfcc_500(2,end), speaker_accuracy_mfcc_10000(2,end));
fprintf('C:  %.2i   %.2i     %.2i     %.2i\n',speaker_accuracy_raw(3,end), speaker_accuracy_mfcc_100(3,end), speaker_accuracy_mfcc_500(3,end), speaker_accuracy_mfcc_10000(3,end));
fprintf('D:  %.2i   %.2i     %.2i     %.2i\n',speaker_accuracy_raw(4,end), speaker_accuracy_mfcc_100(4,end), speaker_accuracy_mfcc_500(4,end), speaker_accuracy_mfcc_10000(4,end));
fprintf('Ave:%.2i   %.2i     %.2i     %.2i\n',speaker_accuracy_raw(5,end), speaker_accuracy_mfcc_100(5,end), speaker_accuracy_mfcc_500(5,end), speaker_accuracy_mfcc_10000(5,end));

Results_Speaker_mfcc_5NN=[speaker_accuracy_raw(1,end), speaker_accuracy_mfcc_100(1,end), speaker_accuracy_mfcc_500(1,end), speaker_accuracy_mfcc_10000(1,end);...
                        speaker_accuracy_raw(2,end), speaker_accuracy_mfcc_100(2,end), speaker_accuracy_mfcc_500(2,end), speaker_accuracy_mfcc_10000(2,end);...
                        speaker_accuracy_raw(3,end), speaker_accuracy_mfcc_100(3,end), speaker_accuracy_mfcc_500(3,end), speaker_accuracy_mfcc_10000(3,end);...
                        speaker_accuracy_raw(4,end), speaker_accuracy_mfcc_100(4,end), speaker_accuracy_mfcc_500(4,end), speaker_accuracy_mfcc_10000(4,end);...
                        speaker_accuracy_raw(5,end), speaker_accuracy_mfcc_100(5,end), speaker_accuracy_mfcc_500(5,end), speaker_accuracy_mfcc_10000(5,end)];
