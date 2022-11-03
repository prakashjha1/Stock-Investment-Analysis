# Stock-Investment-Analysis

### Objective Of this Project
#### 1. Create a benchmark strategy

Our Benchmark is going to be simple and basic, we are going to invest our initial investment equally
among all the 50 stocks during the beginning of the simulation and hold it till the end and get the
portfolio equity curve.

Note:
1. Buy on Open on day 1
2. Daily Value of Stock is Close X Qty
3. Equity Curve is sum of daily value of all stocks

#### 2. Create a strategy to beat the benchmark

Instead of investing in all the 50 stocks, let us select a few based on their performance in the past.

I.Take the prices till one day prior to investment day (Simulation Start Date)

II.Measure the performance of the latest 100 days, in terms of percentage returns
(Close (last day) / Close (100th day before last day) - 1)

III.Select the top 10 best performing stocks (i.e., the ones that have the best returns)
Invest the Initial Investment equally among the 10 stocks during the beginning of the simulation and
hold it till the end and get the portfolio equity curve.

#### 3. Create the equity curve for nifty index

Find the equity curve for Nifty index for the simulation period using the same initial investment value.

### Python Modules used in this project
- numpy 
- pandas 
- pandas_datareader 
- datetime 
- matplotlib.pyplot 
- streamlit 
- time
- concurrent.futures

### Need to take the following as inputs:
1. Start date and end date of simulation
2. Number of days to measure the performance for stock selection required for the sample strategy
3. Number of top stocks to be selected for sample strategy
4. Initial Equity

### Need to display the following:
1. Equity Curves of Nifty index, benchmark and the Sample strategy for the given period in a single plot
2. Stocks that are selected for the sample strategy

### Link of this project

https://investment-analysis-prakashjha.herokuapp.com/
