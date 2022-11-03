import numpy as np
import pandas as pd
import pandas_datareader as data
from datetime import datetime,timedelta,date
import matplotlib.pyplot as plt
import streamlit as st
from preprocess import investment_detail,find_top_stocks,find_equity_curve,nifty_curve
import time
import concurrent.futures


st.title('Stock Investment Analysis')

# Describing Data
st.subheader('Nifty 50 Companies')
listed_comp = pd.read_csv('Nifty50.csv')
st.write(listed_comp)

# User Input for Investment Analysis
st.subheader('Analyse Investment')

start = st.text_input("Enter the Start Date in yy-mm-dd Format", '2020-01-01')

end = st.text_input("Enter the End Date in yy-mm-dd Format", '2021-01-01')

initial_investment = int(st.text_input("Enter the Investment Amount ", 1000000))

n_days_measure_perf = int(st.text_input("Enter the no. of days to measure Performance", 100))

top_n_stocks = int(st.text_input("Enter no. of top stock for selection", 10))

st.write("This Process may take few minutes.")

# Investment Details

if st.button('Analyse'):

    with concurrent.futures.ThreadPoolExecutor() as executor:

        nifty50_stocks = executor.submit(investment_detail,start,initial_investment)
        
        top_stocks = executor.submit(find_top_stocks,start,n_days_measure_perf,top_n_stocks)
        
        top_stocks_invest = executor.submit(investment_detail,start,initial_investment,list(top_stocks.result()[2].keys()))

        top_stocks_curve = executor.submit(find_equity_curve,start,end,top_stocks_invest.result()[2])

        nifty50_stocks_curve = executor.submit(find_equity_curve,start,end,nifty50_stocks.result()[2])

        nifty50_curve = executor.submit(nifty_curve,start,end,initial_investment)
    


    c1,c2 = st.columns(2)

    with c1:
        st.subheader('Total Invested Amount')
        st.subheader(round(nifty50_stocks.result()[1],3))
    with c2:
        st.subheader('Remaining Amount')
        st.subheader(round(nifty50_stocks.result()[0],3))

    st.subheader('Investment Detail of Nifty 50 Stocks')
    st.write('Quantities Purchased on Open Price of Stocks')
    st.write('Open Price x Quantity = Invested Amount')
    st.write(nifty50_stocks.result()[2])


    st.subheader('Stocks Performance')
    st.write(top_stocks.result()[0])

    st.subheader('Top Selected Companies')
    st.write(pd.DataFrame({"Companies":top_stocks.result()[1],'Returns (%)':top_stocks.result()[2].values()}))

    c3,c4 = st.columns(2)
    with c3:
        st.subheader('Total Invested Amount')
        st.subheader(round(top_stocks_invest.result()[1],3))
    with c4:
        st.subheader('Remaining Amount')
        st.subheader(round(top_stocks_invest.result()[0],3))
        
    st.subheader('Investment Detail of Top Selected Stocks') 
    st.write('Quantities Purchased on Open Price of Stocks')
    st.write('Open Price x Quantity = Invested Amount')
    st.write(top_stocks_invest.result()[2])

    st.subheader("Equity Values")

    c5,c6,c7 = st.columns(3)
    with c5:
        st.subheader('Equally distributed stocks')
        st.write(nifty50_stocks_curve.result())
    with c6:
        st.subheader('Top Selected Stocks')
        st.write(top_stocks_curve.result())
    with c7:
        st.subheader('Nifty Investment')
        st.write(nifty50_curve.result()[0])



    st.subheader("Equity Curve Graph")
    date_lst1 = [datetime.strptime(d, '%Y-%m-%d') for d in nifty50_stocks_curve.result()['Date']]
    date_lst2 = [datetime.strptime(d, '%Y-%m-%d') for d in top_stocks_curve.result()['Date']]
    date_lst3 = [datetime.strptime(d, '%Y-%m-%d') for d in nifty50_curve.result()[0]['Date']]
    
    fig,ax = plt.subplots()
    plt.title("Equity Curve Graph",fontweight='bold',fontsize=15)
    ax.plot(date_lst1,nifty50_stocks_curve.result()['Equity Curve'],color='red')
    ax.plot(date_lst2,top_stocks_curve.result()['Equity Curve'],color='grey')
    ax.plot(date_lst3,nifty50_curve.result()[0]['Equity Curve'],color='blue')
    plt.xlabel('Date',fontweight='bold',fontsize=15)
    plt.ylabel('Values',fontweight='bold',fontsize=15)
    ax.legend(['Equal Alloc Buy Hold','Performance_strat','Nifty'])
    plt.xlim(date_lst1[0],date_lst1[-1])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)



    




