function markov(P, s, u, v, T)
  average = zeros(T,1);
  p = zeros(P+1,1);
  p(1) = 1;               % initialise probability distribution
  W = transition_matrix(P, s, u, v);
  x = 0:P;
  hold on;
  plot(x,p);
  for t = 1:T
    pause(0.2);
    plot(x,p,'red');
    average(t) = mean(x*p);
    p = W*p;
    plot(x,p);
    xlabel('Number of mutants, n');
    ylabel('P(n)');
    str = strcat('t= ', num2str(t));
    title(str);
    drawnow;
  end
  hold off
  xlabel('Generations, t')
  ylabel('Average number of mutants, n')
  plot([1:T], average)