a = 6.022140857*(10^(23))

k1 = 1
k2 = 2
k3 = 0.02
k4 = 0.04

syms y(t)
syms x(t)
ode = diff(y,t) == (k2*x - k3*y*(x^2))
cond = y(0) == 0
cond2 = x(0) == 0
ySol(t) = dsolve(ode,cond, cond2)

time = 0:1:500;

sol = ySol(time)

plot(time, sol)

syms x(t)
syms y(t)
ode = diff(x,t) == (x - k4*x -k2*y + k3*y*(x^2))
cond = x(0) == 0
cond2 = y(0) == 0
xSol(t) = dsolve(ode,cond, cond2)

time = 0:1:500;

sol2 = xSol(time)

hold on
plot(time, sol2)

% syms o(t)
% ode = diff(o,t) == -o -0.04
% cond = o(0) == 0
% oSol(t) = dsolve(ode,cond)
% 
% time = 0:1:500;
% 
% sol3 = oSol(time)
% 
% hold on
% plot(time, sol3)

