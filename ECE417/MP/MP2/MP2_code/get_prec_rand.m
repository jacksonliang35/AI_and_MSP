function [type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_rand(train_data,dim_row,dim_col,K,energy)
[N,~]=size(train_data);
acc_list=zeros(80,1); % 0 is wrong label, 1 is right label
for i=1:80
    label=knn(train_data,train_data(:,i),K);
    if(label==ceil(i/20))
        acc_list(i)=1;
    end
end
acc_A=sum(acc_list(1:20))/20*100;
acc_B=sum(acc_list(21:40))/20*100;
acc_C=sum(acc_list(41:60))/20*100;
acc_D=sum(acc_list(61:80))/20*100;
acc_overall=sum(acc_list)/80*100;
fprintf('Feat = rand, Input Dims = %i, kNN = %i, Energy=0.%i, random Projection dim (N) = %i \n',dim_row*dim_col,K,energy*100,N);
fprintf('A: %.2f B: %.2f C: %.2f D: %.2f Overall: %.2f\n\n',acc_A,acc_B,acc_C,acc_D,acc_overall);
type=['rand',num2str(dim_row),'x',num2str(dim_col),' ',num2str(K),'NN',num2str(energy)];
end