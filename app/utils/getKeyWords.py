from zhipuai import ZhipuAI

# 提权关键字函数
def getKeyWords(content):
    # 替换成你的 API key
    api_key = "xxx"
    client = ZhipuAI(api_key=api_key)

    # 将用户内容添加到消息列表中
    messages = [
        {
            "role": "system",
            "content": "请阅读以下文章，并提取1到3个关键字，确保这些关键字准确反映文章的核心内容。关注文章的主题、主要观点和关键概念。如果提取到一个关键字，直接输出；如果提取到多个关键字，请用符号 '|' 隔开。如果生成的是中文关键字，该关键字数不要超过六个字，如果生成的是英文关键字，该关键字的字符数不要超过12个。"
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
