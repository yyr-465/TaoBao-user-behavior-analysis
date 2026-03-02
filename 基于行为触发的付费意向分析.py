"""
- 付费分析：分析付费用户的行为偏好、消费金额分布，识别高价值付费用户的核心特征。
"""
"""
这里由于数据集中不直接包含商品单价或订单金额，用行为偏好分析 作为提升
转为分析购买与其他行为的关系
    路径偏好：用户是“直接买”多，还是“收藏/加购后再买”多？
    品类偏好：哪些类目（category_id）的购买转化率最高？
    时段偏好：高价值用户（买得次数多的人）通常在哪个时间点下单？
"""
from 数据预处理 import *


def analyze_buy_preferences(df):
    print("付费行为偏好深度分析")

    # 1. 提取所有产生过购买行为的用户 ID
    pay_user_ids = df[df['behavior_type'] == 'buy']['user_id'].unique()
    pay_user_df = df[df['user_id'].isin(pay_user_ids)]

    # 2. 计算这些付费用户在【购买前】各种行为的分布
    behavior_counts = pay_user_df['behavior_type'].value_counts()
    print("付费用户全路径行为分布：")
    print(behavior_counts)
    pv_count = behavior_counts.get('pv', 0)
    buy_count = behavior_counts.get('buy', 0)
    conversion_ratio = pv_count / buy_count if buy_count != 0 else 0
    print(f"全站行为转化比 (PV/Buy): {conversion_ratio:.2f}")
    print(f"注：平均每 {conversion_ratio:.1f} 次点击产生 1 次购买")

    # 3. 品类偏好：哪些类目的购买量最高？
    top_buy_categories = df[df['behavior_type'] == 'buy']['category_id'].value_counts().head(10)
    print(top_buy_categories)

    # 4. 复购率分析（核心指标）
    buy_counts_per_user = df[df['behavior_type'] == 'buy'].groupby('user_id').size()
    repurchase_rate = (buy_counts_per_user > 1).sum() / len(buy_counts_per_user)
    print(f"\n用户复购率 (Repurchase Rate): {repurchase_rate:.2%}")

    return top_buy_categories

if __name__ == '__main__':
    file_path = r"D:\项目\电商用户行为分析与运营策略优化\数据集\UserBehavior.csv\UserBehavior.csv"
    start_date = pd.to_datetime('2017-11-25').date()
    end_date = pd.to_datetime('2017-12-03').date()
    cleaned_df, _ = process_data(file_path, start_date, end_date)
    analyze_buy_preferences(cleaned_df)

"""
1. 转化漏斗：从“海量浏览”到“精准决策”
数据洞察：全站转化比为 32.94。这意味着用户平均点击 33 次才会产生 1 次购买。
论文分析：
“实证数据显示，平台用户的购买转化路径呈现出‘宽顶窄底’的典型特征。PV 与 Buy 的比例约为 33:1，这说明用户在最终下单前存在高频的筛选与对比行为。结合 Cart（加购） 频次约为 Fav（收藏） 频次 2.05 倍的结果，可以推断：在该电商平台上，‘加购’是比‘收藏’更具预测价值的购买前置信号。建议平台在算法推荐中，应赋予‘加购’行为更高的权重权重。”
2. 品类矩阵：识别“流量池”与“利润池”
数据洞察：类目 1464116、2735466、2885642 是购买量最高的前三大品类。
论文分析：
“通过对购买量 Top 10 的品类 ID 进行分析，识别出了平台的核心支柱品类。例如，排名第一的类目 1464116 在短时间内产生了超过 3.4 万次 购买。此类高频购买品类构成了平台的‘流量基本盘’。在运营策略上，应针对这些头部类目建立专有的库存预警与促销机制，利用其高频交易的特性带动长尾品类的联动销售。”
3. 用户粘性：复购率折射出的品牌护城河
数据洞察：复购率高达 65.81%。
论文分析：
“本研究发现，该样本群体的复购率高达 65.81%，这一指标远超行业平均水平（通常约 20%-40%）。结合前述 RF 分层中‘重要价值用户’占比超 1/3 的结果，足以证明平台已形成了极强的用户路径依赖。高复购率不仅降低了平台的二次获客成本（CAC），更为平台开展‘会员订阅制’或‘私域流量运营’提供了坚实的用户基础。”
"""