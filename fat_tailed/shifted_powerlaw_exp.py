from .base_distribution import distribution
import numpy as np
from scipy.optimize import minimize


class shifted_powerlaw_exp(distribution):

    def __init__(self):
        super(shifted_powerlaw_exp, self).__init__()
        self.name = 'shifted power law with exp cutoff'
        self.n_para = 4

    def _loglikelihood(self, alpha_lambda_delta_beta, xmin, freq, N):
        alpha, lambda_, delta, beta = alpha_lambda_delta_beta
        delta = delta * xmin
        beta = beta * self.xmax
        sumlog = np.sum(freq[:, -1] * np.log(freq[:, 0] - delta))
        sumlogdem = np.sum(
            freq[:, -1] * np.log(1 + np.exp((freq[:, 0] - beta) * lambda_)))
        xi = np.arange(xmin, self.xmax)
        norm = np.sum((xi - delta)**(-alpha) / (1 + np.exp((xi - beta) *
                                                           lambda_)))
        xi = np.arange(self.xmax, 2e7)
        norm += np.sum((xi - delta) ** (-alpha) * np.exp((beta - xi) *
                                                         lambda_))
        logll = -alpha * sumlog - sumlogdem - N * np.log(norm)
        return -logll

    def _fitting(self, xmin=1):
        freq = self.freq[self.freq[:, 0] >= xmin]
        N = np.sum(freq[:, -1])
        if xmin not in self.N_xmin:
            self.N_xmin[xmin] = N

        res = minimize(self._loglikelihood, x0=(1.27, 3e-05, 0.5, 0.2),
                       method='L-BFGS-B', tol=1e-10,
                       args=(xmin, freq, N),
                       bounds=((0.5, 3), (1e-6, 1e-3), (1e-15, 1. - 1e-2),
                               (xmin / self.xmax, 0.5)))

        aic = 2 * res.fun + 2 * self.n_para
        fits = {}
        fits['alpha'] = res.x[0]
        fits['lambda'] = res.x[1]
        fits['delta'] = res.x[2] * xmin
        fits['beta'] = res.x[3] * self.xmax
        return (res.x[0], -res.fun, aic), fits

    def _get_ccdf(self, xmin):

        alpha = self.fitting_res[xmin][1]['alpha']
        lambda_ = self.fitting_res[xmin][1]['lambda']
        delta = self.fitting_res[xmin][1]['delta']
        beta = self.fitting_res[xmin][1]['beta']

        total, ccdf = 1., []
        xi = np.arange(xmin, self.xmax)
        norm = np.sum((xi - delta)**(-alpha) / (
            1 + np.exp((xi - beta) * lambda_)))
        xi = np.arange(self.xmax, 2e7)
        norm += np.sum((xi - delta) ** (-alpha) * np.exp((beta - xi) *
                                                         lambda_))
        for x in range(xmin, self.xmax):
            total -= (x - delta)**(-alpha) / norm / (
                1 + np.exp((x - beta) * lambda_))
            ccdf.append([x, total])

        return np.asarray(ccdf)
