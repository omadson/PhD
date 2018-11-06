classdef GA_MLM < MLM
    %MLM Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
    end
    
    methods
        function obj = GA_MLM(varargin)
            if nargin == 0
                parameters = struct();
            else
                parameters = varargin{1};
            end
            obj@MLM(parameters);
        end
        function obj = fit(obj, X, y)
            obj = obj.get_training_set(X,y);

            D_in  = phi(X, X);
            D_out = phi(y, y);
            
            %% GA parameters
            generations     = ceil(20 * (obj.training_set.N + obj.training_set.D));
            population_size = ceil(0.8 * (obj.training_set.N));
            
            %% Points used for the distance-based regression
            gaoptions = gaoptimset('PopulationType','bitstring',...
                                   'Generations',generations,...
                                   'PopulationSize',population_size,...
                                   'UseParallel','always','Vectorized','on',...
                                   'StallGenLimit',80,...
                                   'Generations',200,...
                                   'CrossoverFcn',@crossoversinglepoint,...
                                   'MutationFcn', {@mutationuniform, 1/4},...
                                   'CreationFcn',@myInitialpopulation,...
                                   'PlotFcn', {@gaplotbestf,@gaplotbestindiv});
            
            fitnessFunction = @(individuals) fitness_ga_mlm(individuals, D_in, D_out, obj.parameters.lambda);
            
            [finalIndividual] = ga(fitnessFunction, obj.training_set.N, gaoptions);
            
            obj.parameters.rp_index_in  = find(finalIndividual == 1);
            obj.parameters.rp_index_out = 1:obj.training_set.N;
            obj.parameters.B            = pinv(D_in(:,obj.parameters.rp_index_in)) * D_out;
        end
    end
end

