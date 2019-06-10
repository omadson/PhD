classdef Data < handle
    %Regressor main class to create Regressors
    
    properties
        parameters    % Struct with all regressor parameters
        sets          % Struct with the datasets
    end
    
    methods
%         function obj = Data(varargin)
%             if isempty(varargin{1})
%                 obj.parameters = struct();
%             elseif length(varargin) == 1
%                 obj.parameters = varargin{1};
%             else
%                 fprintf("Error, wrong arguments length.");
%             end
%         end
        function obj = load(obj, data_path)
            obj.sets.all = load(data_path);
        end
        function obj = normalize(obj)
            data_mean = mean(obj.sets.all(:,1:end-1));
            data_std  = std(obj.sets.all(:,1:end-1));
            obj.sets.all(:,1:end-1) = (obj.sets.all(:,1:end-1) - data_mean)./ data_std;
        end
        function obj = shuffle(obj)
            obj.sets.all = obj.sets.all(randperm(size(obj.sets.all,1)),:);
        end
        function obj = divide(obj, prop)
            M = size(obj.sets.all,1);
            train_index = ceil(prop * M);
            obj.sets.train.X = obj.sets.all(1:train_index,1:end-1);
            obj.sets.test.X  = obj.sets.all(train_index+1:end,1:end-1);
            
            obj.sets.train.y = obj.sets.all(1:train_index,end);
            obj.sets.test.y  = obj.sets.all(train_index+1:end,end);
        end
    end
end

