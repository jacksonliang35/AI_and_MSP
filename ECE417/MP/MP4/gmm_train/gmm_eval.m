function Y = gmm_eval(X, model)
%gmm_eval GMM probability density function (pdf).
%   Y = gmm_eval(X,model) returns the pdf of the GMM distribution, evaluated for the obsvns in X.
%   X is a two dimensional matrix [#Frames x #Dimensions]
%   model is the GMM estimated by gmm_train
% 

N = size(X, 1);
K = length(model.weight);

% Preallocate likelihood matrix for each component density
LL = ones(N, K);

for k = 1:K
    % Compute the likelihood of the observations w.r.t. the kth component density 
    LL(:,k) = mvnpdf(X,model.mu(:,k)',model.sigma(:,k)');
end

% Now LL(i,k) is the likelihood of xi w.r.t kth component density of the GMM
% The likelihood of xi w.r.t GMM = sum_k=1..K LL(i,k)
total = LL*model.weight ; % [N x 1]. total(i) = likelihood of xi
%total=sum(LL,2);

% Take the log of total(i), i=1...,N and find the mean of the logs
Y = sum(log(total))/N ; % average log-likelihood of data matrix X
