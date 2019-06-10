function fitness = fitness_ga_mlm(individuals,D_in, D_out, lambda)
    for i=1:size(individuals,1)
        % set individual
        individual = individuals(i,:);
        
        % set distance matrix and 
        D = D_in(:,individual == 1);
        B_hat = pinv(D) * D_out;
        
        D_out_hat = D * B_hat;
        
        fitness(i) = lambda*sum(individual) + norm(D_out_hat - D_out,'fro');
    end
end