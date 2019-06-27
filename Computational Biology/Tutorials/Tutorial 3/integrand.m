function y=integrand(x)
  global sg;
  global vg;
  global ug;
  global Pg;
  p_sm = ((1-vg)*(1+sg)*x + ug*(1-x))/(1+sg*x);
  a = p_sm-x;
  bsq = p_sm*(1-p_sm)/Pg;
  y = 2*a/bsq;
