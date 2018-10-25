function [precision_list]=run_ener_90(path)
[Imageset,N1,N2]=load_img(path);
energy=0.9;

%% get all PCA
[principle_PCA_9070,principle_eigVal_9070,Error_est_9070,Error_true_9070]=calc_PCA(Imageset.image_9070,energy);
%[principle_PCA_7090,principle_eigVal_7090,Error_est_7090,Error_true_7090]=calc_PCA(Imageset.image_7090,energy);
%[principle_PCA_3545,principle_eigVal_3545,Error_est_3545,Error_true_3545]=calc_PCA(Imageset.image_3545,energy);
%[principle_PCA_1722,principle_eigVal_1722,Error_est_1722,Error_true_1722]=calc_PCA(Imageset.image_1722,energy);
%[principle_PCA_user,principle_eigVal_user,Error_est_user,Error_true_user]=calc_PCA(Imageset.image_user,energy);

%% get all random matrix
RY_9070=rand_proj(principle_eigVal_9070,Imageset.image_9070);
%RY_7090=rand_proj(principle_eigVal_7090,Imageset.image_7090);
%RY_3545=rand_proj(principle_eigVal_3545,Imageset.image_3545);
%RY_1722=rand_proj(principle_eigVal_1722,Imageset.image_1722);
%RY_user=rand_proj(principle_eigVal_user,Imageset.image_user);

precision_list=cell(12,6);
i=1;
%% calc precption of random 1NN
K=1;

train_data=Imageset.image_7090;
dim_row=70;
dim_col=90;

[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_raw(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall};
i=i+1;

%
train_data=Imageset.image_3545;
dim_row=35;
dim_col=45;

[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_raw(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;

%
train_data=Imageset.image_1722;
dim_row=17;
dim_col=22;

[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_raw(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;

%
train_data=Imageset.image_user;
dim_row=N1;
dim_col=N2;

[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_raw(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;

%% pca data 1NN

%
train_data=principle_PCA_9070;
dim_row=90;
dim_col=70;

[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_PCA(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;

%{
train_data=principle_PCA_3545;
dim_row=35;
dim_col=45;

[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_PCA(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;

%
train_data=principle_PCA_1722;
dim_row=17;
dim_col=22;

[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_PCA(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;

%
train_data=principle_PCA_user;
dim_row=N1;
dim_col=N2;

[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_PCA(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;
%}
%% Rand Matrix data 1NN
%
train_data=RY_9070;
dim_row=90;
dim_col=70;
[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_rand(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;

%{
train_data=RY_3545;
dim_row=35;
dim_col=45;
[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_rand(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;

%
train_data=RY_1722;
dim_row=17;
dim_col=22;
[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_rand(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;

%
train_data=RY_user;
dim_row=N1;
dim_col=N2;
[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_rand(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;
%}

%% calc precption of random 5NN
K=5;

train_data=Imageset.image_7090;
dim_row=70;
dim_col=90;

[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_raw(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;

%
train_data=Imageset.image_3545;
dim_row=35;
dim_col=45;

[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_raw(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;

%
train_data=Imageset.image_1722;
dim_row=17;
dim_col=22;

[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_raw(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;

%
train_data=Imageset.image_user;
dim_row=N1;
dim_col=N2;

[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_raw(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;

%% pca data 5NN

%
train_data=principle_PCA_9070;
dim_row=90;
dim_col=70;

[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_PCA(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;

%{
train_data=principle_PCA_3545;
dim_row=35;
dim_col=45;

[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_PCA(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;

%
train_data=principle_PCA_1722;
dim_row=17;
dim_col=22;

[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_PCA(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;

%
train_data=principle_PCA_user;
dim_row=N1;
dim_col=N2;

[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_PCA(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;
%}
%% Rand Matrix data 5NN
%
train_data=RY_9070;
dim_row=70;
dim_col=90;
[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_rand(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;

%{
train_data=RY_3545;
dim_row=35;
dim_col=45;
[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_rand(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;

%
train_data=RY_1722;
dim_row=17;
dim_col=22;
[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_rand(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;

%
train_data=RY_user;
dim_row=N1;
dim_col=N2;
[type,acc_A,acc_B,acc_C,acc_D,acc_overall]=get_prec_rand(train_data,dim_row,dim_col,K,energy);
precision_list(i,:)={type,acc_A,acc_B,acc_C,acc_D,acc_overall}; i=i+1;
%}







end