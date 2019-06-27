function av_n = multisim(P, s, u, v, NoCopies, T)
  n = zeros(NoCopies,1);
  average = zeros(T+1,1);
  clf
  hold on
  for t=0:T
    % plot distribution
    av_n(t+1) = mean(n);
    if (t>0)
      plot(x,h,'red')
    end
    [h,x] = hist(n,[0:P]);
    h = h/NoCopies;
    plot(x,h)
    xlabel('Number of mutants, n')
    ylabel('P(n)')
    str = strcat('t= ', num2str(t));
    title(str)
    drawnow

    % selection
    p_s = (1+s)*n./(P+s*n);
    % mutations
    p_sm = (1-v)*p_s + u*(1.0-p_s);
    % sampling
    t = t + 1;
    for i=1:NoCopies
      n(i) = binomial_rnd(P, p_sm(i));
    end
  end
  % plot average
  hold off
  plot([0:T], av_n)
  xlabel('Generations, t')
  ylabel('Average number of mutants, n')

