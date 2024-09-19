from zhipuai import ZhipuAI
from datetime import datetime

from app.utils.downloadDaily import downloadDailyToPath


# 生成日报
def generateDailySummary(items):
    api_key = "xxx"
    client = ZhipuAI(api_key=api_key)
    content = ""
    day = datetime.strptime(items[0][0], "%Y-%m-%d %H:%M").strftime("%Y年%m月%d日")
    for item in items:
        content += str(item) + "\n"

    # 将用户内容添加到消息列表中
    messages = [
        {
            "role": "system",
            "content": """
            请根据下面的四元组列表中的内容，生成一篇日报，四元组格式是（开始时间，结束时间，总结，完成情况）,首先根据完成情况True代表已完成，False代表未完成，将日报分为两个部分，一部分是已完成的列表，一部分是未完成的列表，生成的样式是以markdown格式保存，可以使用markdown样式进行渲染，对生成的列表使用无序列表进行排列，每一行前面是创建时间-结束时间，后面是对每一部分的总结，确保准确反映文章的核心内容。示例如下
            **任务完成列表** 
        -  9:10 - 10:10    搜索多模态的数据集 
        - 11:10 - 12:10    进行多模态数据的下载
            **任务未完成列表**
        -  13:10 - 14:10    搜索多模态的数据集 
        - 15:10 - 16:10    进行多模态数据的下载"""
        },
        {
            "role": "user",
            "content": content
        }
    ]

    # 发送请求
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=messages,
        top_p=0.7,
        temperature=0.95,
        max_tokens=1024,
        tools=[{"type": "web_search", "web_search": {"search_result": True}}],
        stream=True
    )

    # 处理响应并提取关键字
    extracted_content = ""
    for trunk in response:
        extracted_content += trunk.choices[0].delta.content
    print(extracted_content)
    print("文件保存成功" if downloadDailyToPath(extracted_content, day) else "文件保存失败")



event_list = [
    (
        "2024-09-01 08:00",
        "2024-09-01 10:00",
        "这次会议将讨论公司未来五年的战略规划。会议将从市场分析开始，涵盖我们的主要竞争对手和目标市场的潜在增长机会。接着，我们将深入探讨产品开发路线图，包括即将推出的新产品和现有产品的改进。此外，会议还将包括一个关于如何提高运营效率和降低成本的特别环节。我们期望所有部门负责人都能提供他们的观点和建议，以便我们能够制定一个全面的、可持续的增长计划。",
        True
    ),
    (
        "2024-09-01 10:30",
        "2024-09-01 11:30",
        "在这次深入的讨论中，我们将分析当前的全球经济形势对我们业务的影响。会议将包括对主要经济指标的回顾，以及它们如何影响我们的供应链、销售和利润率。此外，我们将讨论我们的全球扩张策略，特别是在新兴市场的机遇和挑战。我们还将探讨如何利用技术创新来提高我们的市场竞争力和客户满意度。最后，我们将开放讨论环节，邀请所有参与者分享他们的想法和见解。",
        False
    ),
    (
        "2024-09-01 14:00",
        "2024-09-01 15:00",
        "这份报告将详细介绍我们最新的市场研究结果。它将包括消费者行为的分析、市场趋势的预测以及我们产品在目标市场中的表现。报告还将探讨我们的品牌知名度和客户忠诚度，并提供如何通过营销活动和社交媒体策略来提高这些指标的建议。此外，报告将分析我们的销售数据，以确定最佳的销售渠道和定价策略。我们期望这份报告能为公司提供宝贵的洞察力，帮助我们制定更有效的市场进入和渗透策略。",
        True
    ),
    (
        "2024-09-02 09:00",
        "2024-09-02 11:00",
        "这个全天的工作坊旨在提升我们团队的关键技能，包括领导力、公共演讲和项目管理。我们将从领导力培训开始，探讨如何激励团队、做出决策和处理冲突。接着，我们将进行公共演讲技巧的实践，帮助参与者克服演讲焦虑，提高他们的沟通能力。下午，我们将专注于项目管理，学习如何规划、执行和监控项目，以及如何使用现代工具和技术来提高效率。我们鼓励所有参与者积极参与，分享他们的经验和最佳实践。",
        False
    )
]
generateDailySummary(event_list)