# core package 
import streamlit as st
from streamlit_lottie import st_lottie

import pandas as pd

import plotly.express as px
from db_fxns import (create_table,add_data,view_all_data,
                     get_task,view_unique_tasks,edit_task_data,delete_data)

def main():
    st.title("To-Do App")
    st_lottie('https://assets5.lottiefiles.com/packages/lf20_V9t630.json', key="user")
    menu = ["Create", "Read", "Update","Delete","About"]
    choice = st.sidebar.selectbox("Menu", menu)

    create_table()
    if choice == "Create":
        st.subheader("Add Items")

        #Layout
        col1,col2 = st.columns(2)
        
        with col1:
            task = st.text_area("Task To Do")
        with col2:
            task_status = st.selectbox("Status",["ToDo","Doing","Done"])    
            task_due_date = st.date_input("Due Date")

        if st.button("Add Task"):
            add_data(task,task_status,task_due_date)
            st.success("Successfully Added Data:{}".format(task))
            
    elif choice == "Read":
        st.subheader("View Items")
        result = view_all_data()
        st.write(result)

        df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
        with st.expander("View All Data"):
            st.dataframe(df)

        with st.expander("Task Status"):
            task_df = df['Status'].value_counts().reset_index()
            task_df.columns = ['Status', 'Count']  # Renaming columns for clarity
            st.dataframe(task_df)  # This line is optional, shows the DataFrame before plotting
            
            # Display the bar chart for task status distribution
            p1 = px.bar(task_df, x='Status', y='Count', title="Task Status Distribution")
            st.plotly_chart(p1)

            # Calculate and display the overall completion rate
            total_tasks = len(df)
            accomplished_tasks = len(df[df['Status'] == 'Done'])
            not_accomplished_tasks = total_tasks - accomplished_tasks
            labels = ['Accomplished Tasks', 'Not Accomplished Tasks']
            values = [accomplished_tasks, not_accomplished_tasks]
            fig1 = px.pie(names=labels, values=values, title='Overall Task Completion Rate')
            st.plotly_chart(fig1)

            # Calculate and display the accomplishment rate from ToDo tasks
            todo_tasks = len(df[df['Status'] == 'ToDo'])
            if todo_tasks > 0:
                percent_accomplished_from_todo = (accomplished_tasks / todo_tasks) * 100
                labels_todo = ['Accomplished From ToDo', 'Remaining ToDo']
                values_todo = [accomplished_tasks, todo_tasks - accomplished_tasks]
                fig2 = px.pie(names=labels_todo, values=values_todo, title='Accomplishment Rate of ToDo Tasks')
                st.plotly_chart(fig2)
            else:
                st.write("No ToDo tasks to display completion rate.")

    elif choice == "Update":
        st.subheader("Edit/Update Items")
        st.subheader("View Items")
        result = view_all_data()
        st.write(result)
        df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
        with st.expander("Current Data"):
            st.dataframe(df)

        #st.write(view_unique_tasks())
        list_of_task = [i[0] for i in view_unique_tasks()]
        #st.write(list_of_task)

        selected_task = st.selectbox("Task To Edit",list_of_task)
        selected_result = get_task(selected_task)
        st.write(selected_result)
        if selected_result:
            task = selected_result[0][0]
            task_status = selected_result[0][1]
            task_due_date = selected_result[0][2]
                #Layout
            col1,col2 = st.columns(2)
            
            with col1:
                new_task = st.text_area("Task To Do",task)
            with col2:
                new_task_status = st.selectbox(task_status,["ToDo","Doing","Done"])    
                new_task_due_date = st.date_input(task_due_date)

            if st.button("Update Task"):
                edit_task_data(new_task, new_task_status, new_task_due_date, task, task_status, task_due_date)
                st.success("Updated ::{} ::To {}".format(task, new_task))


        result2 = view_all_data()
        # st.write(result)
        df2 = pd.DataFrame(result2, columns=["Task", "Status", "Date"])
        with st.expander("View Updated Data"):
            st.dataframe(df2)     
		

   
          
				
          
              

        
    elif choice == "Delete":
                st.subheader("Delete Items")
                result = view_all_data()
                # st.write(result)
                df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
                with st.expander("Current Data"):
                    st.dataframe(df)

                list_of_task = [i[0] for i in view_unique_tasks()]
                selected_task= st.selectbox("Task to Delete", list_of_task)
                st.warning("Do you want to Delete?:: '{}'".format(selected_task))

                if st.button("Delete"):
                    delete_data(selected_task)
                    st.warning("Deleted: '{}'".format(selected_task))

                new_result = view_all_data()

                df2 = pd.DataFrame(new_result, columns=["Task", "Status", "Due Date"])
                with st.expander("Updated Data"):
                    st.dataframe(df2)

if __name__ == "__main__":
    main()