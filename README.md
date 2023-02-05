# portfolio-rebalancer
A web-based app built with Flask to help you allocate your investments and restore balance to your portfolio.
## Overview
Portfolio Rebalancer is a Flask-based application that helps you optimize your investment portfolio by rebalancing it to the desired allocation you specify. It makes use of the scipy library's optimization algorithms to find the optimal distribution of assets in your portfolio.
## How to Use
You can use the app by visiting the default route ('/'), entering your portfolio details (including the amount of cash you have, the assets in your portfolio and their respective values, and your target asset allocation), and clicking the rebalance button. The app will then calculate the best way to allocate your investments to restore balance to your portfolio.
## Features
- Rebalancing: Portfolio Rebalancer calculates the best distribution of assets in your portfolio to bring it into line with your desired asset allocation.
- Optimization: The app uses scipy library's optimization algorithms to find the optimal distribution of assets.
- Easy to use: The app has a simple and intuitive user interface, making it easy for you to use.
## Requirements
- Flask
- NumPy
- SciPy
- Flask-Cors
## Running the app
To run the app, simply run the following command:
```
git clone https://github.com/fabioo29/portfolio-rebalancer.git
cd portfolio-rebalancer
pip install -r requirements.txt
python main.py
```
The app will then be available at `http://localhost:5000/`.
## Contributing
If you would like to contribute to this project, please feel free to fork the repository and submit a pull request.