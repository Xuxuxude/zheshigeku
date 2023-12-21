import re
import seaborn as sns
import pandas as pd
import streamlit as st
from collections import Counter
import jieba
import requests
from flask import Flask
from matplotlib import pyplot as plt
from pyecharts import options as opts
from pyecharts.charts import Bar, Line ,Pie ,WordCloud
from bs4 import BeautifulSoup
import streamlit.components.v1 as components


app = Flask(__name__)

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
def remove_punctuation(text):
    text1 = re.sub(r'\s+', '', text)
    return re.sub(r'[^\w\s]', '', text1)
# 分词并统计词频
def segment_and_count(text):
    words = jieba.lcut(text)
    word_counts = Counter(words)
    return word_counts

def word_process(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text()
    t1=remove_html_tags(text_content)
    t2=remove_punctuation(t1)
    t3=segment_and_count(t2)
    top_words = t3.most_common(20)
    return top_words

def draw_pic_seaborn(data, str):
    x, y = zip(*data)

    if str == '回归图':
        data = {
            'Word': y,
            'Count': y
        }
        df = pd.DataFrame(data)
        df['Cumulative_Count'] = df['Count'].cumsum() / df['Count'].sum() * 100
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df, x='Word', y='Cumulative_Count', label='Percentage')
        plt.xlabel('Word')
        plt.ylabel('Cumulative Percentage')
        plt.title('Top 20 Words and Cumulative Percentage')
        plt.legend(loc='upper left')
        st.pyplot(plt.gcf())

    if str == '直方图':
        plt.hist(y)
        plt.xlabel("Value")
        plt.ylabel("Frequency")
        plt.title("Histogram")
        st.pyplot(plt.gcf())

    if str == '成对关系图':
        words = x
        frequencies = y
        df = pd.DataFrame({
            "Word": words,
            "Frequency": frequencies
        })
        sns.pairplot(df[["Frequency"]])
        st.pyplot(plt.gcf())


def draw_pic_pycharts(data, str):
    x, y = zip(*data)  # 解压数据得到x和y
    if str == '柱状图':
        bar = (
            Bar()
            .add_xaxis(x)
            .add_yaxis("出现频率", y)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="网站词频表"),
                xaxis_opts=opts.AxisOpts(
                    name="词语",
                    interval=0,
                    axislabel_opts=opts.LabelOpts(rotate=45)  # 设置x轴刻度标签旋转45度
                ),
                yaxis_opts=opts.AxisOpts(name="频率"),
            )
        )
        return bar.render_embed()
    if str == '饼图':
        pie = (
            Pie()
            .add("", list(zip(x, y)))
            .set_global_opts(title_opts=opts.TitleOpts(title="饼状图"),
                             legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        return pie.render_embed()
    if str == '折线图':
        line = (
            Line()
            .add_xaxis(x)
            .add_yaxis("出现频率", y)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="网站词频表"),
                xaxis_opts=opts.AxisOpts(
                    name="词语",
                    interval=0,
                    axislabel_opts=opts.LabelOpts(rotate=45)  # 设置x轴刻度标签旋转45度
                ),
                yaxis_opts=opts.AxisOpts(name="频率"),
            )
        )
        return line.render_embed()
    if str == '词云图':
        freq_map = dict(zip(x, map(lambda x: x * 10, range(1, len(x) + 1))))
        wordcloud = (
            WordCloud()
            .add("词云图",list(freq_map.items()),word_size_range=[20,100],rotate_step=45,shape='diamond')
        )
    return wordcloud.render_embed()

def main():
    url = st.text_input('请输入文章URL: ')

    typeAPI=st.sidebar.selectbox('API', ['pyecharts','seaborn'])
    if typeAPI=='pyecharts':
        chart_type = st.sidebar.selectbox('图表类型', ['柱状图', '饼图', '折线图','词云图'])
        if chart_type == '柱状图' and st.button('生成'):
            list1=word_process(url)
            bar_html = draw_pic_pycharts(list1,chart_type)
            components.html(bar_html, height=500, width=900)
        if chart_type == '折线图' and st.button('生成'):
            list1=word_process(url)
            bar_html = draw_pic_pycharts(list1,chart_type)
            components.html(bar_html, height=500, width=900)
        if chart_type == '饼图' and st.button('生成'):
            list1=word_process(url)
            bar_html = draw_pic_pycharts(list1,chart_type)
            components.html(bar_html, height=500, width=900)
        if chart_type == '词云图' and st.button('生成'):
            list1=word_process(url)
            bar_html = draw_pic_pycharts(list1,chart_type)
            components.html(bar_html, height=500, width=900)

    if typeAPI == 'seaborn':
        chart_type2 = st.sidebar.selectbox('图表类型', ['回归图', '直方图', '成对关系图'])
        if chart_type2 == '回归图' and st.button('生成'):
            list1=word_process(url)
            draw_pic_seaborn(list1,chart_type2)

        if chart_type2 == '直方图' and st.button('生成'):
            list1=word_process(url)
            draw_pic_seaborn(list1,chart_type2)

        if chart_type2 == '成对关系图' and st.button('生成'):
            list1=word_process(url)
            draw_pic_seaborn(list1,chart_type2)


if __name__ == "__main__":
    main()