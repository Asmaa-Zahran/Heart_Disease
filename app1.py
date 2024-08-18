import streamlit as st

tab1,tab2,tab3,tab4 = st.tabs(["Application","About Heart Data","Univariate","Bivariate"])

with tab1 :
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("<h1 style='color:rgb(255, 165, 0)'>Enter Your Data <h1>",unsafe_allow_html=True)    
        heart = st.radio(label="HeartDisease",options=["Yes","No"])
        col3,col4 = st.columns(2,gap='large')

        with col3:
            weight = st.number_input(label="Enter your Weight (kg) :")
            smoking = st.radio(label="Smoking",options=["Yes","No"])
            stroke = st.radio(label="Stroke",options=["Yes","No"])
            physical = st.radio(label="PhysicalActivity",options=["Yes","No"])
            kidney = st.radio(label="KidneyDisease",options=["Yes","No"])
            
        with col4:    
            height = st.number_input(label="Enter your height (m) :")
            alcohol = st.radio(label="AlcoholDrinking",options=["Yes","No"])
            diabetic = st.radio(label="Diabetic",options=["Yes","No"])
            asthma =st.radio(label="Asthma",options=["Yes","No"])
            diffWalking = st.radio(label="DiffWalking",options=["Yes","No"])

    gender = st.radio(label="Gender",options=["Female","Male"])
    phy_health = st.slider(label='PhysicalHealth',min_value=0,max_value=30)       
    mental = st.slider(label='MentalHealth',min_value=0,max_value=30)
    age_category = ['18-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64','65-69','70-74','75-79','80 or older']  
    age = st.selectbox(label='AgeCategory',options=age_category)  
    race =['White','Hispanic','Black','American Indian/Alaskan Native','Asian','Other']
    rece_col = st.selectbox(label='Race',options=race)
    gen_health = ['Excellent','Very good','Good','Fair','Poor']
    gen = st.select_slider(label='Gen Health',options=gen_health)
    skin = st.radio(label="SkinCancer",options=["Yes","No"])
    sleep = st.slider(label='SleepTime',min_value=1,max_value=24)
    submit = st.button(label='Submit')
    
    if submit == True:
        bmi = weight / (height)**2
        with open('heart_2020_cleaned.csv',mode='a') as fd:
            fd.write(f"{heart},{bmi},{smoking},{alcohol},{stroke},{phy_health},{mental},{diffWalking},{gender},{age},{rece_col},{diabetic},{physical},{gen},{sleep},{asthma},{kidney},{skin}\n")


with tab2 :
    import pandas as pd
    heart_df = pd.read_csv("heart_2020_cleaned.csv")
    st.title("Heart Disease Data :")
    st.markdown(f"<h6 style='color:gray;'>{heart_df.shape[0]} rows <h6>",unsafe_allow_html=True)
    st.dataframe(heart_df.head(10))
    st.image('eda-heart-.png')

with tab3 :
    import seaborn as sns
    import matplotlib.pyplot as plt
    import plotly.express as px
    st.title('Numeric columns :')
    col5,col6 = st.columns(2)
    with col5:
        fig = plt.figure(figsize=(5,3))
        sns.kdeplot(data = heart_df , x='MentalHealth')
        st.pyplot(fig)
        
        fig = plt.figure(figsize=(5,3))
        heart_df['PhysicalHealth'].hist()
        plt.xlabel('PhysicalHealth')
        plt.ylabel('Frequency')
        plt.title('Distribution of PhysicalHealth')
        st.pyplot(fig)

    with col6:
        fig = plt.figure(figsize=(5,3))
        sns.distplot(heart_df["BMI"],hist=True)
        st.pyplot(fig)

        fig = plt.figure(figsize=(5,3))
        sns.kdeplot(data = heart_df , x='SleepTime')
        st.pyplot(fig)

    st.title('Categorical columns :')
    # cat_cols = heart_df.select_dtypes(include='O').columns
    cat_cols = ['None','HeartDisease', 'Race', 'Diabetic', 'PhysicalActivity','GenHealth']
    result = st.selectbox(label="Distribution of each Categorical columns : ",options=cat_cols)
    
    if result == 'None':
        st.markdown("<h6 style='color:red;'>*Please choose Category : <h6>",unsafe_allow_html=True)

    elif result == 'HeartDisease':
        fig, ax = plt.subplots(1, 1,figsize =(15, 8))
        ax.pie(heart_df['HeartDisease'].value_counts(),autopct='%1.0f%%',labels=['No',"Yes"])
        ax.set_title('The Ratio of Heart Disease ')
        st.pyplot(fig)

    elif result == 'Race':  
        fig = plt.figure(figsize=(15,7))
        sns.countplot(data=heart_df,x='Race')
        st.pyplot(fig)

    elif result == 'Diabetic':
        diabetic =heart_df['Diabetic'].value_counts()
        fig = px.pie(diabetic,names=diabetic.index,title='Diabetic',values=diabetic.values,hole=0.5,height=500,width=500,color_discrete_sequence=px.colors.plotlyjs.Jet)   
        st.plotly_chart(fig, use_container_width=True)
    
    elif result == 'PhysicalActivity':
        fig = plt.figure(figsize=(10,7))
        sns.countplot(data=heart_df,x='PhysicalActivity')
        st.pyplot(fig)

    elif result == 'GenHealth':
        gen_health = heart_df['GenHealth'].value_counts()
        fig = px.pie(gen_health,names=gen_health.index,title='GenHealth',values=gen_health.values,hole=0.5,height=500,width=500,color_discrete_sequence=px.colors.plotlyjs.Electric_r)
        st.plotly_chart(fig, use_container_width=True)



with tab4:
    st.markdown('### Heat Map')
    fig = plt.figure(figsize=(10,7))
    sns.heatmap(data = heart_df.select_dtypes('number').corr(),annot=True) 
    st.pyplot(fig)

    st.markdown('### Heart disease & BMI')
    fig = plt.figure(figsize=(5,3))
    sns.boxplot(y=heart_df["BMI"], x=heart_df["HeartDisease"])
    st.pyplot(fig)

    result = st.selectbox(label="Visualization of Heart disease with : ",options=['None','AgeCategory',"Sex"])
    if result == 'None':
        st.markdown("<h6 style='color:red;'>*Please choose Category : <h6>",unsafe_allow_html=True)
    
    elif result == 'AgeCategory':
        fig = plt.figure(figsize = (13,6))
        sns.countplot(x = heart_df['AgeCategory'], hue = 'HeartDisease', data = heart_df)
        st.pyplot(fig)

    elif result == 'Sex':
        fig, ax = plt.subplots(figsize = (14,8))
        ax.hist(heart_df[heart_df["HeartDisease"]=='No']["Sex"], bins=3, alpha=0.8, color="#4285f4", label="No HeartDisease")
        ax.hist(heart_df[heart_df["HeartDisease"]=='Yes']["Sex"], bins=3, alpha=1, color="#ea4335", label="HeartDisease")
        plt.title('The Ratio of Heart Disease Vs Sex')
        ax.set_xlabel("Sex")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)    
