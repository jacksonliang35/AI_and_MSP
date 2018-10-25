%% Load Data
% path='E:\Google Drive\ECE 417\MP7'
function [Frames]=run(path)
%path = './';
if(~strcmp(path(end),'/'))
        path=[path,'/'];
end

Img = imread([path,'mouth.jpg']);
load([path,'ECE417_MP5_AV_Data.mat']);
meshfile = fopen([path,'mesh.txt'],'r');
nv = fscanf(meshfile,'%d',1);
mesh.vertices = zeros(2,nv);
mesh.vertices = fscanf(meshfile,'%d %d',[2 nv]);
mesh.vertices = mesh.vertices';
nt = fscanf(meshfile,'%d',1);
mesh.triangles = zeros(3,nt);
mesh.triangles = fscanf(meshfile,'%d %d %d',[3 nt]);
mesh.triangles = mesh.triangles';
fclose(meshfile);
clear ans meshfile nt nv;

%% Train

numN = 20;  % hyper-parameter
fprintf('\n------------------------------------\n Start ANNs training with %d hidden neurons\n------------------------------------\n\n',numN);
mapping = ECE417_MP5_train(av_train,av_validate,silenceModel,numN,[path,'train_result_',num2str(numN)]);

%% Find Visual Features for testAudio
fprintf('\n------------------\n Testing\n------------------\n\n');

F = ECE417_MP5_test(testAudio,silenceModel,mapping);

%% Warping
%assert F = 3 x 456
%load ./ANNresults;
%F = results;
%clear results;
assert(size(F,1)==3);
assert(size(F,2)==456);
fScale = 1; % hyper-parameter
Frames = zeros([size(Img),size(testAudio,2)]);
t0 = 0; % Equilibrium Frame
fprintf('\n------------------\n Starting generating frames\n------------------\n\n',numN);
for t=1:size(testAudio,2)
    % Reusing equilibrium frames to boost speed (feel free to comment)
    if t0~=0 && t>t0 && all(F(:,t)==zeros(3,1))
        Frames(:,:,t) = Frames(:,:,t0);
    else
        [retVertX,retVertY] = interpVert(mesh.vertices(:,1),mesh.vertices(:,2),0,0,0,F(1,t),F(2,t),F(3,t),fScale);
        [frame] = warping(mesh.vertices,[retVertX,retVertY],mesh.triangles,double(Img));
        Frames(:,:,t) = frame;
        if t0==0 && all(F(:,t)==zeros(3,1))
            t0 = t;
        end
    end
    fprintf('Generate frame %d\n',t);
    %disp(t);
end
Frames=uint8(Frames);
save('trained_Frame.mat','Frames');

%% Generate Movie
fprintf('\n------------------\n Starting saving frames\n------------------\n\n',numN);
%load('trained_Frame.mat')
mkdir('test_img_zzhng122');
for i=1:456
    temp=num2str(10000+i-1);
    imwrite(Frames(:,:,i),['test_img_zzhng122/test_',temp(2:end),'.jpg']);
end
end
%! DxBMP\DxBMP -framerate 30 test_img\test_*.jpg test_img\test.avi