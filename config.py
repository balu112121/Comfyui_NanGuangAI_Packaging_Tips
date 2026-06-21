"""
配置文件 - 南光AI包装提示词
"""

# 节点配置
NODE_CONFIG = {
    "version": "1.0.0",
    "author": "NanGuangAI",
    "name": "南光AI包装提示词",
    "category": "南光AI/包装",
    "max_text_length": 1000,
    "supported_languages": ["中文", "英文"],
    "output_formats": ["详细完整版", "简洁版", "关键词版"],
    "style_emphasize": ["标准", "强调高端感", "强调生态环保", "强调简约现代", "强调传统韵味"]
}

# 包装模板配置
PACKAGING_TEMPLATES = {
    "详细完整版": {
        "template_type": "detailed",
        "include_all": True,
        "format": "detailed"
    },
    "简洁版": {
        "template_type": "short",
        "include_all": False,
        "format": "short"
    },
    "关键词版": {
        "template_type": "keywords",
        "include_all": False,
        "format": "keywords"
    }
}

# 风格强调词库
STYLE_EMPHASIS = {
    "标准": "",
    "强调高端感": "高端奢华，品质感强，",
    "强调生态环保": "生态环保理念，可持续设计，",
    "强调简约现代": "极简主义，现代感强，",
    "强调传统韵味": "传统美学，文化底蕴，"
}

# 材质库
MATERIAL_LIBRARY = {
    "纸类": ["白卡纸", "铜版纸", "牛皮纸", "艺术纸", "特种纸"],
    "塑料类": ["PE", "PET", "PP", "PVC"],
    "金属类": ["铝箔", "锡纸", "马口铁"],
    "玻璃类": ["玻璃", "磨砂玻璃"],
    "其他": ["E瓦楞纸板", "B瓦楞纸板", "灰纸板"]
}

# 工艺库
PROCESS_LIBRARY = {
    "印刷": ["胶印", "凹印", "柔印", "丝印", "数码印刷"],
    "表面处理": ["覆哑膜", "覆光膜", "UV上光", "烫金", "烫银", "压纹"],
    "后期": ["模切", "糊盒", "开窗", "折页"]
}

# 常见配色方案
COLOR_SCHEMES = {
    "自然风": ["绿色", "棕色", "米色", "白色"],
    "简约风": ["白色", "黑色", "灰色", "银色"],
    "高端风": ["金色", "黑色", "白色", "深蓝"],
    "清新风": ["蓝色", "白色", "绿色", "粉色"],
    "传统风": ["红色", "金色", "黑色", "黄色"]
}