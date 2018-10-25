% datadir='E:\Google Drive\ECE 417\MP6';
% datadir='/Users/zhangzixu/Google Drive/ECE 417/MP6'
% jpgdir=[datadir,'/jpg']
% rectdir=[datadir,'/rects']
function run(jpgdir,rectdir)
%% Import Rects & Images
if(~strcmp(jpgdir(end),'/'))
        jpgdir=[jpgdir,'/'];
end
if(~strcmp(rectdir(end),'/'))
        rectdir=[rectdir,'/'];
end
% load rects and jpg
totalrects = load([rectdir,'allrects.txt'],'-ascii');
JPGDIR=jpgdir;
files = dir(JPGDIR);
totalII = zeros(480,720,168);
for i=3:length(files)
    if(strcmp(files(i).name(end-3:end),'jpeg'))
        totalII(:,:,i-2) = integralimage(imread([JPGDIR,'/',files(i).name]));
    end
end
%% Training w/ Adaboost
trainrects = totalrects(1:126,17:48);
trainII = totalII(:,:,1:126);
Y = [ones(126,4),zeros(126,4)]; % labels
W = ones(126,8);    %[num of images x NR per image]
% Adaboost
beta = zeros(1,40);
besth = zeros(40,8);
for t=1:40
    disp(t);
    % renormalize W
    W = W/sum(sum(W));
    % exhaustive search
    minerr = 0.51;
    for fx = 0:1/6:5/6
        for fy = 0:1/6:5/6
            for fw = 1/6:1/6:(1-fx)
                for fh = 1/6:1/6:(1-fy)
                    % Get fraction
                    rectf = [fx,fy,fw,fh];
                    for vert = [0,1]
                        for order = (1+vert):(4-vert)
                            % Compute features for the entire database
                            F = rectfeature(trainII,trainrects,rectf,order,vert);
                            % Compute threshold, polarity & error rate
                            [theta,p,err] = bestthreshold(F,Y,W);
                            if err < minerr
                                minerr = err;
                                besth(t,:) = [rectf,order,vert,theta,p];
                            end
                        end
                    end

                end
            end
        end
    end
    
    % update weight matrix W
    beta(t) = minerr/(1-minerr);
    fprintf('min error: %d, Beta: %d \n',minerr,beta(t));
    F = rectfeature(trainII,trainrects,besth(t,1:4),besth(t,5),besth(t,6));
    classify = besth(t,8).*F<besth(t,8)*besth(t,7);
    W((classify==Y)) = W((classify==Y)).*beta(t);
end

save train_result
%% Testing
testII=totalII(:,:,127:end);
testrects=totalrects(127:end,17:48);
[num_test,~]=size(testrects);
F=zeros(num_test,8,40);
single_classify=zeros(num_test,8,40);
scaled_classify=zeros(num_test,8,40);
Y_test = [ones(num_test,4),-ones(num_test,4)];
for t=1:40
    F(:,:,t) = rectfeature(testII,testrects,besth(t,1:4),besth(t,5),besth(t,6));
    alpha=-log(beta(t));
    single_classify(:,:,t)=besth(t,end).*sign(besth(t,end-1)-F(:,:,t));
    scaled_classify(:,:,t)=alpha.*single_classify(:,:,t);
    %class_label=class_label+alpha.*(2*(besth(t,8)*F<besth(t,8)*besth(t,7))-1);
end
final_classify=cumsum(scaled_classify,3);
totalerr=zeros(40,1);
singleerr=zeros(40,1);
for t=1:40
    totalerr(t)=mean(mean(sign(final_classify(:,:,t))~= Y_test));
    singleerr(t)=mean(mean(sign(single_classify(:,:,t))~= Y_test));
end

%% result
figure

set(gcf,'defaultAxesTickLabelInterpreter','latex');
set(gcf,'defaulttextinterpreter','latex');
set(gcf, 'defaultLegendInterpreter','latex');
set(gcf,'DefaultAxesFontsize',24);
set(gcf,'DefaultTextFontname','Times New Roman');
set(gcf,'DefaultAxesFontname','Times New Roman');
set(gcf, 'Units', 'Normalized', 'OuterPosition', [0.05 0.05 0.9 0.9]);
set(gca,'XMinorTick','on','YMinorTick','on')

hold on
plot(totalerr.*100,'-k','LineWidth',2,'DisplayName','Unweighted Error of Strong Classifier')
plot(singleerr.*100,'--b','LineWidth',2,'DisplayName','Unweighted Error of Weak Classifier')
plot(beta./(1+beta).*100,'-.r','LineWidth',2,'DisplayName','Weighted Error Rate')
legend show
legend('Location','northwest')
legend('boxoff')
box on
xlabel('Iteration')
ylabel('Error Rate $[\%]$')
xlim([0,41])
ylim([0,100])



