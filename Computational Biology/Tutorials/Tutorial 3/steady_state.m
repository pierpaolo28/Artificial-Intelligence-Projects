function steady_state(P,s,u,v)
  global sg;
  global vg;
  global ug;
  global Pg;
  Pg = P;
  vg = v;
  ug = u;
  sg = s;
  x = 0:1/P:1;
  y = zeros(size([0:1/P:1]));
  i=2;
  
  % Using Gauss-Legendre to perform integration
  xtab = zeros(1,8);
  xtab(1) = 0.0198550718;
  xtab(2) = 0.1016667613;
  xtab(3) = 0.2372337950;
  xtab(4) = 0.4082826788;
  xtab(5) = 0.5917173212;
  xtab(6) = 0.7627662050;
  xtab(7) = 0.8983332387;
  xtab(8) = 0.9801449282;
  weight = zeros(8,1);
  weight(1) = 0.0506142681;
  weight(2) = 0.1111905172;
  weight(3) = 0.1568533229;
  weight(4) = 0.1813418917;
  weight(5) = 0.1813418917;
  weight(6) = 0.1568533229;
  weight(7) = 0.1111905172;
  weight(8) = 0.0506142681;

  for xx = x
    if (xx==0) | (xx==1)
      y(i) = 0;
    else
      p_sm = ((1-vg)*(1+sg)*xx + ug*(1-xx))/(1+sg*xx);
      bsq = p_sm*(1-p_sm)/Pg;
      z = zeros(1,8);
      j = 1;
      xval = (xx-0.5)*xtab+0.5;
      for xxx = xval
	z(j) = integrand(xxx);
	j = j+1;
      end
      y(i) = exp((xx-0.5)*(z*weight))/bsq;
      %     numerical integration is slow
      %     y(i) = exp(quad('integrand',0.5,xx,0.00001))/bsq; 
      i = i+1;
    end
  end
  y = y/sum(y);

  % Compute the leading eigenvector of the transition matrix
  W = transition_matrix(P,s,u,v);
  [V,L]=eig(W);
  % Use the approximate formula for the diffusion equation
  z=x.^(2*P*u-1).*(1-x).^(2*P*v-1).*exp(2*P*s*x);
  z = z/sum(z)
  % plot results
  plot(x,y,x,V(:,1)/sum(V(:,1)),x,z)
  legend('diffusion','markov','approximate diffusion')
