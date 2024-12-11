import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# App title
st.title("Student Grade Analysis")

# Initialize session state for storing data
if "student_data" not in st.session_state:
    st.session_state.student_data = pd.DataFrame(columns=["Student Name", "Grade"])

# Form for user input
st.subheader("Enter Student Data")
with st.form("grade_form"):
    student_name = st.text_input("Student Name")
    grade = st.number_input("Grade", min_value=0, max_value=100, value=50)
    submitted = st.form_submit_button("Add Data")
    
    if submitted:
        # Add the input data to session state
        new_data = pd.DataFrame({"Student Name": [student_name], "Grade": [grade]})
        st.session_state.student_data = pd.concat([st.session_state.student_data, new_data], ignore_index=True)
        # Ensure Grade column is numeric
        st.session_state.student_data["Grade"] = pd.to_numeric(st.session_state.student_data["Grade"], errors="coerce")
        st.success(f"Added: {student_name} with Grade: {grade}")

# Display the entered data
if not st.session_state.student_data.empty:
    st.subheader("Student Data")
    st.write(st.session_state.student_data)

    # Grade Distribution
    st.subheader("Grade Distribution")
    fig, ax = plt.subplots()
    sns.histplot(st.session_state.student_data['Grade'], kde=True, bins=10, color="blue", ax=ax)
    ax.set_title("Grade Distribution")
    ax.set_xlabel("Grade")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)
    
    # Top Performers
    st.subheader("Top Performers")
    top_performers = st.session_state.student_data.nlargest(5, "Grade")[["Student Name", "Grade"]]
    st.table(top_performers)
    
    # Average Grade
    avg_grade = st.session_state.student_data['Grade'].mean()
    st.metric(label="Average Grade", value=f"{avg_grade:.2f}")
    
    # Pass/Fail Analysis
    pass_threshold = st.slider("Set Pass Threshold", min_value=0, max_value=100, value=50)
    st.session_state.student_data['Result'] = st.session_state.student_data['Grade'].apply(
        lambda x: "Pass" if x >= pass_threshold else "Fail"
    )
    
    pass_fail_counts = st.session_state.student_data['Result'].value_counts()
    st.subheader("Pass/Fail Analysis")
    fig, ax = plt.subplots()
    sns.barplot(x=pass_fail_counts.index, y=pass_fail_counts.values, palette="viridis", ax=ax)
    ax.set_title("Pass/Fail Counts")
    ax.set_xlabel("Result")
    ax.set_ylabel("Count")
    st.pyplot(fig)
else:
    st.info("No data entered yet. Please use the form above to add student data.")
