function append_metrics(experiment_name, metrics, dataset_name, model_name)
    try
        load(sprintf('~/Dropbox/mlm-matlab/experiments/metrics/%s.mat',experiment_name));
        eval(sprintf('%s.%s = metrics;', dataset_name, model_name));
        save(sprintf('~/Dropbox/mlm-matlab/experiments/metrics/%s.mat',experiment_name),dataset_name,'-append');
    catch exception
        eval(sprintf('%s.%s = metrics;', dataset_name, model_name));
        save(sprintf('~/Dropbox/mlm-matlab/experiments/metrics/%s.mat',experiment_name),dataset_name);
    end
end