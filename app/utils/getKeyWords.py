from zhipuai import ZhipuAI

# 提权关键字函数
def getKeyWords(content):
    # 替换成你的 API key
    api_key = "xx.xx"
    client = ZhipuAI(api_key=api_key)

    # 将用户内容添加到消息列表中
    messages = [
        {
            "role": "system",
            "content": """请阅读以下文章，并提取1到3个关键字，确保这些关键字准确反映文章的核心内容。关注文章的主题、主要观点和关键概念。如果提取到一个关键字，直接输出；如果提取到多个关键字，请用符号 '|' 隔开。如果生成的是中文关键字，该关键字数不要超过六个字，如果生成的是英文关键字，该关键字的字符数不要超过12个"
                       必须严格按照上面的要求生成，示例如下：
                       量子计算是一种利用量子力学原理进行计算的新型计算方式。它具有巨大的计算潜力，能够解决传统计算机无法解决的问题。量子计算的核心是量子比特（qubit），它可以同时表示0和1的状态。量子计算机的性能取决于量子比特的数量和质量。近年来，量子计算在密码学、优化问题和材料科学等领域展现出了广阔的应用前景。
                       关键字：量子计算|量子比特
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
    keywords = extracted_content.split("|")
    # 返回关键字列表
    return keywords
