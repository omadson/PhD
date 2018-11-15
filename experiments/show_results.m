clear;clc;close all;

experiment_name = 'esann_2019_3';
load(sprintf('metrics/%s.mat', experiment_name));
% datasets = who;
datasets = {'motorcycle','cpu','forestfires','housing','concrete'};
for i=1:length(datasets)
    load(sprintf('dataset_divisions/%s_%s.mat',experiment_name, datasets{i}));
%     models = eval(sprintf('struct2cell(%s)',datasets{i}));
    models = eval(sprintf('%s;',datasets{i}));
    model_names = eval(sprintf('fieldnames(%s);',datasets{i}));
    
    
    model_names = {'MF_MLM_MF_FL1', 'MF_MLM_MF_FL2', 'MF_MLM_MF_FL3','MLM_RN_FL', 'MLM_FL_FL', };
    
    fprintf('%15s\n',datasets{i});
    for k=1:length(model_names)
%         fprintf('%15s: ', model_names{k});
        for j=1:length(index)
            y_test = dataset(index{j}.test,end);
            y_hat  = models.(model_names{k}).y_hat_test{j};
            mse(j) = sqrt(mean((y_test - y_hat).^2));
%             plot(y_test, y_hat,'.')
            full_size(j) = length(index{j}.train);
        end     
        
        rp_in_p  = 100*(1 - models.(model_names{k}).model.rp_in ./ full_size);
        rp_out_p = 100*(1 - models.(model_names{k}).model.rp_out ./ full_size);
        
        fprintf('%10.1f & %8.1f &', mean(mse), std(mse));
%         fprintf('%10.1f & %8.1f   |', mean(rp_in_p), std(rp_in_p));
%         fprintf('%10.1f & %8.1f   \n', mean(models.(model_names{k}).model.rp_in), std(models.(model_names{k}).model.rp_in));
        
        prefix = sprintf('%s.%s.',datasets{i},model_names{k});
    end
    fprintf('\n                      & \\#IRPs  &');
    for k=1:length(model_names)
         fprintf('%10.1f & %8.1f &', mean(models.(model_names{k}).model.rp_in), std(models.(model_names{k}).model.rp_in));
    end
    fprintf('\n');
    
    model = eval(sprintf('fieldnames(%s);',datasets{1}));
end

