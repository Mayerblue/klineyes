#!/usr/bin/python
# -*- coding: UTF-8 -*-
from patterns import classifier_list
import pandas as pd
import numpy as np

def classifier_single_date(data):
    '''
    获取某一天的形态
    :param date:
    :param data:
    :return:
    '''
    candle_quant = get_candlestick_feature(data)
    for classifier in classifier_list:
        df = classifier(candle_quant)
        if df is not None:
            return df


def get_candlestick_feature(data):
    '''
    单根蜡烛线 参数计算 top_height bottom_height entity_height pct_change pct_amplitude positive
    :param data:
    :return:
    '''
    negtive_filter = lambda x: None if x < 0 else x       # 过滤负值（无效数据）
    calc_rate = lambda shadow_height, height : None if shadow_height is None or height == 0.0 or height is None else shadow_height / height     # 计算影线占实体的比例
    height = data.highestPrice - data.lowestPrice   # 蜡烛图长度

    return {
        'top_height': calc_rate(negtive_filter(data.highestPrice - max(data.openPrice, data.closePrice)), height),
        'bottom_height': calc_rate(negtive_filter(min(data.openPrice, data.closePrice)-data.lowestPrice), height),
        'entity_height': calc_rate(abs(data.closePrice-data.openPrice), height),
        'pct_change': calc_rate(abs(data.closePrice-data.lowestPrice), data.openPrice),
        'pct_amplitude': calc_rate(abs(data.highestPrice-data.openPrice), data.openPrice),
        'positive': True if((data.closePrice - data.preClosePrice) > 0) else False   # True=阳  False=阴
    }