import streamlit as st
import subprocess
import sys


def main():
    page = st.sidebar.selectbox("Choose a page", ["Move Approved Orders", "Exploration"])

    if page == "Move Approved Orders":
        st.header("This is approve order mover tool.")
        st.write("This button will move things from 03_Files Approved for Processing to new batch folders in 01_Order Production")
        st.write("Make sure the word 'batch' is in the folder name!")
        result = st.button("Move Files!")
        if result:
            subprocess.run([f"{sys.executable}", "/app/gdrive_scripts/refresh_token.py"])
            st.write("finished")
    # elif page == "Exploration":
    #     st.title("Data Exploration")
    #     x_axis = st.selectbox("Choose a variable for the x-axis", df.columns, index=3)
    #     y_axis = st.selectbox("Choose a variable for the y-axis", df.columns, index=4)
    #     visualize_data(df, x_axis, y_axis)

if __name__ == "__main__":
    main()

