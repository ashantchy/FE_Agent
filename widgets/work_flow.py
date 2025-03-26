import streamlit as st
import time
 
def workflow_widget():
    # Define steps
    steps = [
        "Accessing the Url",
        "Extracting the Table",
        "Parsing The Table",
        "Cleaning the Table",
        "Saving Data",
        "Finished"
    ]
   
    # UI for the workflow animation
    st.subheader("Workflow Animation", anchor=False)
 
    # Layout for the steps (with added empty row and vertical line in the 3rd column of the second row)
    layout = [
        [steps[0], "Line", steps[1], "Line", steps[2]],  # First row: 1 | separator | 2 | separator | 3
        ["", "", "", "", "Vertical Line"],  # Empty row with vertical line in 3rd column
        [steps[5], "Line", steps[4], "Line", steps[3]],  # Second row: 6 | separator | 5 | separator | 4
    ]
 
    # Create a container to hold all steps (boxes)
    boxes = []  # List to store empty containers (boxes) for each step
 
    # Create the empty boxes in the correct layout (pre-existing boxes)
    for row_steps in layout:
        cols = st.columns(len(row_steps))  # Create columns for each row
        for i, (col, step) in enumerate(zip(cols, row_steps)):
            if step == "Line":
                # Add a line separator between the steps
                col.markdown("<hr style='border: 1px solid white;'>", unsafe_allow_html=True)
            elif step == "Vertical Line":
                # Add a vertical line only in the 3rd column of the empty row, centered
                col.markdown("""
                    <div style="width: 2px; height: 150px; background-color: white; margin: 0 auto;"></div>
                """, unsafe_allow_html=True)
            elif step == "":
                # Empty space in the second row (no content)
                col.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
            else:
                # Create the empty container for each step
                step_box = col.empty()
                boxes.append(step_box)  # Store it in the list of boxes
                step_box.markdown(f"<p style='color: white; padding: 10px;'>{step}</p>", unsafe_allow_html=True)
 
    # Add custom CSS to adjust margin between boxes and rows
    st.markdown("""
        <style>
            /* Add margin between boxes */
            .css-1d391kg {
                margin-bottom: 30px;  /* Adds more space between each box */
            }
 
            /* Add margin between rows */
            .stBlock {
                margin-bottom: 300px;  /* Adds even more space between rows */
            }
        </style>
    """, unsafe_allow_html=True)
 
    # Function to run the workflow animation with spinner
    def run_workflow():
        # Sequentially go through steps in the original order: 1, 2, 3, 4, 5, 6
        step_order = [
            steps[0], steps[1], steps[2], steps[3], steps[4], steps[5]
        ]
       
        # Initialize the box index
        box_index = 0  # Start from the first box in the layout
        # Sequentially show each step
        for idx, step in enumerate(step_order):
            # Find the correct box in the layout (first or second row)
            for row_idx, row in enumerate(layout):
                if step in row:
                    # Find the position of the step in the current row
                    step_pos = row.index(step)
                    # Calculate the correct box index for this step by counting valid steps before it
                    box_index = sum([1 for s in row[:step_pos] if s != "Line" and s != "Vertical Line" and s != ""])  # Only count non-"Line" items
                   
                    # Get the correct box from the boxes list based on the total box index
                    current_box = boxes[box_index + sum([len([1 for s in r if s != "Line" and s != "Vertical Line" and s != ""]) for r in layout[:row_idx]])]  # Adjust box index for prior rows
                   
                    # Show the spinner for the current step in the correct box
                    with current_box:
                        with st.spinner(f"{step}..."):
                            time.sleep(2)  # Simulate work being done
                   
                    # After the spinner finishes, show the step as completed (green)
                    with current_box:
                        current_box.success(step)
 
                    break
 
    # Buttons to start the workflow
    col1, col2 = st.columns(2)
    with col1:
        # Start button that triggers the workflow
        if st.button("Start"):
            run_workflow()
 

 