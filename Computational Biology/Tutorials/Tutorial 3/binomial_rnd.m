function [M] = binomial_rnd(N,p,r,c)
%BINRAND Create random numbers from binomial distribution.
%
% USE:
% [output] = binrand(N,p,r,c),
%
% where N = the number of trial,
% p = the probability of success per trial,
% r = the number of rows of the output, and
% c = the numbe of columns of the output.
%
% If r and c are unspecified, they will be set = 1.

% Tomo Eguchi
% 23 January 2000

if (nargin < 2),
   error('Not enough input arguments.  It needs at least three.')
elseif (nargin > 4),
   error('Too many input arguments.  It needs at most five.')
elseif (nargin == 3),
   c = 1;
elseif (nargin == 2),
   r = 1; c = 1;
end

M = zeros(r,c);

for c1 = 1:N,
   M1 = zeros(r,c);
   y = rand(r,c);
   i1 = find(y < p);
   if (length(i1)~=0),
      M1(i1) = 1;
   end
   M = M + M1;
end
