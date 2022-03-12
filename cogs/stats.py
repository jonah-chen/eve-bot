import nextcord
from nextcord.ext import commands
import numpy as np
import random

class Stats(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=['sample', 'realization'])
    async def realize(self, ctx, *, msg):
        if msg == 'help':
            await ctx.send("**Available distributions:**uniform, normal, poisson, binomial, geometric, negative_binomial, hypergeometric, beta, gamma, chisquare, f, t, pareto")
            await ctx.send("Usage: `realize <distribution> <parameters (comma seperated)>`")
            return

        try:
            # Split the message into the distribution and the parameters
            dist, params_str = msg.lower().split(' ', 1)
            # purge whitespace from param_str
            params_str = params_str.replace(' ', '')
            params = dict()
            for param in params_str.split(','):
                splitted = param.split('=')
                if len(splitted) == 2:
                    params[splitted[0]] = float(splitted[1])
                else:
                    await ctx.send(f"Invalid parameter: `{param}`")
            if not params:
                await ctx.send("No parameters specified")
                return

            if 'uniform' in dist.lower():
                # Uniform distribution
                if 'low' in params and 'high' in params:
                    low = params['low']
                    high = params['high']
                    await ctx.send(str(random.uniform(low, high)))
                elif 'a' in params and 'b' in params:
                    a = params['a']
                    b = params['b']
                    await ctx.send(str(random.uniform(a, b)))
                elif 'min' in params and 'max' in params:
                    min_ = params['min']
                    max_ = params['max']
                    await ctx.send(str(random.uniform(min_, max_)))
                else:
                    await ctx.send("Invalid parameters for uniform distribution: " + 
                        "Only `low,high`, `a,b`, and `min,max` are valid parameters.")
            elif 'normal' in dist.lower():
                # Normal distribution
                if 'mean' in params and 'stdev' in params:
                    mean = params['mean']
                    stdev = params['stdev']
                    await ctx.send(str(random.gauss(mean, stdev)))
                elif 'mu' in params and 'sigma' in params:
                    mu = params['mu']
                    sigma = params['sigma']
                    await ctx.send(str(random.gauss(mu, sigma)))
                elif 'z' in params and 's' in params:
                    z = params['z']
                    s = params['s']
                    await ctx.send(str(random.gauss(z, s)))
                else:
                    await ctx.send("Invalid parameters for normal distribution: " + 
                        "Only `mean,stdev`, `mu,sigma`, and `z,s` are valid parameters.")
            elif 'poisson' in dist.lower():
                # Poisson distribution
                if 'lambda' in params:
                    lam = params['lambda']
                    await ctx.send(str(np.random.poisson(lam)))
                elif 'rt' in params:
                    rt = params['rt']
                    await ctx.send(str(np.random.poisson(rt)))
                elif 'r' in params and 't' in params:
                    rt = params['r'] * params['t']
                    await ctx.send(str(np.random.poisson(rt)))
                else:
                    await ctx.send("Invalid parameters for poisson distribution: " + 
                        "Only `lambda` and `rt` are valid parameters.")
            elif 'binomial' in dist.lower():
                if 'n' in params and 'p' in params:
                    n = int(params['n'])
                    p = params['p']
                    await ctx.send(str(np.random.binomial(n, p)))
                else:
                    await ctx.send("Invalid parameters for binomial distribution: " + 
                        "Only `n,p` are valid parameters.")
            elif 'geometric' in dist.lower():
                if 'p' in params:
                    p = params['p']
                    await ctx.send(str(np.random.geometric(p)))
                else: # when distribution have only one parameter
                    p = list(params.values())[0]
                    await ctx.send(str(np.random.geometric(p)))
            elif 'hypergeometric' in dist.lower():
                if 'good' in params and 'bad' in params and 'total' in params:
                    good = int(params['good'])
                    bad = int(params['bad'])
                    total = int(params['total'])
                    await ctx.send(str(np.random.hypergeometric(good, bad, total)))
                elif 'g' in params and 'b' in params and 'n' in params:
                    g = int(params['g'])
                    b = int(params['b'])
                    n = int(params['n'])
                    await ctx.send(str(np.random.hypergeometric(g, b, n)))
                elif 'n' in params and 'k' in params and 'samples' in params:
                    n = int(params['n'])
                    k = int(params['k'])
                    samples = int(params['samples'])
                    await ctx.send(str(np.random.hypergeometric(k, samples-k, n)))
                else:
                    await ctx.send("Invalid parameters for hypergeometric distribution: " + 
                        "Only `good,bad,total`, `g,b,n`, and `n,k,samples` are valid parameters.")
            elif 'exponential' in dist.lower():
                if 'lambda' in params:
                    lam = params['lambda']
                    await ctx.send(str(np.random.exponential(lam)))
                else:
                    lam = list(params.values())[0]
                    await ctx.send(str(np.random.exponential(lam)))
            elif 'lognormal' in dist.lower():
                if 'mu' in params and 'sigma' in params:
                    mu = params['mu']
                    sigma = params['sigma']
                    await ctx.send(str(np.random.lognormal(mu, sigma)))
                elif 'z' in params and 's' in params:
                    z = params['z']
                    s = params['s']
                    await ctx.send(str(np.random.lognormal(z, s)))
                elif 'mean' in params and 'stdev' in params:
                    mean = params['mean']
                    stdev = params['stdev']
                    await ctx.send(str(np.random.lognormal(mean, stdev)))
                else:
                    await ctx.send("Invalid parameters for lognormal distribution: " + 
                        "Only `mu,sigma` and `z,s` are valid parameters.")
            elif 'chisquare' in dist.lower():
                if 'df' in params:
                    df = params['df']
                    await ctx.send(str(np.random.chisquare(df)))
                else:
                    df = list(params.values())[0]
                    await ctx.send(str(np.random.chisquare(df)))
            elif 'f'==dist.lower():
                if 'dfn' in params and 'dfd' in params:
                    dfn = params['dfn']
                    dfd = params['dfd']
                    await ctx.send(str(np.random.f(dfn, dfd)))
                else:
                    await ctx.send("Invalid parameters for f distribution: " + 
                        "Only `dfn,dfd` are valid parameters.")
            elif 'gamma' in dist.lower():
                if 'shape' in params and 'scale' in params:
                    shape = params['shape']
                    scale = params['scale']
                    await ctx.send(str(np.random.gamma(shape, scale)))
                elif 'a' in params and 'b' in params:
                    a = params['a']
                    b = params['b']
                    await ctx.send(str(np.random.gamma(a, b)))
                elif 'alpha' in params and 'beta' in params:
                    alpha = params['alpha']
                    beta = params['beta']
                    await ctx.send(str(np.random.gamma(alpha, beta)))
                else:
                    await ctx.send("Invalid parameters for gamma distribution: " + 
                        "Only `shape,scale`, `a,b`, and `alpha,beta` are valid parameters.")
            elif 'beta' in dist.lower():
                if 'alpha' in params and 'beta' in params:
                    alpha = params['alpha']
                    beta = params['beta']
                    await ctx.send(str(np.random.beta(alpha, beta)))
                else:
                    await ctx.send("Invalid parameters for beta distribution: " + 
                        "Only `alpha,beta` are valid parameters.")
            elif 'pareto' in dist.lower():
                if 'a' in params and 'b' in params:
                    a = params['a']
                    b = params['b']
                    await ctx.send(str(np.random.pareto(a, b)))
                elif 'xm' in params and 'alpha' in params:
                    xm = params['xm']
                    alpha = params['alpha']
                    await ctx.send(str(np.random.pareto(xm, alpha)))
                elif 'shape' in params and 'scale' in params:
                    shape = params['shape']
                    scale = params['scale']
                    await ctx.send(str(np.random.pareto(shape, scale)))
                else:
                    await ctx.send("Invalid parameters for pareto distribution: " + 
                        "Only `a,b`, `xm,alpha`, and `shape,scale` are valid parameters.")
            elif 't'==dist.lower():
                if 'nu' in params:
                    nu = params['nu']
                    await ctx.send(str(np.random.standard_t('nu')))
                else:
                    nu = list(params.values())[0]
                    await ctx.send(str(np.random.standard_t(nu)))
            elif 'negative_binomial' in dist.lower():
                if 'n' in params and 'p' in params:
                    n = params['n']
                    p = params['p']
                    await ctx.send(str(np.random.negative_binomial(n, p)))
                else:
                    await ctx.send("Invalid parameters for negative_binomial distribution: " + 
                        "Only `n,p` are valid parameters.")
        except ValueError as e:
            await ctx.send("Invalid parameters: " + str(e))
        except Exception as e:
            await ctx.send("Error: " + str(e))


def setup(client):
    client.add_cog(Stats(client))