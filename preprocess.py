import numpy as np
import pandas as pd
import pandas_datareader as data
from datetime import datetime,timedelta,date

index_name_list = ['RELIANCE.NS','HDFCBANK.NS','ICICIBANK.NS','INFY.NS','HDFC.NS','TCS.NS','ITC.NS','KOTAKBANK.NS',
                'HINDUNILVR.NS','LT.NS','SBIN.NS','BHARTIARTL.NS','BAJFINANCE.NS','AXISBANK.NS','ASIANPAINT.NS',
                'M&M.NS','MARUTI.NS','TITAN.NS','SUNPHARMA.NS','BAJAJFINSV.NS','HCLTECH.NS','ADANIENT.NS','TATASTEEL.NS',
                'INDUSINDBK.NS','NTPC.NS','POWERGRID.NS','TATAMOTORS.NS','ULTRACEMCO.NS','NESTLEIND.NS','TECHM.NS',
                'GRASIM.NS','CIPLA.NS','JSWSTEEL.NS','ADANIPORTS.NS','WIPRO.NS','HINDALCO.NS','SBILIFE.NS','DRREDDY.NS',
                'EICHERMOT.NS','HDFCLIFE.NS','ONGC.NS','TATACONSUM.NS','DIVISLAB.NS','BAJAJ-AUTO.NS','BRITANNIA.NS',
                'APOLLOHOSP.NS','COALINDIA.NS','UPL.NS','HEROMOTOCO.NS','BPCL.NS']

def investment_detail(start,initial_investment,top_comp=[]):

    index_dict = dict()
    new_df = pd.read_csv('Nifty50.csv')
    for i,j in zip(new_df['Company Name'],index_name_list):
        index_dict[j] = i

    date_time_obj = datetime.strptime(start, '%Y-%m-%d') + timedelta(4)
    temp_end = date_time_obj.strftime('%Y-%m-%d')

# Finding Open Price and Close Price
    open_price = {}
    close_price = []
    if len(top_comp) != 0:
        for i in top_comp:
            price = data.DataReader(i,'yahoo',start,temp_end)
            open_price[i] = price['Open'][0]
            close_price.append(price['Close'][0])

    else:
        for i in index_dict.keys():
            price = data.DataReader(i,'yahoo',start,temp_end)
            open_price[i] = price['Open'][0]
            close_price.append(price['Close'][0])

    invested_detail = pd.DataFrame({'Companies':open_price.keys(),'Open Price':open_price.values(),'Close Price':close_price})
    
    if len(top_comp) != 0:
        equal_allocation = initial_investment/len(top_comp)
    else:
        equal_allocation = initial_investment/50

## stock selection by using initial amount
 
    mini_stock_price = min(list(open_price.values()))

    max_stock_price = max(list(open_price.values()))

    remaining_amt = 0
    qty_dict = dict()
    inv_amt = dict()
    for name,price in open_price.items():

        if (equal_allocation+remaining_amt) >= mini_stock_price:
            qty = (equal_allocation+remaining_amt)//price
            qty_dict[name] = qty
            new_amt = qty*price
            inv_amt[name] = new_amt
            remaining_amt = (equal_allocation+remaining_amt)-new_amt

            
    ## stock selection by using remaining amount

    keys = list(open_price.keys())
    val = list(open_price.values())

    temp_stock_price = [i for i in val if i < remaining_amt]

    if len(temp_stock_price)>0:
        
        temp_stock_price.sort()

        while remaining_amt > temp_stock_price[0]:
            
            for mini_stock_price in temp_stock_price:
                
                if remaining_amt >= mini_stock_price:
                    index = keys[val.index(mini_stock_price)]
                    qty = remaining_amt//mini_stock_price
                    qty_dict[index] += qty
                    new_amt = qty*mini_stock_price
                    inv_amt[index] += new_amt
                    remaining_amt -=new_amt

    invested_detail['Quantity'] = list(qty_dict.values())
    invested_detail['Invested Amount'] = list(inv_amt.values())
    total_invested_amt = sum(list(inv_amt.values()))

    return remaining_amt,total_invested_amt,invested_detail


