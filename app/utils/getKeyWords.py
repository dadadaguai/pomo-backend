from zhipuai import ZhipuAI



def getKeyWords(summary):


    client = ZhipuAI(api_key="ce4fccad5f7b94b2c494c2c82e4a9d8c.iDHBy06hi7OdVXMl")
    prompt = "分析下面的笔记内容，运用关键词提取技术，提取其中的关键信息。生成1个或者2个或者三个关键字。关键字格式实例：xx|xx|xx。每个关键字中文不超过五个字，英文不超过两个单词,笔记内容如下："
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {
                "role": "system",
                "content": "您好！如果您有一段笔记需要提取关键字，只需将笔记内容发送给我。我会分析文本并为您识别出最重要的词汇。您也可以指定需要提取的关键字数量，或者告诉我您对关键字的任何特定要求。现在，请将您的笔记发给我，让我们开始吧！"
            },
            {
                "role": "user",
                "content": prompt+"\n"+summary
            }
        ],
        top_p= 0.7,
        temperature= 0.95,
        max_tokens=1024,
        tools = [{"type":"web_search","web_search":{"search_result":True}}],
        stream=True
    )
    # 初始化一个空字符串来存储提取的内容
    extracted_content = ""
    for trunk in response:
        # 将提取的内容添加到结果字符串中
        extracted_content += trunk.choices[0].delta.content
    # 分割关键字
    keywords = extracted_content.split("|")
    return keywords

if __name__ == '__main__':
    summary = """该文档介绍了一个名为 CR-LIBM（Correctly Rounded LIBM）的新型基础函数库,它实现了 ANSI C99 标准定义的函数,并在所有舍入模式下保证正确舍入。关键点如下:

- 开发 CR-LIBM 的主要目标是在保持合理性能和低内存使用的同时,确保正确舍入,使其适用于实际应用。
    
- CR-LIBM 采用两步方法 - 第一步使用可移植的 IEEE-754 浮点算术进行快速计算,第二步使用软件进位保存算术进行更精确的计算。
    
- 该文档详细解释了 CR-LIBM 中指数函数的实现,包括:
    
    - 处理溢出、下溢和不同模式下的舍入等特殊情况
    - 两步范围缩减过程
    - 多项式求值和最终结果的重构
    - 全面测试以确保在所有舍入模式下的正确舍入
- 作者声称,CR-LIBM 在性能、内存使用和保证正确舍入之间达到了良好平衡,使其适合用于关键应用。
"""

    getKeyWords(summary)