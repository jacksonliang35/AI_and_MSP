set(groot,'defaultAxesTickLabelInterpreter','latex');
set(groot,'defaulttextinterpreter','latex');
set(groot, 'defaultLegendInterpreter','latex');
set(groot,'DefaultAxesFontsize',24);
set(groot,'DefaultTextFontname','Times New Roman');
set(groot,'DefaultAxesFontname','Times New Roman');

close all
clear

global percision;
global query_counter;
global file_name;



percision=[];
query_counter=-1;
figure_counter=0;
figure_list=[];
percision_all=[];
while(figure_counter<5)
if(query_counter==-1)
    
    cbirMP;
    query_counter=0;
    percision=[];
end
uiwait
query_counter=-1;
figure_counter=figure_counter+1;
if(length(percision)<5)
    temp=zeros(1,5);
    temp(1:length(percision))=percision;
    percision_all=[percision_all;temp];
else
    percision_all=[percision_all;percision(1:5)];
end
figure_list=[figure_list;file_name];
end
f=figure(1);
hold on
symbol=["-ok";"--ok";":ok";"-*k";"--*k"];
for i=1:5
    plot(1:5,percision_all(i,:),char(symbol(i)),'LineWidth',3,'MarkerSize',12,'DisplayName',string(figure_list(i,:)))
end
box on
legend('show')
xlabel('num of trails')
ylabel('Percesion')
ylim([0,1.1])
legend('Location','southeast')
