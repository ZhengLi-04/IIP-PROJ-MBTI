import streamlit as st
import time

# st.button("Start over")

# placeholder = st.empty()
# # placeholder.markdown("Hello")
# time.sleep(1)

# placeholder.progress(0, "Wait for it...")
# time.sleep(1)
# placeholder.progress(50, "Wait for it...")
# time.sleep(1)
# placeholder.progress(100, "Wait for it...")
# time.sleep(1)

# with placeholder.container():
#     st.line_chart({"data": [1, 5, 2, 6]})
#     time.sleep(1)
#     st.markdown("3...")
#     time.sleep(1)
#     st.markdown("2...")
#     time.sleep(1)
#     st.markdown("1...")
#     time.sleep(1)

# placeholder.markdown("Poof!")
# time.sleep(1)

# placeholder.empty()


st.button("Rerun")

with st.spinner("Wait for it...", show_time=True):
    time.sleep(5)
st.success("Done!")

progress_text = "Operation in progress. Please wait."
my_bar = st.progress(0, text=progress_text)

for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1, text=progress_text)
time.sleep(1)
my_bar.empty()

st.button("Rerun")