"""
工具类 - 提供各种辅助功能
"""

import re
from typing import List, Dict, Tuple
from .config import STYLE_EMPHASIS


class TextValidator:
    """文本验证器"""
    
    def __init__(self, max_length: int = 1000):
        self.max_length = max_length
    
    def validate_total_length(self, params: Dict[str, str]) -> Tuple[bool, str]:
        """验证总文本长度"""
        total_text = ''.join(str(v) for v in params.values() if isinstance(v, str))
        if len(total_text) > self.max_length:
            return False, f"❌ 输入文本超过{self.max_length}字符限制，当前长度：{len(total_text)}"
        return True, "验证通过"
    
    def validate_field_length(self, field: str, max_length: int = 200) -> Tuple[bool, str]:
        """验证单个字段长度"""
        if len(field) > max_length:
            return False, f"字段长度超过{max_length}字符限制"
        return True, "验证通过"


class PromptGenerator:
    """提示词生成器"""
    
    def generate_short_prompt(self, full_prompt: str, params: Dict[str, str]) -> str:
        """生成简洁提示词"""
        # 提取关键信息
        keywords = []
        
        # 提取产品名
        product_match = re.search(r'产品(?:为|：)\s*([^，,。]+)', full_prompt)
        if product_match:
            keywords.append(product_match.group(1).strip())
        
        # 提取设计风格
        style_match = re.search(r'设计风格[：:]\s*([^，,。]+)', full_prompt)
        if style_match:
            keywords.append(style_match.group(1).strip())
        
        # 提取配色
        color_match = re.search(r'配色[：:]\s*([^，,。]+)', full_prompt)
        if color_match:
            keywords.append(color_match.group(1).strip())
        
        # 如果关键词太少，使用简化策略
        if len(keywords) < 3:
            # 取前200个字符
            short = full_prompt[:200]
            if len(full_prompt) > 200:
                short += "..."
            return short
        
        # 组合简洁提示词
        short = f"{'，'.join(keywords)}，{full_prompt[-50:] if len(full_prompt) > 50 else full_prompt}"
        if len(short) > 200:
            short = short[:197] + "..."
        
        return short
    
    def generate_keywords_prompt(self, params: Dict[str, str]) -> str:
        """生成关键词提示词"""
        keywords = []
        
        # 基础关键词
        if params.get('product'):
            keywords.append(params['product'])
        if params.get('brand'):
            keywords.append(params['brand'])
        if params.get('style'):
            keywords.append(params['style'])
        if params.get('design_style'):
            keywords.append(params['design_style'])
        
        # 设计元素
        if params.get('elements'):
            elements = [e.strip() for e in re.split('[、,，]', params['elements']) if e.strip()]
            keywords.extend(elements[:3])  # 取前3个
        
        # 配色
        if params.get('colors'):
            colors = [c.strip() for c in re.split('[、,，]', params['colors']) if c.strip()]
            keywords.extend(colors[:2])  # 取前2个
        
        # 材质工艺
        if params.get('material'):
            keywords.append(params['material'])
        if params.get('process'):
            keywords.append(params['process'])
        
        # 补充通用关键词
        keywords.extend(['包装设计', '产品摄影', '8K', '高清'])
        
        # 去重
        seen = set()
        unique_keywords = []
        for k in keywords:
            if k not in seen:
                seen.add(k)
                unique_keywords.append(k)
        
        return '，'.join(unique_keywords[:15])  # 限制15个关键词
    
    def translate_to_english(self, text: str) -> str:
        """简单的中文到英文翻译（实际项目中可接入翻译API）"""
        # 这是一个简单的示例，实际使用时建议使用翻译API
        translations = {
            '产品': 'Product',
            '品牌名': 'Brand',
            '包装': 'Packaging',
            '设计': 'Design',
            '风格': 'Style',
            '配色': 'Color scheme',
            '材质': 'Material',
            '工艺': 'Process',
            '高端': 'Premium',
            '简约': 'Minimalist',
            '自然': 'Natural',
            '环保': 'Eco-friendly',
            '传统': 'Traditional',
            '现代': 'Modern',
            '高清': 'High quality',
            '写实': 'Realistic',
            '影棚布光': 'Studio lighting',
            '透视视角': 'Perspective view'
        }
        
        result = text
        for zh, en in translations.items():
            result = result.replace(zh, en)
        
        return result


class StyleManager:
    """风格管理器"""
    
    def __init__(self):
        self.emphasis_map = STYLE_EMPHASIS
    
    def get_emphasis(self, style: str) -> str:
        """获取风格强调词"""
        return self.emphasis_map.get(style, "")
    
    def get_all_styles(self) -> List[str]:
        """获取所有风格选项"""
        return list(self.emphasis_map.keys())
    
    def get_style_description(self, style: str) -> str:
        """获取风格描述"""
        descriptions = {
            "标准": "标准设计风格，平衡各方面要素",
            "强调高端感": "突出高端品质，奢华质感",
            "强调生态环保": "强调环保理念，可持续设计",
            "强调简约现代": "极简设计，现代美学",
            "强调传统韵味": "传统文化元素，古典韵味"
        }
        return descriptions.get(style, "")


class CacheManager:
    """缓存管理器"""
    
    def __init__(self, cache_dir: str = "./cache"):
        self.cache_dir = cache_dir
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self):
        """确保缓存目录存在"""
        import os
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def get_cache(self, key: str) -> str:
        """获取缓存"""
        import os
        cache_file = os.path.join(self.cache_dir, f"{key}.txt")
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    
    def set_cache(self, key: str, value: str):
        """设置缓存"""
        import os
        cache_file = os.path.join(self.cache_dir, f"{key}.txt")
        with open(cache_file, 'w', encoding='utf-8') as f:
            f.write(value)