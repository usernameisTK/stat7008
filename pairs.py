pairs = [
    # 基本问候
    [r"my name is (.*)", ["Hello %1, How are you today?"]],
    [r"hi|hello|hey", ["Hi there!", "Hello!", "Hey! How can I help you?"]],
    [r"how are you?", ["I'm just a program, but I'm doing well! How about you?"]],
    [r"good morning", ["Good morning! How's your day starting?"]],
    [r"good evening", ["Good evening! How was your day?"]],

    # 自我介绍
    [r"what is your name?", ["I am a chatbot created to assist you."]],
    [r"are you human?", ["No, I am a virtual assistant here to help you."]],
    [r"what can you do?", ["I can chat with you, provide information, and help with simple tasks."]],

    # 日常问答
    [r"what time is it?", ["I'm not wearing a watch, but you can check your device for the time."]],
    [r"what is the weather like?", ["I can't check it now, but you can try a weather app for accurate info!"]],
    [r"can you tell me a joke?", ["Why don't scientists trust atoms? Because they make up everything!"]],
    [r"what is the meaning of life?", ["42! Just kidding, it depends on what you make of it."]],
    [r"how do I cook (.*)?", ["I'm not a chef, but you can find great recipes online for %1!"]],

    # 个人状态
    [r"i am feeling (.*)", ["Why are you feeling %1?", "Oh, I'm here if you want to talk about it."]],
    [r"i am (.*)", ["Why do you think you are %1?", "How long have you been %1?"]],

    # 社交场景
    [r"do you have friends?", ["My only friends are the users I interact with, like you!"]],
    [r"can we be friends?", ["Of course! I'm happy to be your digital friend."]],
    [r"what do you do for fun?", ["Chatting with you is my idea of fun!"]],
    
    # 生活建议
    [r"how do I stay healthy?", ["Eat balanced meals, stay active, and sleep well!"]],
    [r"how do I manage stress?", ["Try deep breathing, mindfulness, or talking to a friend."]],

    # 结束对话
    [r"bye|goodbye", ["Goodbye! Have a great day!", "See you later!"]],
    [r"thank you", ["You're welcome!", "Glad I could help!"]],
    [r"thanks", ["You're welcome!", "Anytime!"]],
    [r"see you later", ["See you! Take care!"]]
]
