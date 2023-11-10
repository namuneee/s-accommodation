import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import numpy as np
import math

def ColourWidgetText(wgt_txt, wch_colour = '#000000'):
    htmlstr = """<script>var elements = window.parent.document.querySelectorAll('*'), i;
                    for (i = 0; i < elements.length; ++i) { if (elements[i].innerText == |wgt_txt|) 
                        elements[i].style.color = ' """ + wch_colour + """ '; } </script>  """

    htmlstr = htmlstr.replace('|wgt_txt|', "'" + wgt_txt + "'")
    components.html(f"{htmlstr}", height=0, width=0)

st.subheader('1. 수용도 계산')
st.sidebar.title(':blue[인자 값]을 입력하세요')

status = st.sidebar.radio(
    '확인하고 싶은 타입 선택',
    ['LCD','LED'])
if status == 'LCD':
    
    text = st.sidebar.number_input('글꼴높이 (mm)', 0.0) 

    glass = st.sidebar.number_input('유리 투과율 (%)', 0.0, 100.0) 

    bright = st.sidebar.number_input('글꼴 명도 (%)', 0.0, 100.0) 

    back_il = st.sidebar.number_input('배경 휘도 (cd/m\u00b2)', 0.0, value=1.0) 
    

elif status == 'LED':

    text = st.sidebar.number_input('글꼴높이 (mm)', 0.0) 

    glass = st.sidebar.number_input('유리 투과율 (%)', 0.0, 100.0) 

    bright = st.sidebar.number_input('조명 광도 (cd/m\u00b2)', 0.0)

    back_il = st.sidebar.number_input('배경 휘도 (cd/m\u00b2)', 0.0, value=10.0) 


#보이는 페이지 1번. 수용도 계산
col1,col2 = st.columns([8,2]) # 공간을 2:3 으로 분할하여 col1과 col2라는 이름을 가진 컬럼을 생성합니다.  

with col1 :
    if status =='LCD':
        st.caption('•  휘도대비 (cd/m\u00b2) : 글꼴휘도 / 배경휘도')
        st.caption('•  글꼴휘도 (cd/m\u00b2) : {0.009(글꼴명도(%))$^2$ - 0.02글꼴명도(%)} x 유리투과율')

        #lcd 글꼴휘도
        text_il=(0.009 * (bright)**2 - 0.02*bright)*(glass/100)
        #휘도대비
        illum=text_il/back_il

        lcd_acm=(1 / (1 + np.exp(-(0.01997*illum + 1.19709*text -6.3165))))*100 #수용도 계산
        df=pd.DataFrame({
              '휘도대비 (cd/m\u00b2)': [illum], '글꼴높이 (mm)': [text]})
        st.dataframe(df, hide_index=True, width=500)

        df=pd.DataFrame({
             '유리 투과율 (%)':[glass], '글꼴 명도 (%)': [bright], '글꼴휘도 (cd/m\u00b2)': [text_il], '배경휘도 (cd/m\u00b2)': [back_il]})
        st.dataframe(df, hide_index=True, width=500)
        

    elif status == 'LED':
        st.caption('•  휘도대비 (cd/m\u00b2) : 글꼴휘도 / 배경휘도')
        st.caption('•  글꼴휘도 (cd/m\u00b2) : 조명광도 x 유리투과율')
        
        #led 글꼴휘도
        text_il=bright*(glass/100)
        #lcd휘도대비
        illum=text_il/back_il

        led_acm=(1 / (1 + np.exp(-(0.02389*illum + 1.18998*text -6.9123))))*100 #수용도 계산
        df=pd.DataFrame({
            '휘도대비 (cd/m\u00b2)': [illum], '글꼴높이 (mm)': [text]})
        st.dataframe(df, hide_index=True, width=500)

        df=pd.DataFrame({
            '유리 투과율 (%)':[glass], '조명 광도 (cd/m\u00b2)': [bright], '글꼴휘도 (cd/m\u00b2)': [text_il], '배경휘도 (cd/m\u00b2)': [back_il]})
        st.dataframe(df, hide_index=True, width=500)

        
with col2 :
  # column 2 에 담을 내용
    st.markdown('##')
    st.markdown('##')
    if status == 'LCD':
        st.metric(label="수용도", value="{0:.2f}%".format(lcd_acm))
        if lcd_acm>75:
            ColourWidgetText("{0:.2f}%".format(lcd_acm), '#3a960f') 
        else:
            ColourWidgetText("{0:.2f}%".format(lcd_acm), '#FF0000') 
    elif status == 'LED':
        st.metric(label="수용도", value="{0:.2f}%".format(led_acm))
        if led_acm>75:
            ColourWidgetText("{0:.2f}%".format(led_acm), '#3a960f') 
        else:
            ColourWidgetText("{0:.2f}%".format(led_acm), '#FF0000') 

