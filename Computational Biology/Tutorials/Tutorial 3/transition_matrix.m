function W = transition_matrix(P, s, u, v)
  W = zeros(P+1,P+1);
  for n = 0:P
    p_sm = ((1-v)*(1+s)*n + u*(P-n))/(P+s*n);
    lp = log(p_sm);
    lq = log(1.0-p_sm);
    x = P*lq;
    for np = 0:P
      W(np+1,n+1) = exp(x);
      x = x + lp - lq + log((P-np)/(np+1));
    end
  end
