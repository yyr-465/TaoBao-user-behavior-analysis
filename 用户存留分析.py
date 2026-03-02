"""
留存分析：计算日 / 周 / 月留存率，分析不同用户群体的留存差异，
挖掘高留存用户行为特征；
"""
import pandas as pd
from 数据预处理 import *
def calculate_retention(df):
    print("用户存留率分析")
    user_active_days = df[['user_id','date']].drop_duplicates()
    retention_table = []
    unique_dates = sorted(user_active_days['date'].unique())
    for i ,base_date in enumerate(unique_dates):#enumerate()在遍历（循环）一个列表或序列时，同时获得“索引（第几个）”和“对应的元素值”。返回的结果形似Series，但不是
        base_users = set(user_active_days[user_active_days['date'] == base_date]['user_id'])
        base_count = len(base_users)
        retention_row = {'日期':base_date,'初始人数':base_count}
        for day_offset in range(1,8):
            target_idx =i +day_offset
            if target_idx < len(unique_dates):
                target_date = unique_dates[target_idx]
                target_users = set(user_active_days[user_active_days['date'] == target_date]['user_id'])
                retained_users = len(base_users & target_users)
                retention_row[f'Day{day_offset}'] = round(retained_users/base_count *100,2)
            else:
                retention_row[f'Day{day_offset}'] = None
        retention_table.append(retention_row)
    retention_df = pd.DataFrame(retention_table)
    print(retention_df)
    return retention_df

if __name__ == '__main__':
    file_path = r"D:\项目\电商用户行为分析与运营策略优化\数据集\UserBehavior.csv\UserBehavior.csv"
    start_date = pd.to_datetime('2017-11-25').date()
    end_date = pd.to_datetime('2017-12-03').date()
    cleaned_df, _ = process_data(file_path, start_date, end_date)
    calculate_retention(cleaned_df)

"""
在论文的“研究方法”部分，你可以这样描述这个双重循环的逻辑：“本研究采用了**滑动时间窗口法（Sliding Window）**构建留存矩阵。
以观察期内的每一日作为基准日（$T_0$），通过集合交集运算（Set Intersection）识别在后续 $T_{+n}$ 日重复活跃的用户 ID，
从而精确计算出动态留存率。”
"""
"""
你可以直接参考这段话放入你的论文结论部分：
“通过留存矩阵分析发现，该平台用户展现出极强的周期活跃特征。常规日次日留存率均值为 78.8%，表明平台对用户具有较强的基础吸引力。
尤为显著的是，在 12 月 2 日（双十二预热及周末节点），各基准日的用户回流率均突破了 90%（如图 X 所示）。
这一数据揭示了电商营销活动对用户行为的显著干预作用：通过大促预热与周末流量波峰的叠加，平台实现了极高比例的用户召回。
这也验证了在电商运营中，精准的时间节点选择与营销节奏把控是提升留存的核心要素。”
"""