st.divider()
st.markdown('###')
st.subheader('2. 타깃 수용도에 따른 글꼴 높이 계산')
st.markdown("###")
acm_slider = st.slider('수용도 (%)', 0, 100, 75, 5)

col3,col4 = st.columns([8,2])

#글꼴높이 얻기
# lcd_acm=(1 / (1 + np.exp(-(0.01997*illum + 1.19709*text -6.3165))))*100 #수용도 계산
# led_acm=(1 / (1 + np.exp(-(0.02389*illum + 1.18998*text -6.9123))))*100 #수용도 계산

with col3 :
    if status =='LCD':
        st.markdown('✅ 왼쪽 사이드바에 **유리 투과율**, **글꼴 명도**, **배경 휘도**를 입력하시오')
        st.caption('•  배경 휘도 default value: 1 (cd/m\u00b2)')
        if (acm_slider==100) | (acm_slider==0) :
            st.error('🚨 [계산 불가] 입력하신 인자 값을 다시 확인하세요')
            lcd_text=0
        else:
            if back_il==0:
                lcd_text=0
            else:
                lcd_text=(6.3165-math.log(100/acm_slider-1)-0.01997*(0.009*(bright)**2-0.02*bright)*(glass/100)/back_il)/1.19709
            if lcd_text<0:
                lcd_text=0
            elif lcd_text>100:
                lcd_text=100
            else:
                lcd_text=lcd_text
            #lcd 글꼴휘도
            text_il=(0.009 * (bright)**2 - 0.02*bright)*(glass/100)
            if text_il<0:
                text_il=0
            else:
                text_il=text_il
            #휘도대비
            illum=text_il/back_il
            df=pd.DataFrame({
                '유리 투과율': [glass], '글꼴 명도':[bright], '글꼴 휘도': [text_il], '배경 휘도': [back_il],'휘도 대비': [illum], '수용도': [acm_slider]})
            st.dataframe(df, hide_index=True, width=500)
        
    elif status == 'LED':
        st.markdown('✅ 왼쪽 사이드바에 **유리 투과율**, **조명 광도**, **배경 휘도**를 입력하시오')
        st.caption('•  배경 휘도 default value: 10 (cd/m\u00b2)')
        if (acm_slider==100) | (acm_slider==0) :
            st.error('🚨 [계산 불가] 입력하신 인자 값을 다시 확인하세요')
            led_text=0
        else:
            if back_il==0:
                led_text=0
            else:
                led_text=(6.9123-math.log(100/acm_slider-1)-0.02389*bright*(glass/100)/back_il)/1.18998
            if led_text<0:
                led_text=0
            elif led_text>100:
                led_text=100
            else:
                led_text=led_text
            #led 글꼴휘도
            text_il=bright*(glass/100)
            if text_il<0:
                text_il=0
            else:
                text_il=text_il
            #lcd휘도대비
            illum=text_il/back_il
            df=pd.DataFrame({
                '유리 투과율': [glass], '조명 광도':[bright], '글꼴 휘도': [text_il], '배경 휘도': [back_il],'휘도 대비': [illum], '수용도': [acm_slider]})
            st.dataframe(df, hide_index=True, width=500)

with col4 :
    st.markdown('#')
    st.markdown('##')
# column 2 에 담을 내용
    if status == 'LCD':
        st.metric(label="글꼴높이", value="{0:.1f}mm".format(lcd_text))
        ColourWidgetText("{0:.1f}mm".format(lcd_text), '#4068cf') 

    elif status == 'LED':
        st.metric(label="글꼴높이", value="{0:.1f}mm".format(led_text))
        ColourWidgetText("{0:.1f}mm".format(led_text), '#4068cf') 

if status=='LED':
    st.divider()
    st.markdown('###')
    st.subheader('3. (참고) 광도 단위 변환표')
    st.caption('•  조명 광도 (cd/m\u00b2) : 조명의 설계값(lm)이 아닌, 유백필름 표면 위 휘도계로 측정된 조명의 휘도값')
    df=pd.DataFrame({
                    'LED 광도 (%)': [100, 80, 60, 40], 'cd/m\u00b2':[1800, 1440, 1080, 720]})
    st.dataframe(df, hide_index=True, width=300)