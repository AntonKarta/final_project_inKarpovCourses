# импорт библиотек

import pandas as pd # мир пандам
import numpy as np

import scipy.stats as st # Статистика 

import matplotlib.pyplot as plt #Графики - сила
import seaborn as sb
import plotly.express as px
import plotly.graph_objects as go


def get_bootstrap(
    group_a, # числовые значения первой выборки
    group_b, # числовые значения второй выборки
    boot_it = 3000, # количество бутстрэп-подвыборок
    statistic = np.mean, # интересующая нас статистика
    bootstrap_conf_level = 0.95 # уровень значимости
):
    boot_len = max([len(group_a), len(group_b)])
    boot_data = []
    for i in range(boot_it): # извлекаем подвыборки
        samples_1 = group_a.sample(
            boot_len, 
            replace = True # параметр возвращения
        ).values
        
        samples_2 = group_b.sample(
            boot_len, 
            replace = True
        ).values
        
        boot_data.append(statistic(samples_1-samples_2)) # mean() - применяем статистику
        
    pd_boot_data = pd.DataFrame(boot_data)
        
    left_quant = (1 - bootstrap_conf_level)/2
    right_quant = 1 - (1 - bootstrap_conf_level) / 2
    ci = pd_boot_data.quantile([left_quant, right_quant])
        
    p_1 = st.norm.cdf(
        x = 0, 
        loc = np.mean(boot_data), 
        scale = np.std(boot_data)
    )
    p_2 = st.norm.cdf(
        x = 0, 
        loc = -np.mean(boot_data), 
        scale = np.std(boot_data)
    )
    p_value = min(p_1, p_2) * 2
        
    # Визуализация
    plt.figure(figsize=[15,5])
    plt.hist(pd_boot_data[0], bins = 50,color='green')
    plt.style.use('ggplot')
    plt.vlines(ci,ymin=0,ymax=50,linestyle='--',)
    plt.xlabel('boot_data')
    plt.ylabel('frequency')
    plt.title("Histogram of boot_data")
    plt.show()
       
    return  p_value