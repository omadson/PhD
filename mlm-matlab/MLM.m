classdef MLM < Regressor
    %MLM Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
    end
    
    methods
        function obj = MLM(varargin)
            if nargin == 0
                parameters = struct();
            else
                parameters = varargin{1};
            end
            obj@Regressor(parameters);
        end
        function obj = fit(obj, X, y)
            % test and fix parameters
            if ~isfield(obj.parameters, 'selection_type') && ...
               ~isfield(obj.parameters, 'M')
                obj.parameters.selection_type = 4;
            elseif ~isfield(obj.parameters, 'selection_type') && ...
                    isfield(obj.parameters, 'M')
                obj.parameters.selection_type = 1;
            elseif  isfield(obj.parameters, 'selection_type') && ...
                   ~isfield(obj.parameters, 'M')
                 fprintf('The M parameter is necessary.\n');
            end
            
            
            obj = obj.get_training_set(X,y);
            
            % full in / full out
            if obj.parameters.selection_type == 4
                obj.parameters.rp_index_in  = 1:obj.training_set.N;
                obj.parameters.rp_index_out = 1:obj.training_set.N;
            else
                % convert percentage value to integer value
                if obj.parameters.M < 1
                    obj.parameters.M = ceil(obj.parameters.M * obj.training_set.N);
                end
                % select randomly M points into dataset
                rp_index = randi(obj.training_set.N, [obj.parameters.M,1]);
                
                % random in / random out
                if obj.parameters.selection_type == 1
                    obj.parameters.rp_index_in  = rp_index;
                    obj.parameters.rp_index_out = rp_index;
                    
                % random in / full out
                elseif obj.parameters.selection_type == 2
                    obj.parameters.rp_index_in  = rp_index;
                    obj.parameters.rp_index_out = 1:obj.training_set.N;
                    
                % full in / random out
                elseif obj.parameters.selection_type == 3
                    obj.parameters.rp_index_in  = 1:obj.training_set.N;
                    obj.parameters.rp_index_out = rp_index;
                end 
            end
             
            D_in  = phi(X, X(obj.parameters.rp_index_in,:));
            D_out = phi(y, y(obj.parameters.rp_index_out,:));
            
            obj.parameters.B = pinv(D_in) * D_out;
        end
        function cost = in_cost(obj, y, d_out_hat)
            d_out = phi(y, obj.training_set.y(obj.parameters.rp_index_out,:));
            cost = d_out.^2 - d_out_hat.^2;
        end
        function y_hat = predict(obj,X)
            N         = size(X,1);
            y_hat     = zeros(N,1);
            X_rp      = obj.training_set.X(obj.parameters.rp_index_in,:);
            D_in      = phi(X, X_rp);
            D_out_hat = D_in * obj.parameters.B;
            y_mean    = mean(obj.training_set.y(obj.parameters.rp_index_out,:));
            
            for i=1:N
                d_out_hat  = D_out_hat(i,:);
                J          = @(y) obj.in_cost(y, d_out_hat);
                options    = optimoptions('lsqnonlin','Display','off');
                y_hat(i,1) = lsqnonlin(J,y_mean,[],[],options);
            end
        end
        function plot(obj)
            obj.plot@Regressor(100);
            hold on;
            plot(obj.training_set.X(obj.parameters.rp_index_in,:), ...
                 obj.training_set.y(obj.parameters.rp_index_in,:),...
                 'ko','MarkerSize',10);
            hold off;
        end
    end
end

