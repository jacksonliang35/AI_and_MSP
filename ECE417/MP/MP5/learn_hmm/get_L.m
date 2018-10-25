function accurate=get_L(train_seq,test_idx,P0,A,mu,sigma,N,A_init)
test_seq=train_seq{test_idx};
train_seq=[train_seq(1:test_idx-1),train_seq(test_idx+1:end)];

[P0_c,A_c,mu_c,sigma_c] = ghmm_learn(train_seq,N,A_init);

[~,scale_correct] = ghmm_fwd(test_seq,A_c,P0_c,mu_c,sigma_c);
P_correct = (sum(scale_correct));

[~,scale_wrong] = ghmm_fwd(test_seq,A,P0,mu,sigma);
P_wrong=(sum(scale_wrong));

if(P_correct>P_wrong)
    accurate=1;
else
    accurate=0;
end
end
