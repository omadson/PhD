function [best_parameters] = Crossvalidation(K, model_class, parameters, X, y)
    %% create all combinations of parameters
    parameter_names = fieldnames(parameters);
    if length(parameters) > 1
        args = sprintf('%s%s', sprintf('parameters.%s, ',...
            parameter_names{1:end-1}), sprintf('parameters.%s',...
            parameter_names{end}));
    else
        args = sprintf('parameters.%s', parameter_names{1});
    end
    eval(sprintf('parameter_combination = combvec(%s)'';', args));
    %% LOOP of parameters
    [N, M] = size(parameter_combination);
    for i=1:N
        parameters_ = cell2struct(num2cell(parameter_combination(i,:)), parameter_names',2);
        clf = eval(sprintf('%s(parameters_);',model_class));
        %% K-fold LOOP
        indices = crossvalind('Kfold',y,K);
        for j=1:K
            test = (indices == j); 
            train = ~test;
            
            clf.fit(X(train,:), y(train,:));
            
            y_hat  = clf.predict(X(test,:));
            mse(i,j) = mean((y_hat - y(test,:)).^2);
            model_class();
        end
    end
    mean_mse = mean(mse,2);
    [~,best_i] = min(mean_mse);
    best_parameters = cell2struct(num2cell(parameter_combination(best_i,:)), parameter_names',2);
end