function [Imageset,N1,N2]=load_img(path)
%Imageset.path='./newimdata'; 
Imageset.path=path;
Imageset.filenamelist=cell(80,1);
Imageset.filenamelist(:)={''};
for i=1:20
    eval(['Imageset.filenamelist(',int2str(i),')={''A',int2str(i),'.jpg''};']);
    eval(['Imageset.filenamelist(',int2str(20+i),')={''B',int2str(i),'.jpg''};']);
    eval(['Imageset.filenamelist(',int2str(40+i),')={''C',int2str(i),'.jpg''};']);
    eval(['Imageset.filenamelist(',int2str(60+i),')={''D',int2str(i),'.jpg''};']); 
end

%%call each image by [char(Imageset.path),'/',char(Imageset.filenamelist(1))]


%% read image
Imageset.image_9070=zeros(6300,80);
Imageset.image_7090=zeros(6300,80);
Imageset.image_3545=zeros(1575,80);
Imageset.image_1722=zeros(374,80);

N1=7;
N2=9;
Imageset.image_user=zeros(N1*N2,80);


for i=1:80
   temp=im2double(rgb2gray(imread([char(Imageset.path),'/',char(Imageset.filenamelist(i))])));
   temp_7090=reshape(imresize(temp,[70,90]),[6300,1]);
   temp_3545=reshape(imresize(temp,[35,45]),[35*45,1]);
   temp_1722=reshape(imresize(temp,[17,22]),[17*22,1]);
   temp_user=reshape(imresize(temp,[N1,N2]),[N1*N2,1]);
   temp=reshape(temp,[6300,1]);
   Imageset.image_9070(:,i)=temp;
   Imageset.image_7090(:,i)=temp_7090;
   Imageset.image_3545(:,i)=temp_3545;
   Imageset.image_1722(:,i)=temp_1722;
   Imageset.image_user(:,i)=temp_user;
end
end