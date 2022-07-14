import pandas as pd
import numpy as np
from tqdm.auto import tqdm
from scipy.stats import norm

def get_bootstrap(
    data_column_1, # числовые значения первой выборки
    data_column_2, # числовые значения второй выборки
    boot_it = 1000, # количество бутстрэп-подвыборок
    statistic = np.mean, # интересующая нас статистика
    bootstrap_conf_level = 0.95 # уровень значимости
    ):
    
    boot_len = max([len(data_column_1), len(data_column_2)]) # максимальное значение
    boot_data = [] # значение бутстрапа
    
    for i in tqdm(range(boot_it)): # извлекаем подвыборки
        # первая выборка
        samples_1 = data_column_1.sample(
            boot_len, 
            replace = True # параметр возвращения
        ).values
        # вторая выборка
        samples_2 = data_column_2.sample(
            boot_len, 
            replace = True
        ).values
        
        boot_data.append(statistic(samples_1-samples_2)) # mean() - применяем статистику
        
    pd_boot_data = pd.DataFrame(boot_data) # перевод в дата фрэйм
    
    left_quant = (1 - bootstrap_conf_level)/2 # правое значение квантиля
    right_quant = 1 - (1 - bootstrap_conf_level) / 2 # лебое значение квантиля
    ci = pd_boot_data.quantile([left_quant, right_quant]) # значения доверительного интервала
    
    # расчет p-значения
    p_1 = norm.cdf(
        x = 0, 
        loc = np.mean(boot_data), 
        scale = np.std(boot_data)
    )
    
    p_2 = norm.cdf(
        x = 0, 
        loc = -np.mean(boot_data), 
        scale = np.std(boot_data)
    )
    
    p_value = min(p_1, p_2) * 2
    
    
    return {"boot_data": boot_data, 
            "ci": ci, 
            "p_value": p_value}