function result = verify_model_run(experiment_name, dataset_name, model_name)
    try
        load(sprintf('~/Dropbox/mlm-matlab/experiments/metrics/%s.mat',experiment_name));
        if exist(dataset_name)
            test = eval(sprintf('isfield(%s,''%s'')', dataset_name, model_name));
            if test
                result = true;
            else
                result = false;
            end
        else
            result = false;
        end
    catch exception
        result = false;
    end
end