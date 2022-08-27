from cProfile import label
import calendar
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from streamlit_option_menu import option_menu

#import the database 
import database as db

#parameters-------------
incomes = ['Salary','Consultation','Gift','Other']
expenses = ['Rent','Internet', 'Food', 'Transport', 'Misc.']
currency = 'USD'
page_title = 'Monthly Pocket Tracker'
page_icon = ':moneybag:'
layout = 'centered' #wide / centered

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_icon+' '+ page_title)

#drop-down Periods
years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name[1:])

#get periods from DB
def get_all_periods():
    items = db.fetch_all_periods()
    periods = [item["key"] for item in items]
    
    return periods


#html reset
html_style = """ 
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
"""
st.markdown(html_style, unsafe_allow_html=True)

#navigation
selected = option_menu(
    menu_title=None,
    options=["Financial Log", "Budget Visualizer"],
    icons=["cash-coin","file-bar-graph"], #bootstrap
    orientation='horizontal'
)

if selected == "Financial Log":

    #input form
    st.header(f"Data Entry in {currency}")
    with st.form("data_form", clear_on_submit=True):
        col_1, col_2 = st.columns(2)
        col_1.selectbox("Select Month", months, key='month')
        col_2.selectbox("Select Year", years, key='year')


        with st.expander("Income"):
            for income in incomes:
                st.number_input(f"{income}:", min_value=0, format="%i", step=1, key=income)

        with st.expander("Expense"):
            for expense in expenses:
                st.number_input(f"{expense}:", min_value=0, format="%i", step=1, key=expense)
        
        with st.expander("Comment"):
            comment = st.text_area("", placeholder="Any Comments ...?")

        submitted = st.form_submit_button("Save")

        if submitted:
            period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
            incomes = {income: st.session_state[income] for income in incomes}
            expenses = {expense: st.session_state[expense] for expense in expenses}

            #insert from db
            db.insert_period(period=period, incomes=incomes, expenses=expenses, comment=comment)

            #print
            #st.write(f"date: {period}")
            #st.write(f"incomes: {incomes}")
            #st.write(f"expenses: {expenses}")
            #st.write(f"comment: {comment}")
            st.success("Income and Expenditure Successfully Saved!")


elif selected == "Budget Visualizer": 
#Visualizer

    st.header("Income-Expense Visualizer")
    with st.form("saved_periods"):

        period = st.selectbox('Select Period: ', get_all_periods() #["2022_August"]
        )
        submitted = st.form_submit_button('Visualize')
        
        if submitted:
            #comment='Random...'
            #incomes = {'Salary': 100.0, 'Consultation': 20.0, 'Gift': 10.0, 'Other': 30.0}
            #expenses= {'Rent': 20.0, 'Internet': 10.0, 'Food': 20.0, 'Transport': 0.0, 'Misc.': 20.0}

            period_data = db.get_period(period)
            comment = period_data.get("comment")
            incomes = period_data.get("incomes")
            expenses = period_data.get("expenses")

            #metrics
            total_income = sum(incomes.values())
            total_expenses = sum(expenses.values())
            remainder = total_income - total_expenses

            col_1, col_2, col_3 = st.columns(3)
            
            col_1.metric("Total Income:", f"{currency} {total_income}")
            col_2.metric("Total Expenses:", f"{currency} {total_expenses}")
            col_3.metric("Total Remainder (Budget):", f"{currency} {remainder}")
            

    #sankey chart

            label = list(incomes.keys()) + ["Total Expenses"] + list(expenses.keys())
            source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
            target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses]
            value = list(incomes.values()) + list(expenses.values())

            link = dict(source=source, target=target, value=value)
            node = dict(label = label, pad=20, thickness=30, color='#e0b35e')
            data = go.Sankey(link=link, node=node)

            fig = go.Figure(data)
            fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
            st.plotly_chart(fig, use_container_width=True)
            
            st.text(f"Comment: {comment}")