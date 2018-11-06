function Population = myInitialpopulation(GenomeLength, FitnessFcn, options)
    % generate individuals with zero values
    totalPopulation = sum(options.PopulationSize);
    
    Population = rand(totalPopulation,GenomeLength) > 0.5;
end