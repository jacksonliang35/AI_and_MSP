function [accuracy,likelihood_list]=audio_accuracy(test_data,GMM)
accuracy=zeros(5,2);
N_model=size(GMM,2);
likelihood_list=zeros(N_model,40);
    for p=1:4
        for i=1:10
           [likelihood,gmm_label]= find_label_GMM(test_data.cep(:,:,(p-1)*10+i)',GMM);
           likelihood_list(:,(p-1)*10+i)=likelihood;
           if(gmm_label==p)
               accuracy(p,1)=accuracy(p,1)+1;
           end
        end
    end
    accuracy(end,1)=sum(accuracy(1:end-1,1));
    accuracy(1:end-1,2)=accuracy(1:end-1,1)./10;
    accuracy(end,end)=accuracy(end,1)./40;

end

function [pr_list,idx]=find_label_GMM(x,GMM)
N_model=size(GMM,2);
pr_list=zeros(N_model,1);
for i=1:N_model
    pr_list(i)=gmm_eval(x, GMM(i));
end
[~,idx]=max(pr_list);
end