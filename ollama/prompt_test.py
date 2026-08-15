import ollama

client = ollama.Client(host="http://localhost:11434")

def ask(system, user):
    """带 system 的提问（system 可为空字符串）"""
    resp = client.chat(
        model="qwen3.5:4b",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        stream=False,
        think=False
    )
    return resp.message.content

# ① 角色设定对比
print("=== ① 角色设定 ===")
print("[无角色]", ask("", "设备报警 E-102 是什么意思？"))
print("[维修专家]", ask("你是拥有20年经验的工业设备维修专家，回答专业、简洁、先给结论。",
                        "设备报警 E-102 是什么意思？"))

# ② 指令清晰对比
print("\n=== ② 指令清晰 ===")
print("[模糊]", ask("", "解释一下PLC"))
print("[清晰]", ask("", "用不超过100字，面向一线维修工，解释什么是PLC，并列出最常见的3个故障点。"))

# ③ Few-shot（分类）
print("\n=== ③ Few-shot 分类 ===")
fewshot = """把下列句子分类为「故障报修/咨询/无关」三类。
例子1：变频器报警过流 → 故障报修
例子2：这款型号支持485通讯吗？ → 咨询
例子3：今天天气不错 → 无关
现在分类：触摸屏开机黑屏"""
print(ask("", fewshot))

# ④ CoT（思维链）
print("\n=== ④ CoT ===")
print("[直接答]", ask("", "进水管3小时灌满水池，出水管6小时放空，同时开，多久灌满？"))
print("[一步步想]", ask("", "进水管3小时灌满水池，出水管6小时放空，同时开，多久灌满？请先列出计算步骤，再给出答案。"))

# ⑤ 结构化输出（JSON）
print("\n=== ⑤ 结构化输出 ===")
js = ask("只输出JSON，不要任何解释和多余文字。",
         '请分析：设备="伺服电机"，现象="运行中异响"。输出：{"设备": "...", "可能原因": ["...", "..."], "建议": "..."}')
print(js)
import json
try:
    data = json.loads(js)          # 能解析成功 = 程序可直接对接
    print("\n✅ json.loads 解析成功，字段：", list(data.keys()))
except Exception as e:
    print("\n❌ 解析失败（模型带了多余文字）：", e)
