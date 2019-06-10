classdef MF_MLM < MLM
    %MLM Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
    end
    
    methods
        function obj = MF_MLM(varargin)
            if nargin == 0
                parameters = struct();
            else
                parameters = varargin{1};
            end
            obj@MLM(parameters);
        end
        function obj = fit(obj, X, y)
            %% test and fix parameters
            % p-norm
            if ~isfield(obj.parameters, 'd')
                obj.parameters.d = 0.8;
            else
                if obj.parameters.d > 1
                    obj.parameters.d = 1; 
                elseif obj.parameters.d < 0
                    obj.parameters.d = 0;
                end
            end
            
            
            % regularization parameter (lambda)
            if ~isfield(obj.parameters, 'lambda')
                obj.parameters.lambda = 10e-5;
            else
                if obj.parameters.lambda < 0
                    obj.parameters.d = 10e-9;
                end
            end
            
            % selection type parameter
            if ~isfield(obj.parameters, 'selection_type')
                obj.parameters.selection_type = 1;
            elseif obj.parameters.selection_type ~= 1 &&...
                   obj.parameters.selection_type ~= 2
                obj.parameters.selection_type = 1;
            end
            
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
                obj.parameters.rp_index_out = 1:obj.training_set.N;
                obj.parameters.B            = B(gamma_ind,:);
            end
        end
    end
end

