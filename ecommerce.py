import streamlit as st 
import pandas as pd 
import numpy  as np 
import plotly.express as px
import datetime

st.set_page_config(layout="centered",page_title="Ecommerce",page_icon='🛍️',initial_sidebar_state="collapsed")

st.title("Streamlit App about Ecommerce ")
st.image('https://www.zuplic.com/wp-content/uploads/2018/07/eCommerce-Animated-GIF.gif')
st.divider()

# Load the dataset  
df = pd.read_csv("ecommerce.csv")
df.drop_duplicates(inplace=True)
df.columns = df.columns.str.strip().str.lower()

df['month'] = pd.to_datetime(df['year-month']).dt.month
df['year'] = pd.to_datetime(df['year-month']).dt.month
df['hour'] = df['invoicetime'].str.split(':').str[0]
df['hour'] = df['hour'].astype('int64')

def orderdate (x):
    if x >= 12 and x < 17:
        return 'afternoon'
    elif x >= 17 and x < 24 :
        return 'evening'
    else :
        return 'morning'

df['ordertimeofday'] = df['hour'].apply(lambda x : orderdate(x))

num_cols = df.select_dtypes(include='number').columns
cat_cols = df.select_dtypes(include='O').columns

st.sidebar.header("User Input Features")

selected_col = st.sidebar.selectbox("Select Column", ['Univariate','Bivariate', 'Multivariate'])

if  selected_col == "Univariate":
    st.subheader("Univariate Analysis")
    num_col= st.selectbox('Select a numerical column to filter by:', ['ordervalue','quantit','invoiceno'])
    fig1 = px.histogram(df,x=num_col,text_auto = True,template='simple_white',color_discrete_sequence = px.colors.sequential.RdBu,title= f'Histogram of {num_col}')
    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    # cat_col1 = st.selectbox('Select one category column to filter by:', ['major category','minor category','country','ordertimeofday'] )
    # ws = df[cat_col1].value_counts().reset_index()
    # fig2 = px.pie(ws,names='index',values=cat_col1,color_discrete_sequence = px.colors.sequential.RdBu,color = 'index',template='presentation',title=f'Number of {cat_col1}',hole = 0.35)
    # st.plotly_chart(fig2, use_container_width=True)

elif selected_col =='Bivariate':

    st.subheader("Bivariate Analysis")

    st.divider()

    se1 = st.selectbox('Select categorical column  !', ['major category','minor category','country','ordertimeofday'])
    se2 = st.selectbox('Select numerical column  !', ['ordervalue','quantit','invoiceno'])
    agg_selected = st.radio("What aggregation do you want to use?", ('mean', 'sum','count'))

    fig_1 = (px.bar(df.groupby(se1)[se2].agg(agg_selected).reset_index(),x=se1,y=se2,text_auto=True,color= se1
    ,color_discrete_sequence=px.colors.sequential.RdBu
    ,title=f'The {agg_selected} {se2} for each {se1}'))
    st.plotly_chart(fig_1)

    st.divider()

    if st.checkbox('Filter with time. '):
        sel_1 = st.radio('Filter time by ', ['month','hour'])

        data=df.groupby(sel_1)[se2].agg(agg_selected).sort_values(ascending = False).reset_index()
        data= data.sort_values(by =sel_1)

        fig1 = px.line(data_frame=data,x=sel_1,y=se2,title=f'The line of {se2} per {sel_1}s'
        ,color_discrete_sequence = px.colors.sequential.RdBu,markers = True)
        st.plotly_chart(fig1)
    st.divider()

    if st.checkbox('Filter with specific time.'):
        se_1 = st.selectbox('Filter time by ', ['ordertimeofday','month','hour'])
        if se_1=='ordertimeofday':
            filter_time = st.selectbox('Choose the time of day',['morning','afternoon','evening'])
            mask = df['ordertimeofday'] == filter_time

        elif  se_1=='month':
            filter_time = st.slider('Months',0,12)
            mask = df['month'] == filter_time

        else:
            filter_time = st.slider('Hours',0,23)
            mask = df['hour'] == filter_time

        fig1 = (px.bar(df[mask].groupby([se1])[se2].agg(agg_selected).reset_index()
        ,x=se1,y=se2,text_auto=True,color= se1
        ,color_discrete_sequence=px.colors.sequential.RdBu
        ,title=f'The {agg_selected} {se2} for each {se1} in {filter_time}'))
        st.plotly_chart(fig1)

elif selected_col =='Multivariate':
    st.subheader('Multivariate  Analysis')

    values_sel = st.selectbox('Select numeric column to use as values',['ordervalue','quantit','invoiceno'])
    index_sel  = st.multiselect('Select categorical  columns to use as Index',['major category','minor category','country','ordertimeofday'],default = 'country')
    columns_sel= st.selectbox('Select categorical column to use as columns',['major category','minor category','country','ordertimeofday'])
    agg_selected = st.radio("Select aggregation do you want to use", ('mean', 'sum','count'))

    st.dataframe(pd.pivot_table(data=df,values=values_sel,index=index_sel,columns=columns_sel,aggfunc=agg_selected,margins=True,margins_name='Total'), use_container_width=True)