def find_top_stocks(start,n_days_measure_perf,top_n_stocks):

    # Finding Prior Date

    previous_date = datetime.strptime(start, '%Y-%m-%d') - timedelta(n_days_measure_perf)
    previous_date = previous_date.strftime('%Y-%m-%d')

    n_days_data = data.DataReader('RELIANCE.NS','yahoo',previous_date,start)
    n_days_data

    day=0

    while n_days_data.shape[0] != (n_days_measure_perf+1):
        
        day += ((n_days_measure_perf+1)-n_days_data.shape[0])
        
        previous_date = datetime.strptime(start, '%Y-%m-%d') - timedelta(day)
        previous_date = previous_date.strftime('%Y-%m-%d')
        
        n_days_data = data.DataReader('RELIANCE.NS','yahoo',previous_date,start)
        n_days_data
        
    start_included = False
    if start in n_days_data.index:
        start_included = True
        
    ## Finding close price of stocks
    close_price = {}
    if start_included:
        for com in index_name_list:
            n_day_data = data.DataReader(com,'yahoo',previous_date,start)
            close_price[com] = (n_day_data['Close'][0],n_day_data['Close'][-2])
    else:
        for com in index_name_list:
            n_day_data = data.DataReader(com,'yahoo',previous_date,start)
            close_price[com] = (n_day_data['Close'][0],n_day_data['Close'][-1])
    
    previous_price = [i[0] for i in close_price.values()]
    latest_price = [i[1] for i in close_price.values()]

    stock_performance = pd.DataFrame({"Company":close_price.keys(),"{} day before last day Price".format(n_days_measure_perf):previous_price,"last day Price":latest_price})

    stock_performance['Return (%)'] = ((stock_performance['last day Price']/stock_performance["{} day before last day Price".format(n_days_measure_perf)])-1)*100

    sorted_returns = sorted(stock_performance['Return (%)'],reverse=True)
    top_companies = {}

    if top_n_stocks <= 50:
        for val in sorted_returns[0:top_n_stocks]:
            index = list(stock_performance['Return (%)']).index(val)
            company = stock_performance['Company'][index]
            top_companies[company] = val
    
    selected_companies = ''.join(top_companies.keys()).split('.NS')[:-1]

    return stock_performance,selected_companies,top_companies
        

def find_equity_curve(start,end,invested_detail):

    daily_value = pd.DataFrame()

    for comp,qty in zip(invested_detail['Companies'],invested_detail['Quantity']):
        temp = data.DataReader(comp,'yahoo',start,end)
        daily_value[comp] = list(temp['Close']*qty)

    daily_value.insert(0,column='Date',value=temp.index)

    equity_curve = []
    for i in range(len(daily_value)):
        equity_curve.append(sum(daily_value.iloc[i][1:]))

    date_list = [x.strftime('%Y-%m-%d') for x in daily_value['Date'] ]

    equity_curve_df = pd.DataFrame({'Date':date_list,'Equity Curve':equity_curve})

    return equity_curve_df


def nifty_curve(start,end,investment_amount):

    # Finding Quantity

    nifty50_data = data.DataReader('^NSEI','yahoo',start,end)
    nifty50_data = nifty50_data.reset_index()
    nifty50_data = nifty50_data[['Date','Open','Close']]
    close_price = nifty50_data['Close'][0]
    open_price = nifty50_data['Open'][0]

    qty = investment_amount//open_price
    invested_amount = open_price*qty
    remaining_amount = investment_amount - invested_amount

    # Finding equity Curve List

    equity_curve = list(nifty50_data['Close']*qty)

    date_list = [x.strftime('%Y-%m-%d') for x in nifty50_data['Date'] ]

    equity_curve_df = pd.DataFrame({'Date':date_list,'Equity Curve':equity_curve})

    return equity_curve_df,invested_amount


def cagr(start_value, end_value, num_periods):
    return ((end_value / start_value) ** (1 / (num_periods - 1)) - 1)*num_periods*100

