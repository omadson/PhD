clear;clc;close all;

experiment_name = 'esann_2019_2';
load(sprintf('metrics/%s.mat', experiment_name));
% datasets = who;
datasets = {'motorcycle','cpu','housing'};
for i=1:length(datasets)
    load(sprintf('dataset_divisions/%s_%s.mat',experiment_name, datasets{i}));
%     models = eval(sprintf('struct2cell(%s)',datasets{i}));
    models = eval(sprintf('%s;',datasets{i}));
%     model_names = eval(sprintf('fieldnames(%s);',datasets{i}));
    
    
    model_names = {'MLM_RN_RN', 'MLM_FL_FL', 'MF_MLM_MF_MF1', 'MF_MLM_MF_MF2', 'MF_MLM_MF_MF3'};
    
    fprintf('%15s\n',datasets{i});
    for k=1:length(model_names)
        fprintf('%15s: ', model_names{k});
        for j=1:length(index)
            y_test = dataset(index{j}.test,end);
            y_hat  = models.(model_names{k}).y_hat_test{j};
            mse(j) = sqrt(mean((y_test - y_hat).^2));
%             plot(y_test, y_hat,'.')
            full_size(j) = length(index{j}.train);
        end     
        
        rp_in  = 100*(1 - models.(model_names{k}).model.rp_in ./ full_size);
        rp_out = 100*(1 - models.(model_names{k}).model.rp_out ./ full_size);
        
        fprintf('%10.3f   ± %8.3f   |', mean(mse), std(mse));
        fprintf('%10.3f   ± %8.3f   |', mean(rp_in), std(rp_in));
        fprintf('%10.3f   ± %8.3f   \n', mean(rp_out), std(rp_out));
        
        prefix = sprintf('%s.%s.',datasets{i},model_names{k});
%         eval() mean(mse);
        std(mse);
    end
    fprintf('\n');
    
    model = eval(sprintf('fieldnames(%s);',datasets{1}));
end

