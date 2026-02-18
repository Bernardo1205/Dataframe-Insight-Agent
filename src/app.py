import pandas as pd
import streamlit as st

from src.agent.agent import Agent

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
        st.success("Done!")
        st.text_area("Response", value=result.get("output", ""), height=200)
