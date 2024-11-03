import matplotlib.pyplot as plt
import streamlit as st

def plot_sales_chart(dates, sales, title):
    fig, ax = plt.subplots()
    ax.plot(dates, sales, marker="o", linestyle="-")
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Quantité")
    st.pyplot(fig)
