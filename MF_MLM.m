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
            
            D_in  = phi(X, X);
            D_out = phi(y, y);
            
            % step 1 RP_in pruning
            [B, gamma_ind, ~, ~] = MFOCUSS(D_in, D_out,...
                                            obj.parameters.lambda,...
                                            'p',obj.parameters.p);
            
            % RP selection method 
            if obj.parameters.selection_type == 1     % MF-MF
                obj.parameters.rp_index_in  = gamma_ind;
                obj.parameters.rp_index_out = gamma_ind;
                obj.parameters.B            = B(gamma_ind,gamma_ind);
            elseif obj.parameters.selection_type == 2 % MF-FL
                obj.parameters.rp_index_in  = gamma_ind;
                obj.parameters.rp_index_out = 1:size(X,1);
                obj.parameters.B            = B(gamma_ind,:);
            else                       % MF-MF
                obj.parameters.rp_index_in  = gamma_ind;
                obj.parameters.rp_index_out = gamma_ind;
                obj.parameters.B            = B(gamma_ind,gamma_ind);
            end
            
            
        end
    end
end

