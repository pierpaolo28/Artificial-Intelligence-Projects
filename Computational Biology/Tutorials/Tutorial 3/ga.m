function av_n = ga(P,s,u,v,L,T)
  pop=zeros(L,P);  % initialise population
  av_n = zeros(T+1,1);
  cu = 1/log(1-u);  % mutation magic number
  cv = 1/log(1-v);  % mutation magic number
  hold on
  for t=0:T
    % compute fitness
    n = sum(pop); % number of ones in each member of the population
    av_n(t+1) = mean(n); 
    fitness = (1+s).^n;

    % plot distribution of one at sites
    if t>0
      plot(x,h,'red')
    end
    [h,x] = hist(sum(pop,2),[0:L]);
    h = h/L;
    plot(x,h)
    xlabel('Number of mutants, n')
    ylabel('P(n)')
    str = strcat('t= ', num2str(t));
    title(str)
    drawnow
    pause(0.1) %%% NB this slows you down so you can see the evolution
    
    % selection
    cum_fitness = cumsum(fitness);
    randindex = cum_fitness(P)*rand(P,1);  % roulette wheels
    newpop=zeros(L,P);
    for mu=1:P
      % using binary search
      lower = 1;
      upper = P;
      while lower<upper
	middle = floor((lower+upper)/2);
	if (randindex(mu)<cum_fitness(middle))
	  upper = middle;
	else
	  lower = middle+1;
	end
      end
      newpop(:,mu)=pop(:,upper);
    end

    % mutation using a fast but non-obvious algorithm
    % forward mutations 0-->1
    mutu = cumsum(floor(cu*log(rand(3*u*L*P,1))));
    for i=1:length(mutu)
      mu = floor(mutu(i)/L)+1;
      if (mu>P)
	break;
      end
      l = rem(mutu(i),L)+1;
      if newpop(l,mu)==0;
	newpop(l,mu)=1;
      end
    end
    % backward mutation 1-->0
    mutv = cumsum(floor(cv*log(rand(3*v*L*P,1))));
    for i=1:length(mutv)
      mu = floor(mutv(i)/L)+1;
      if (mu>P)
	break;
      end
      l = rem(mutv(i),L)+1;
      if newpop(l,mu)==1;
	newpop(l,mu)=0;
      end
    end
    
    % uniform crossover
    for mu=1:2:P-1
      mask=(rand(L,1)>0.5);
      pop(:,mu) = (mask&newpop(:,mu))|(~mask&newpop(:,mu+1));
      pop(:,mu+1) = (~mask&newpop(:,mu))|(mask&newpop(:,mu+1));
    end    
  end
  hold off
  % Show results
  plot(0:T,av_n)
  xlabel('Generations, t')
  ylabel('Average number of mutants, n')
