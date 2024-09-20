from zhipuai import ZhipuAI
from datetime import datetime

from app.utils.downloadDaily import downloadDailyToPath


# 生成日报
def generateToDo(content):
    api_key = "xxx"
    client = ZhipuAI(api_key=api_key)

    # 将用户内容添加到消息列表中
    messages = [
        {
            "role": "system",
            "content": """
            请将以下文章内容,从文章中提取出主要任务和目标,转化为一个任务列表i,并结合知识图谱，查询相关的知识点， 按照层次渐进的学习方法，每个计划包括要学习其文章相关的知识点和时间安排。
            输出格式：使用markdown样式进行渲染
任务列表：
1. 任务1：描述任务
   - [ ] 知识点1：描述知识点
   - [ ] 知识点2：描述知识点
   - 时间安排：描述时间安排

2. 任务2：描述任务
   - [ ] 知识点1：描述知识点
   - [ ] 知识点2：描述知识点
   - 时间安排：描述时间安排

样例如下：
文章内容：
量子计算是一种利用量子力学原理进行计算的新型计算方式。它具有巨大的计算潜力，能够解决传统计算机无法解决的问题。量子计算的核心是量子比特（qubit），它可以同时表示0和1的状态。量子计算机的性能取决于量子比特的数量和质量。

输出格式：
任务列表：
1. 任务1：了解量子计算的基本原理
   - [ ] 知识点1：量子力学基础
   - [ ] 知识点2：量子比特的概念
   - 时间安排：2小时

2. 任务2：研究量子计算的应用
   - [ ] 知识点1：量子计算在密码学中的应用
   - [ ] 知识点2：量子计算在优化问题中的应用
   - 时间安排：3小时
"""
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
    # print("文件保存成功" if downloadDailyToPath(extracted_content, day) else "文件保存失败")



if __name__ == '__main__':
    content = """
    基于CLIP模型扩展到多个模态的方法：

模态特定编码器：

文本：保留CLIP的文本Transformer编码器。
图像：保留CLIP的视觉Transformer编码器。
视频：扩展视觉Transformer，加入时序处理能力，如3D卷积或时序注意力机制。
音频：引入专门的音频Transformer，如wav2vec 2.0或AST (Audio Spectrogram Transformer)。


多模态投影层：

设计一个统一的投影层，将所有模态的特征映射到同一个高维空间。
可以使用类似CLIP的方法，但需要处理更多的模态对。


对比学习扩展：

扩展CLIP的对比学习方法到多模态场景。
设计多模态对比损失函数，不仅考虑文本-图像对，还包括文本-视频、文本-音频、图像-视频等所有可能的模态对。


预训练策略：

首先在大规模的单模态数据集上预训练各个模态的编码器。
然后使用多模态数据集进行联合训练，优化跨模态对齐。


下游任务适应：

设计多任务学习目标，包括跨模态检索、模态转换和多模态融合任务。
使用少量标记数据进行微调，以适应特定的下游任务。



可行性分析：
优势：

基础稳固：CLIP模型在文本-图像对齐上已经证明了其有效性，为扩展提供了良好的起点。
可扩展性：CLIP的架构相对灵活，可以相对容易地扩展到其他模态。
迁移学习：可以利用CLIP在大规模数据上的预训练结果，加速其他模态的学习。

挑战：

计算复杂度：增加更多模态会显著增加模型的参数量和计算需求。
数据需求：需要大量的多模态配对数据，特别是包含视频和音频的高质量数据集可能较少。
对齐复杂性：不同模态之间的语义对齐比单纯的文本-图像对齐更加复杂。
模态特性差异：每种模态都有其独特的特性，设计一个统一的架构来有效处理所有模态是具有挑战性的。

实施建议：

渐进式扩展：先从添加一个新模态（如视频）开始，然后逐步扩展到更多模态。
模块化设计：保持各个模态编码器的独立性，便于单独优化和更新。
灵活的训练策略：设计能够处理不完整模态输入的训练方法，以充分利用现有数据集。
持续评估：在扩展过程中，持续评估模型在各种跨模态任务上的性能，确保新增模态不会影响原有模态的性能。
    """
    generateToDo(content)