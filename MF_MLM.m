classdef MF_MLM < MLM
    %MLM Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
    end
    
    methods
        function obj = MF_MLM(parameters)
            obj@MLM(parameters);
        end
        function obj = fit(obj, X, y)
            obj = obj.get_training_set(X,y);
            
            D_in  = pdist2(X, X);
            D_out = pdist2(y, y);
            
            % step 1 RP_in pruning
            [B, gamma_ind, ~, ~] = MFOCUSS(D_in, D_out,...
                                            obj.parameters.lambda,...
                                            'p',obj.parameters.p);
            obj.parameters.B            = B(gamma_ind,:);
            obj.parameters.rp_index_in  = gamma_ind;
            obj.parameters.rp_index_out = 1:size(X,1);
        end
%         function cost = in_cost(obj, y, d_out_hat)
%             d_out = pdist2(y, obj.training_set.y(obj.parameters.rp_index,:));
%             cost = d_out.^2 - d_out_hat.^2;
%         end
%         function y_hat = predict(obj,X)
%             N         = size(X,1);
%             y_hat     = zeros(N,1);
%             X_rp      = obj.training_set.X(obj.parameters.rp_index,:);
%             D_in      = pdist2(X, X_rp);
%             D_out_hat = D_in * obj.parameters.B;
%             y_mean    = mean(obj.training_set.y(obj.parameters.rp_index,:));
%             
%             for i=1:N
%                 d_out_hat  = D_out_hat(i,:);
%                 J          = @(y) obj.in_cost(y, d_out_hat);
%                 options    = optimoptions('lsqnonlin','Display','off');
%                 y_hat(i,1) = lsqnonlin(J,y_mean,[],[],options);
%             end
%         end
%         function plot(obj)
%             obj.plot@Regressor(100);
%             hold on;
%             plot(obj.training_set.X(obj.parameters.rp_index_in,:), ...
%                  obj.training_set.y(obj.parameters.rp_index_in,:),...
%                  'ko','MarkerSize',10);
%             hold off;
%         end
    end
end

