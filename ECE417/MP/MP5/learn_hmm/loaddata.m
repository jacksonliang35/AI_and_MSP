function [Audio_data,Visual_data,AV_data]=loaddata(datadir)
    if(~strcmp(datadir(end),'/'))
        datadir=[datadir,'/'];
    end

    Audio_data=cell(2,10); %first row store class 2, second row store class 5
    Visual_data=cell(2,10);
    AV_data = cell(2,10);

    % load class 2
    for i=1:10
       Audio_data(1,i)={importdata([datadir,'2.',num2str(i),'.a.fea'])};
       Visual_data(1,i)={importdata([datadir,'2.',num2str(i),'.v.fea'])};
    end
    % load class 5
    for i=1:10
       Audio_data(2,i)={importdata([datadir,'5.',num2str(i),'.a.fea'])};
       Visual_data(2,i)={importdata([datadir,'5.',num2str(i),'.v.fea'])};
    end
    
    for i = 1:2
        for j = 1:10
            AV_data{i,j} = [Audio_data{i,j},Visual_data{i,j}];
        end
    end
end