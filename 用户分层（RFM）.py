"""
用户分层：用RFM模型（最近消费时间、消费频率、消费金额）将用户分为高价值、
潜力、一般、流失4类；
R:最近一次消费
F：消费频率
M：消费金额
"""
from scipy.fft import rfft2

from 数据预处理 import *
import pandas as pd
def RF_analysis (df):
    print("RF用户分层分析")
    buy_df = df[df['behavior_type'] == 'buy'].copy()
    analysis_date = buy_df['date'].max()
    rf_model = buy_df.groupby('user_id').agg({
        'date':lambda x:(analysis_date - x.max()).days,
        'item_id':'count'
    })
    rf_model.columns = ['R','F']
    rf_model['R_score'] = pd.qcut(
        rf_model['R'], q=4, labels=[4,3,2,1],
        duplicates = 'drop')
    rf_model['F_score'] = pd.qcut(
        rf_model['F'].rank(method = 'first'), q=4,
        labels=[1,2,3,4])
    r_avg = rf_model['R_score'].astype(int).mean()
    f_avg = rf_model['F_score'].astype(int).mean()
    def get_segment(row):
        r = int(row['R_score'])
        f = int(row['F_score'])

        if r > r_avg and f > f_avg:
            return '重要价值用户'
        if r < r_avg and f > f_avg:
            return "重要保持用户"
        if r > r_avg and f < f_avg:
            return "重要发展用户"
        else:
            return "一般保留用户"
    rf_model['用户分层'] = rf_model.apply(get_segment,axis=1)

    rf_summary = rf_model['用户分层'].value_counts().reset_index()
    rf_summary.columns = ['用户分层','人数']
    rf_summary['占比(%)'] = (rf_summary['人数']/rf_summary['人数'].sum() * 100).round(2)

    print(rf_summary)
    return rf_model,rf_summary
if __name__ == '__main__':
    file_path = r"D:\项目\电商用户行为分析与运营策略优化\数据集\UserBehavior.csv\UserBehavior.csv"
    start_date = pd.to_datetime('2017-11-25').date()
    end_date = pd.to_datetime('2017-12-03').date()

    cleaned_df, _ = process_data(file_path, start_date, end_date)
    rf_model, rf_summary = RF_analysis(cleaned_df)

"""
根据 RF 分析结果，你可以为项目报告准备以下策略：
重要价值用户 (High R, High F)：他们是核心资产。
策略：通过会员积分、专属客服、新品优先试用进行深度维系。
重要保持用户 (Low R, High F)：曾经很忠诚，但最近没买了。
策略：发送召回通知或大额流失补偿券，防止被竞品挖走。
重要发展用户 (High R, Low F)：最近刚买过，但频次不高。
策略：通过**多买优惠（如第二件半价）**提高客单价和购买频次。
一般留存用户 (Low R, Low F)：活跃度和忠诚度都低。
策略：通过低价爆款进行基础留存，不必投入过多营销成本。
"""
"""
论文段落：电商用户价值分层实证分析
[标题示例：基于改进型 RF 模型的用户价值特征分布研究]
本研究通过对 100 万+ 规模的电商用户行为数据进行挖掘，
利用最近消费时间（Recency）与消费频率（Frequency）构建了 RF 
用户价值评估模型。通过等频分线法对指标进行打分量化，将付费用户群体划分为四
个显著的维度特征层级（见表 X）。
实证结果显示，该电商平台的重要价值用户占比最高，达到了 34.66%。
这表明平台拥有较为稳固的核心用户基础，这部分群体在统计周期内表现出高频且近期
的购买行为，是平台 GMV（商品交易总额）贡献的主要来源。
其次，一般保留用户与重要发展用户分别占比 27.98% 和 22.02%。其中，
重要发展用户作为“近期有过购买但频次偏低”的群体，
反映了平台近期具备较强的拉新转化能力或促销吸引力，具有较大的价值跃迁潜力。
值得关注的是，重要保持用户占比为 15.34%。此类用户虽然历史贡献度较高，
但近期活跃度出现明显下滑，存在流失风险。从预警管理角度看，
该群体应作为运营侧“精准召回”的核心目标。综上所述，该平台用户结构整体呈现
向好态势，但需针对不同层级的流失风险与成长空间实施差异化的动态管理策略。
"""
"""
给你的建议：
关于 M 指标的说明：如果审稿人问起为什么没有 M（金额），
你可以在论文的“研究设计”部分提到：“鉴于脱敏数据集中未包含具体成交金额，
本研究采用行为频次作为价值强度的代理变量，构建了适配互联网高频交易场景的
 RF 模型。”
可视化建议：在论文中，配合一个饼图或帕累托图展示这四个占比，视觉效果会更好。
"""