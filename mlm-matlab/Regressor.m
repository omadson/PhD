classdef Regressor < handle
    %Regressor main class to create Regressors
    
    properties
        parameters    % Struct with all regressor parameters
        metrics       % Struct with all regressor information
        training_set  % Struct with the dataset used on the fit phase
    end
    
    methods
        function obj = Regressor(varargin)
            if isempty(varargin{1})
                obj.parameters = struct();
            elseif length(varargin) == 1
                obj.parameters = varargin{1};
            else
                fprintf("Error, wrong arguments length.");
            end
            obj.metrics      = struct('fit_time', 0,...
                                      'predict_time', 0,...
                                      'mse_train', 0);
            obj.training_set = struct('X', [],...
                                      'y', []);
        end
        function obj = get_training_set(obj, X, y)
            [obj.training_set.N, obj.training_set.D] = size(X);
            obj.training_set.X = X;
            obj.training_set.y = y;
        end
        function obj = fit(obj, X, y)
            obj = obj.get_training_set(X,y);
            
            obj.parameters.w = pinv([ones(obj.training_set.N,1) X]) * y;
        end
        function y_hat = predict(obj, X)
            N = size(X,1);
            y_hat = [ones(N,1) X] * obj.parameters.w;
        end
        function plot(obj,varargin)
            if nargin < 2
                divisions = 500;
            else
                divisions = varargin{1};
            end
            X_min  = min(obj.training_set.X);
            X_max  = max(obj.training_set.X);
            X_grid = [X_min:(X_max - X_min)/divisions:X_max]';
            y_hat = obj.predict(X_grid);
            plot(obj.training_set.X, obj.training_set.y, '.',...
                 X_grid, y_hat,'-');
            xlabel('$x$');
            ylabel('$y$');
            legend({'data points', 'approximation'});
        end
    end
end

