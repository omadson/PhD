function [best_parameters] = cross_kfold(model_class, parameters, folds, dataset)
    X = dataset(:,1:end-1);
    y = dataset(:,end);
    
    %% create all combinations of parameters
    parameter_names = fieldnames(parameters);
    if length(fieldnames(parameters)) > 1
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
%         fprintf('\n        - ');
%         for j=1:length(parameter_names)
%             fprintf('%s: %f, ',parameter_names{j}, eval(sprintf('parameters_.%s',parameter_names{j})));
%         end
%         fprintf(' | fold: ');
        %% K-fold LOOP
        for k=1:length(folds)
%             fprintf('%d, ', k);

            clf = eval(sprintf('%s(parameters_);',model_class));
            
            
            X_train = X(folds{k}.train,:);
            max_x = repmat(max(X_train),size(X_train,1),1);
            min_x = repmat(min(X_train),size(X_train,1),1);
            
            X_test = X(folds{k}.test,:);
            
            max_x_test = repmat(max(X_train),size(X_test,1),1);
            min_x_test = repmat(min(X_train),size(X_test,1),1);
            % normalize X_train and X_test
            X_train = (X_train - min_x) ./ (max_x - min_x);
            X_test = (X_test - min_x_test) ./ (max_x_test - min_x_test);
            
            
            y_train = y(folds{k}.train,:);
            max_y = max(y_train);
            min_y = min(y_train);
            y_train = (y_train - min_y) ./ (max_y-min_y);
            
            
            
            
            y_test = y(folds{k}.test,:);
            try
                clf.fit(X_train, y_train);
            catch exception
                parameters_
            end
            y_hat  = (clf.predict(X_test) .* (max_y - min_y)) + min_y;
            mse(i,k) = mean((y_hat - y_test).^2);
        end
%         fprintf(' (mse=%.3f), ', mean(mse(i,:)));
    end
    mean_mse = mean(mse,2);
    
    [~,best_i] = min(mean_mse);
    
    best_parameters = cell2struct(num2cell(parameter_combination(best_i,:)), parameter_names',2);
end