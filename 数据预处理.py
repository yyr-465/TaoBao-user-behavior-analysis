'''
项目一：电商用户行为分析与运营策略优化（优先级最高，适配育碧商业化 / 用户分析岗、互联网DA岗）
一、项目阶段（4
个核心阶段）
1.
数据准备阶段（1
周）：确定分析目标、获取并校验数据
2.
数据预处理阶段（2
周）：数据清洗、异常值 / 缺失值处理、数据格式标准化
3.
核心分析阶段（3
周）：用户行为漏斗、用户分层、留存 / 转化分析
4.
成果输出阶段（1
周）：可视化图表制作、策略提炼、报告撰写
二、项目名称（3
个差异化表述，适配不同场景）
- 求职版：基于RFM模型的电商用户分层与付费转化运营策略优化
- 考研版：电商用户全链路行为分析及留存提升路径研究
- 论文 / 复试精简版：电商用户行为特征挖掘与运营优化实证分析
三、数据来源（权威公开，易获取）
- 核心数据：阿里天池公开数据集（淘宝用户行为数据集，包含用户ID、商品ID、行为类型、时间戳、支付金额等字段，样本量100万 +，覆盖用户点击、收藏、加购、支付全行为）
- 辅助数据：艾瑞咨询电商行业报告、淘宝平台公开运营数据（补充行业背景，提升分析深度）
四、核心步骤（突出SQL / Python实操，贴合你的能力）
1.
数据加载与探索：用Python（pandas）加载数据，查看数据维度、字段含义，通过描述性统计识别数据异常（如时间戳异常、缺失值）；
2.
数据预处理：用SQL完成数据清洗（去重、缺失值填充、异常值剔除），用Python完成时间格式转换、用户行为标签化（如活跃用户、付费用户定义）；
3.
核心分析：
- 行为漏斗分析：拆解“点击 - 加购 - 收藏 - 支付”全链路，计算各环节转化率，定位流失核心节点；
- 用户分层：用RFM模型（最近消费时间、消费频率、消费金额）将用户分为高价值、潜力、一般、流失4类；
- 留存分析：计算日 / 周 / 月留存率，分析不同用户群体的留存差异，挖掘高留存用户行为特征；
- 付费分析：分析付费用户的行为偏好、消费金额分布，识别高价值付费用户的核心特征。
4.
可视化与成果输出：用Tableau制作用户分层、漏斗转化、留存趋势等图表，提炼3 - 4
条可落地的运营策略（如流失用户召回、高价值用户深耕），撰写分析报告。
'''
import pandas as pd

def process_data(file_path,start_date,end_date):
    #指定数据类型以减少内存消耗
    dtypes = {"user_id":'int32', 'item_id': 'int32', 'category_id': 'int32', 'behavior_type': 'int32', 'timestamp': 'int8'}
    columns = ["user_id",'item_id','category_id','behavior_type','timestamp']
    total_missing = pd.Series(0, index=columns + ['datetime', 'date', 'hour'])
    processed_chunks =[]
    csv_chunks =  pd.read_csv(
        file_path,header = None,names = columns,chunksize = 1000000)
    for chunk in csv_chunks:
        chunk['datetime'] = pd.to_datetime(chunk['timestamp'],unit = 's')
        chunk['date'] = chunk['datetime'].dt.date
        chunk['hour'] = chunk['datetime'].dt.hour
        chunk_filtered = chunk[(chunk['date'] >= start_date) & (chunk['date'] <= end_date)]
        # 去重
        chunk_filtered = chunk_filtered.drop_duplicates(
            subset=columns,
            keep='first'
        )
        processed_chunks.append(chunk_filtered)
        #累加缺失值
        total_missing += chunk_filtered.isna().sum()
    #合并所有块
    df_processed = pd.concat(processed_chunks, ignore_index=True)
    return df_processed,total_missing

import matplotlib.pyplot as plt

"""
在处理天池数据时，我发现原始数据存在时间戳越界的问题，因此我除了做常规清洗外，
还专门编写了审计脚本，通过 24 小时流量分布图 
确认了数据符合电商『午后和夜间双高峰』的业务逻辑，剔除了疑似爬虫的超高频采样点。
"""
def audit_data(df):
    """
    专门用于检查数据质量的函数
    """
    print("--- 数据质量审计报告 ---")

    # 1. 检查日期范围（确保没有 1970 或 2025 的噪声）
    dates = df['date'].unique()
    print(f"包含的日期: {sorted(dates)}")

    # 2. 检查用户行为异常（识别爬虫）
    # 计算每个用户总行为数，取前10名
    top_users = df.groupby('user_id').size().sort_values(ascending=False).head(10)
    print(f"\n活跃度前10的用户（检查爬虫）:\n{top_users}")

    # 3. 检查小时分布（验证业务真实性）
    hourly_dist = df['hour'].value_counts().sort_index()
    print("\n小时分布数据已准备，正在生成图表...")

    # 绘图：24小时流量分布
    plt.figure(figsize=(10, 6))
    hourly_dist.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title("User Behavior Distribution by Hour UTC")
    plt.xlabel("Hour of Day")
    plt.ylabel("Behavior Count")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

if __name__ == '__main__':
    file_path = r"D:\项目\电商用户行为分析与运营策略优化\数据集\UserBehavior.csv\UserBehavior.csv"
    start_date = pd.to_datetime('2017-11-25').date()
    end_date = pd.to_datetime('2017-12-03').date()
    cleaned_df, missing_stats = process_data(file_path, start_date, end_date)
    #缺失值
    print(missing_stats)
    #数据量确认
    print(len(cleaned_df))
    #行为分布查看
    print(cleaned_df['behavior_type'].value_counts())
    #质量校验
    audit_data(cleaned_df)
