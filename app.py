import streamlit as st
from streamlit_option_menu import option_menu
import processor,solver
import matplotlib.pyplot as plt
from st_aggrid import GridOptionsBuilder, AgGrid
import plotly.express as px
import altair as alt
import seaborn as sns


def table(data):
    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_pagination(paginationAutoPageSize=True)  # Add pagination
    gb.configure_side_bar()  # Add a sidebar
    gridOptions = gb.build()

    grid_response = AgGrid(
        data,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT',
        update_mode='MODEL_CHANGED',
        fit_columns_on_grid_load=True,
        theme='blue',  # Add theme color to the table
        enable_enterprise_modules=False,
        height=350,
        width='120%',
        reload_data=True
    )



def header(url):
    st.markdown(
        f'<h3 style="color:#faf3f2;">{url}</h3>',
        unsafe_allow_html=True)
def title(url):
    st.markdown(
        f'<h1 style="color:#eb4034;">{url}</h1>',
        unsafe_allow_html=True)

with st.sidebar:
    user_menu=option_menu(
    'Whatsapp Chat Analyzer',['Upload'],menu_icon="cast",icons=['cloud-arrow-up'])

if user_menu=='Upload':
    uploaded_file = st.sidebar.file_uploader("Choose A File")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        data=bytes_data.decode('utf-8')
        df=processor.preprocess(data)

        #unique users
        user_list=df['user'].unique().tolist()
        user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0,'Overall')
        selected_user=st.sidebar.selectbox('Select A User',user_list)

        if st.sidebar.button('Analyze'):

            num_messages,words,num_media_msg = solver.stats(selected_user,df)



            header('Top Statistics')
            col1, col2, col3 = st.columns(3)

            with col1:

                header('Messages Sent')
                title(num_messages)
            with col2:
                header('Words  Spoken')
                title(words)
            with col3:
                header('Media Shared')
                title(num_media_msg)

            header('Monthly Activity Timeline')
            total=solver.monthly_timeline(selected_user,df)
            fig1 = px.line(data_frame=total, x='Time', y='message', labels=dict(Time="Time", message="Message Count"))
            st.plotly_chart(fig1)



            header('Daily Activity Timeline')
            daily = solver.daily_timeline(selected_user,df)
            fig2=px.line(daily, x='Date',y='message',labels=dict(Date="Date", message="Message Count"))
            fig2.update_traces(line_color='#1bd13d')
            st.plotly_chart(fig2)



            col4, col5 = st.columns(2, gap='large')
            day_df=solver.day_activity(selected_user,df)
            monthly_df=solver.monthly_activity(selected_user,df)

            with col4:
                header('Busiest Days')
                chart = alt.Chart(day_df).mark_bar().encode(
                    y='Count',
                    x=alt.X('Day', sort='-y'),
                    color=alt.value("#faf3f2")  # The negative color
                ).properties(width=400)
                st.altair_chart(chart)

            with col5:
                header('Busiest Months')

                chart = alt.Chart(monthly_df).mark_bar().encode(
                    y='Count',
                    x=alt.X('Month', sort='-y'),
                    color=alt.value("orange")  # The negative color
                ).properties(width=400)
                st.altair_chart(chart)



            if selected_user=='Overall':
                x,new_df = solver.most_chatty_users(df)

                col6,col7 =st.columns(2,gap='large')
                with col6:
                    header('Most Busy Users')

                    chart = alt.Chart(x).mark_bar().encode(
                        y='Message Count',
                        x=alt.X('User', sort='-y'),
                        color=alt.value("#3375de")  # The negative color
                    ).properties(width=350,height=440)
                    st.altair_chart(chart)

                with col7:
                    header('Contributions To The Chat')
                    table(new_df)

            header('Activity Heatmap')
            user_heatmap = solver.activity_heatmap(selected_user, df)
            fig3,ax=plt.subplots(figsize=(10,6))
            ax=sns.heatmap(user_heatmap)
            ax.set_xlabel('Hours', fontsize=10)
            ax.set_ylabel('Day', fontsize=10)

            st.pyplot(fig3)


            header('Most Used Words')
            df_wc=solver.createt_wordcloud(selected_user,df)
            fig4, ax = plt.subplots(figsize=(12, 10))
            ax.imshow(df_wc)
            st.pyplot(fig4)









