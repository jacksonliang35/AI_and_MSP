function RY=rand_proj(principle_eigVal,feature_data)
N = length(principle_eigVal);
[num_row,~]=size(feature_data);
R = randn(num_row,N);  % N random vectors for projection
RY = R'*feature_data; % Projection
end