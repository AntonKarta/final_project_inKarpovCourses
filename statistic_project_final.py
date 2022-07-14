import pandas as pd 
import numpy as np

import scipy.stats as st 

import matplotlib.pyplot as plt 
import seaborn as sb
import plotly.express as px
import plotly.graph_objects as go
import funBood
import pylab


def new_table_pocas(df1, checks, active_studs):
    
    #создание новой группы
    df2    = pd.read_csv('https://getfile.dokpub.com/yandex/get/https://disk.yandex.ru/d/3aARY-P9pfaksg')
    groups = pd.concat([df1, df2], ignore_index=True)
    groups.to_csv('new_group.csv', index=False)
    
    # расчет базовых метрик
    by_chek = checks.merge(groups, on='id') 
    
    mean_chek  = by_chek.groupby('grp',as_index=False).agg({'rev':pd.Series.mean}).rename(columns={'rev':'mean_ch'}) # стредний чек
    max_chek   = by_chek.groupby('grp',as_index=False).agg({'rev':pd.Series.max}).rename(columns={'rev':'max_ch'}) # максимальный чек
    count_chek = by_chek.groupby('grp',as_index=False).agg({'rev':pd.Series.count}).rename(columns={'rev':'count_ch'}) # кооличество чеков
    sum_chek   = by_chek.groupby('grp',as_index=False).agg({'rev':pd.Series.sum}).rename(columns={'rev':'sum_ch'}) # суммарный чек
    join_table_chek = mean_chek.merge(max_chek,on='grp').merge(count_chek,on='grp').merge(sum_chek,on='grp') # сводная
    
    activ_user = active_studs.merge(groups, on='id')
    grp_activ  = activ_user.groupby('grp',as_index=False).agg({'id':pd.Series.count}).rename(columns={'id':'users'})
    
    # расчет сложносоставных метрик
    def CR (grop): # функция для расчета конверсии
        CR_active             = round(activ_user.query("grp==@grop").id.count()/groups.query("grp==@grop").id.count(),2)*100
        CR_active_bying_abs   = round(by_chek.query("grp==@grop").id.count()/groups.query("grp==@grop").id.count(),2)*100
        CR_active_bying_otnos = round(by_chek.query("grp==@grop").id.count()/activ_user.query("grp==@grop").id.count(),2)*100
        return CR_active,CR_active_bying_abs,CR_active_bying_otnos
    
    CR_A  = CR('A')
    CR_B  = CR('B')
    
    def ARPU (grop): # функция для расчета ARPU
        ARPU  = round(by_chek.query("grp==@grop").rev.sum()/groups.query("grp==@grop").id.count(),2)
        ARPAU = round(by_chek.query("grp==@grop").rev.sum()/activ_user.query("grp==@grop").id.count(),2)
        return ARPU,ARPAU
    
    ARPU_A = ARPU('A')
    ARPU_B = ARPU('B') 
    
    group = ['A','B']

    df = pd.DataFrame(columns=['Группа','CR в посетитель','СR посетитель в покупку','CR посетитель в покупку (относительно активного пользователя)','ARPU','ARPAU'])

    CR_active             = [CR_A[0],CR_B[0]]
    CR_active_bying_abs   = [CR_A[1],CR_B[1]]
    CR_active_bying_otnos = [CR_A[2],CR_B[2]]

    ARPU  = [ARPU_A[0],ARPU_B[0]]
    ARPAU = [ARPU_A[1],ARPU_B[1]]

    df['Группа']                                                        = group
    df['CR в посетитель']                                               = CR_active
    df['СR посетитель в покупку']                                       = CR_active_bying_abs 
    df['CR посетитель в покупку (относительно активного пользователя)'] = CR_active_bying_otnos
    df['ARPU']                                                          = ARPU
    df['ARPAU']                                                         = ARPAU
    
    #объединение всех метрик 
    new_table = df.merge(join_table_chek,on=join_table_chek.grp).drop(columns=['key_0','grp']).rename(columns={'mean_ch':\
                        'Средний чек','max_ch':'Максимальный чек', 'count_ch':'Колличество покупок', 'sum_ch':'Суммарный чек'})
     
    return new_table
    
    
    
def figure_plot (df):
    
    columns=df.columns
    columns=columns.drop(['Группа'])

    sb.set(style="darkgrid")

    for col,i in zip(columns,range(9)):
        plt.figure(figsize=[20,20])
        pylab.subplot(5,2,i+1)
        sb.barplot(data=df,x=df['Группа'], y=df[col])
        pylab.xlabel('')
        pylab.ylabel('')
        pylab.title(col)
