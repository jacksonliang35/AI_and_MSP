function [Y,principle_eigVal]=calc_PCA(input_data,energy)
%% obtain PCA for raw data
[M,b]=size(input_data);
mean_wrt=mean(input_data,2); %[6300x1] mean
%X_tilde=bsxfun(@minus,input_data,mean_wrt)./sqrt(M-1); 
X_tilde=(input_data-repmat(mean_wrt,[1,b]))./sqrt(M-1); 
%Sigma=X_tilde*X_tilde';
Gram=X_tilde'*X_tilde; %[80x80] gram matrix
[V,K]=eig(Gram);
S=sqrt(K);
eigval=diag(K);
weighted_PCA=X_tilde*V; %U*S
orth_PCA=weighted_PCA/S; %U

%% find top 95% of energy
total_energy=sum(eigval);
sum_min=0;
least_N=0;
while(sum_min<(1-energy)*total_energy)
    least_N=least_N+1;
    sum_min=sum_min+(eigval(least_N)); %% not sure
end
principle_eigVal=eigval(end:-1:least_N);
principle_PCA=orth_PCA(:,end:-1:least_N);%reordered
Y=principle_PCA'*(X_tilde*sqrt(M-1));
end
