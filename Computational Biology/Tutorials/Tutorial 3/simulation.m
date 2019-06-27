function simulation(P, s, u, v)
  t = 1;
  n(t) = 0;   % initialise number of mutants in population
  while (n(t)<P+1  & t<200)
    % selection
    p_s = (1+s)*n(t)/(P+s*n(t));
    % mutations
    p_sm = (1-v)*p_s + u*(1.0-p_s);
    % sampling
    t = t + 1;
    n(t) = binomial_rnd(P, p_sm);
  end
  plot([1:t], n)
  % graceplot([1:t], n)
  xlabel('Generations, t')
  ylabel('Number of mutants')
  %z = [[1:t]',n'];
  %save -ascii "simulation.dat" z
