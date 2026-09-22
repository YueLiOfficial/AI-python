
MAP_AGENT_PROMPT = """
你是一名地图规划助手。
你只负责景点搜索、路线分析、地图生成。

规则：
1. 优先筛选 3 到 6 个最值得推荐的景点
2. 输出时说明推荐理由
3. 如果可以生成高德个人地图，优先生成
4. 不要输出冗长原始 POI 数据
"""

def get_map_subagent():
    map_subagent = {
        "name": "map_agent",
        "description": "能够使用高德地图规划旅游路线、进行景点推荐、生成路线地图",
        "system_prompt": MAP_AGENT_PROMPT,
        "skills":["/skills"]
    }

    return map_subagent