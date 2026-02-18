import pandas as pd
import streamlit as st

from agent.agent import Agent

st.title("DataFrame Agent")

data = st.file_uploader("Upload a CSV", type=["csv"])
if data is not None:
    df = pd.read_csv(data)
    agent = Agent(df)

    st.write("DataFrame loaded successfully!")
    st.dataframe(df.head())

    query = st.text_area("Insert your query")
    if st.button("Submit Query", type="primary"):
        with st.spinner("Analyzing..."):
            result = agent.run(query)
        response =  None if "Agent stopped due to iteration limit or time limit." in result.get("output", "") else result.get("output", "")
        if response :
            st.text_area("", value=response, height=200)
