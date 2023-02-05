import numpy as np

from flask_cors import CORS
from scipy.optimize import minimize
from flask import Flask, request, render_template


app = Flask(__name__)
CORS(app)


class Portfolio:
    def __init__(self, cash, assets, selling_allowed=False):
        self._cash = cash
        self._assets = assets
        self._selling_allowed = selling_allowed

    def portfolio_value(self):
        return self._cash + sum(self._assets.values())
    
    def sell_everything(self):
        for ticker, quantity in self._assets.items():
            self._cash += quantity
            self._assets[ticker] = 0

    @staticmethod
    def rebalance_objective(new_asset_values, current_asset_values, target_allocation, total_cash):
        # total asset value
        asset_vals = current_asset_values + new_asset_values
        tot_asset_val = np.sum(asset_vals)
        # compute current allocation
        current_allocation = asset_vals / tot_asset_val

        # Penalize asset allocation's far from target allocation (we use L2 norm)
        asset_alloc_diff = target_allocation - current_allocation
        j1 = np.inner(asset_alloc_diff, asset_alloc_diff)  # range: (0, 1)

        # Penalize unused cash (we use L2 norm)
        cash_diff = (total_cash -
                    np.sum(new_asset_values)) / (
                        total_cash +
                        np.sum(new_asset_values))
        j2 = cash_diff * cash_diff  # range: (0, 1)

        return j1 + j2

    def rebalance_optimizer(self, target_alloc_values):
        bound = (0.00, self._cash)
        bounds = ((bound, ) * len(self._assets))
        constraints = [{
            'type':
            'ineq',
            'fun':
            lambda new_asset_values: self._cash - np.sum(new_asset_values)
        }]  # Can't buy more than available cash

        current_asset_values = np.array([
            asset
            for asset in self._assets.values()
        ])
        new_asset_values0 = target_alloc_values / 100. * self.portfolio_value() - current_asset_values

        solution = minimize(self.rebalance_objective,
                            new_asset_values0,
                            args=(current_asset_values,
                                target_alloc_values / 100., 
                                self._cash),
                            method='SLSQP',
                            bounds=bounds,
                            constraints=constraints)

        return solution.x


# Define the default route for the web app
@app.route('/')
def index():
    return render_template("index.html", rebalanced_portfolio_data=[])

# Define the route for processing the portfolio rebalancing request
@app.route('/rebalance', methods=['POST'])
def rebalance_portfolio():
    # Get the portfolio data from the form
    cash = float(request.json.get("cash"))
    assets = dict(request.json.get("assets"))
    target_asset_alloc = dict(request.json.get("target_asset_alloc"))

    # convert the assets and target_asset_alloc values to float
    assets = {k: float(v) for k, v in assets.items()}
    target_asset_alloc = {k: float(v) for k, v in target_asset_alloc.items()}

    # Create a portfolio instance
    p = Portfolio(cash, assets)

    # If selling is allowed, sell everything first
    if p._selling_allowed:
        p.sell_everything()

    # Compute the target asset allocation values
    target_alloc_values = np.array([target_asset_alloc.get(asset, 0) for asset in p._assets.keys()], dtype=float)

    # Rebalance the portfolio
    to_buy_vals = p.rebalance_optimizer(target_alloc_values)
    p.remain_cash = p._cash - np.sum(to_buy_vals)
    p.alloc_diffs = target_alloc_values - (list(p._assets.values()) + to_buy_vals) / (p.portfolio_value()+p.remain_cash) * 100.

    # Generate the rebalanced portfolio data to display in the table
    rebalanced_portfolio_data = []
    for idx, (ticker, quantity, target_alloc, to_buy_val) in enumerate(zip(p._assets.keys(), p._assets.values(), target_alloc_values, to_buy_vals)):
        new_asset_amount = quantity + to_buy_val
        prev_asset_alloc = quantity / sum(p._assets.values()) * 100.
        rebalanced_portfolio_data.append({
            'ticker': ticker,
            'to_buy_val': f'{to_buy_val:.2f}',
            'new_asset_amount': f'{new_asset_amount:.2f}',
            'prev_asset_alloc': f'{prev_asset_alloc:.2f}',
            'target_alloc': f'{target_alloc:.2f}',
            'new_alloc': f'{target_alloc-p.alloc_diffs[idx]:.2f}',
            'alloc_diff': f'{p.alloc_diffs[idx]:.2f}',
        })

    # render the index.html template with the rebalanced portfolio data in request
    return rebalanced_portfolio_data