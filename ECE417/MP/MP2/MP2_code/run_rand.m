function [precision_list]=run_rand(path)
[Imageset,N1,N2]=load_img(path);
energy=0.95;

%% get all PCA
[principle_PCA_9070,principle_eigVal_9070,Error_est_9070,Error_true_9070]=calc_PCA(Imageset.image_9070,energy);


precision_list=cell(20,6);

%% calc precption of random NN
%
for i=1:10
    RY_9070=rand_proj(principle_eigVal_9070,Imageset.image_9070);
    train_data=RY_9070;
    dim_row=90;
    dim_col=70;
    [type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_rand(train_data,dim_row,dim_col,1,energy);
    precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall};     
    [type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_rand(train_data,dim_row,dim_col,5,energy);
    precision_list(i+10,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; 
end

end
