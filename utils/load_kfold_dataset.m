function [dataset, dataset_name, index, k_in, k_out] = load_kfold_dataset(experiment_name, dataset_name,  k_out, k_in)
    try
        load(sprintf('~/Dropbox/mlm-matlab/experiments/dataset_divisions/%s_%s.mat',...
        experiment_name, dataset_name));
    catch exception
        generate_dataset_kfold(experiment_name, dataset_name, k_out, k_in);
        load(sprintf('~/Dropbox/mlm-matlab/experiments/dataset_divisions/%s_%s.mat',...
        experiment_name, dataset_name));
    end
end