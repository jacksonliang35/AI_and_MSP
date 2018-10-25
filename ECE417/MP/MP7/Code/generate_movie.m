load('trained_Frame.mat')
mkdir('test_img');
for i=1:456
    temp=num2str(10000+i-1);
    imwrite(Frames(:,:,i),['test_img/test_',temp(2:end),'.jpg']);
end
! DxBMP\DxBMP -framerate 30 test_img\test_*.jpg test_img\test.avi