# nodes.py
# 南光AI包装提示词 - 四端口输出版
# 输出端口：完整提示词、简洁提示词、关键词提示词、调试信息
# 界面：10个分类输入 + 多行补充说明 + 控制选项
# 预置示例数据：笋干礼品盒包装

import re

class Comfyui_NanGuangAI_Packaging_Tips:
    """
    南光AI包装提示词节点
    四端口输出：完整/简洁/关键词/调试信息
    """
    CATEGORY = "南光AI/包装"
    FUNCTION = "generate_prompts"
    OUTPUT_NODE = True
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("完整提示词", "简洁提示词", "关键词提示词", "调试信息")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # ----- 10个分类输入（单行，预置示例）-----
                "产品": ("STRING", {
                    "multiline": False,
                    "default": "笋干",
                    "placeholder": "请输入产品名称，如：笋干"
                }),
                "品牌名": ("STRING", {
                    "multiline": False,
                    "default": "Bamboo Harvest",
                    "placeholder": "请输入品牌名称，如：Bamboo Harvest"
                }),
                "尺寸规格": ("STRING", {
                    "multiline": False,
                    "default": "120*65*145mm",
                    "placeholder": "请输入尺寸规格，如：120*65*145mm"
                }),
                "净含量": ("STRING", {
                    "multiline": False,
                    "default": "200g",
                    "placeholder": "请输入净含量，如：200g"
                }),
                "包装样式": ("STRING", {
                    "multiline": False,
                    "default": "礼品盒",
                    "placeholder": "请输入包装样式，如：礼品盒"
                }),
                "设计风格": ("STRING", {
                    "multiline": False,
                    "default": "简约自然风",
                    "placeholder": "请输入设计风格，如：简约自然风"
                }),
                "设计元素": ("STRING", {
                    "multiline": False,
                    "default": "竹叶图案、山脉轮廓",
                    "placeholder": "请输入设计元素，如：竹叶图案、山脉轮廓"
                }),
                "主题配色": ("STRING", {
                    "multiline": False,
                    "default": "绿色、棕色、米色",
                    "placeholder": "请输入主题配色，如：绿色、棕色、米色"
                }),
                "印刷材质": ("STRING", {
                    "multiline": False,
                    "default": "350g白卡纸+E瓦楞纸板",
                    "placeholder": "请输入印刷材质，如：350g白卡纸+E瓦楞纸板"
                }),
                "印刷工艺": ("STRING", {
                    "multiline": False,
                    "default": "胶印+覆哑膜",
                    "placeholder": "请输入印刷工艺，如：胶印+覆哑膜"
                }),
                
                # ----- 补充说明（多行编辑框）-----
                "补充说明": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "补充说明：南光AIGC绘画提示词、模型、图像、音频视频、工作流定制，节点软件开发服务。商业定制VX：nankodesign2001(注明来意）..."
                }),
            },
            "optional": {
                # ----- 控制选项（位于补充说明下方）-----
                "风格强调": (["强调高端感", "强调自然感", "强调艺术感", "强调电影感"], {
                    "default": "强调高端感"
                }),
                "输出格式": (["详细完整版", "简洁版", "关键词版"], {
                    "default": "详细完整版"
                }),
                "语言": (["中文", "英文"], {
                    "default": "中文"
                }),
                "启用高级模式": ("BOOLEAN", {
                    "default": True,
                    "label_on": "开启",
                    "label_off": "关闭"
                }),
            }
        }

    def generate_prompts(self, **kwargs):
        """
        生成四种提示词 + 调试信息
        """
        # 1. 读取所有字段
        fields = {
            "产品": kwargs.get("产品", "").strip(),
            "品牌名": kwargs.get("品牌名", "").strip(),
            "尺寸规格": kwargs.get("尺寸规格", "").strip(),
            "净含量": kwargs.get("净含量", "").strip(),
            "包装样式": kwargs.get("包装样式", "").strip(),
            "设计风格": kwargs.get("设计风格", "").strip(),
            "设计元素": kwargs.get("设计元素", "").strip(),
            "主题配色": kwargs.get("主题配色", "").strip(),
            "印刷材质": kwargs.get("印刷材质", "").strip(),
            "印刷工艺": kwargs.get("印刷工艺", "").strip(),
        }
        extra = kwargs.get("补充说明", "").strip()
        style = kwargs.get("风格强调", "强调高端感")
        output_format = kwargs.get("输出格式", "详细完整版")
        lang = kwargs.get("语言", "中文")
        advanced = kwargs.get("启用高级模式", True)

        # 字段顺序（用于组装提示词）
        field_order = [
            "产品", "品牌名", "尺寸规格", "净含量", "包装样式",
            "设计风格", "设计元素", "主题配色", "印刷材质", "印刷工艺"
        ]

        # 2. 构建完整内容列表（仅非空字段）
        all_parts = []
        for key in field_order:
            val = fields.get(key, "")
            if val:
                all_parts.append(val)
        if extra:
            all_parts.append(extra)

        # 3. 风格前缀（映射到包装语境）
        style_prefix_map = {
            "强调高端感": "高端奢华，品质感强，",
            "强调自然感": "自然清新，生态环保，",
            "强调艺术感": "艺术氛围浓厚，创意独特，",
            "强调电影感": "电影级质感，视觉冲击力强，"
        }
        style_prefix = style_prefix_map.get(style, "")

        # ========== 生成四种输出 ==========

        # ---- (1) 完整提示词 ----
        full_prompt = "，".join(all_parts)
        if style_prefix and full_prompt:
            full_prompt = style_prefix + full_prompt
        elif style_prefix:
            full_prompt = style_prefix + "包装设计"
        # 添加通用包装结尾（若没有则补充）
        if not any(kw in full_prompt for kw in ["构图", "渲染", "高清", "8K"]):
            full_prompt += "，整体构图干净、优雅，写实产品渲染，影棚布光，正面透视视角，高清，8K，可商业落地，符合印刷要求"
        if lang == "英文" and full_prompt:
            full_prompt = "[English] " + full_prompt
        if not full_prompt:
            full_prompt = "一款简约礼品盒包装设计，产品为未知，请填写产品信息"

        # ---- (2) 简洁提示词 ----
        # 选取核心字段：产品、品牌名、包装样式、设计风格、主题配色、设计元素
        core_keys = ["产品", "品牌名", "包装样式", "设计风格", "主题配色", "设计元素"]
        concise_parts = []
        for key in core_keys:
            val = fields.get(key, "")
            if val:
                concise_parts.append(val)
        if extra:
            concise_parts.append(extra[:50] + "..." if len(extra) > 50 else extra)
        concise_prompt = "，".join(concise_parts[:6])
        if style_prefix and concise_prompt:
            concise_prompt = style_prefix + concise_prompt
        if lang == "英文" and concise_prompt:
            concise_prompt = "[English] " + concise_prompt
        if not concise_prompt:
            concise_prompt = "包装设计，简约风格，高清摄影"

        # ---- (3) 关键词提示词 ----
        keywords = []
        # 提取产品名
        product = fields.get("产品", "")
        if product:
            keywords.append(product)
        # 提取品牌名
        brand = fields.get("品牌名", "")
        if brand:
            keywords.append(brand)
        # 提取包装样式
        style_val = fields.get("包装样式", "")
        if style_val:
            keywords.append(style_val)
        # 提取设计风格
        design_style = fields.get("设计风格", "")
        if design_style:
            keywords.append(design_style)
        # 提取配色（取第一个颜色）
        colors = fields.get("主题配色", "")
        if colors:
            color_list = re.split('[、,，]', colors)
            if color_list:
                keywords.append(color_list[0].strip())
        # 提取材质或工艺（取第一个）
        material = fields.get("印刷材质", "")
        if material:
            keywords.append(material[:10])
        # 补充设计元素（取前两个）
        elements = fields.get("设计元素", "")
        if elements:
            elem_list = re.split('[、,，]', elements)
            keywords.extend([e.strip() for e in elem_list[:2] if e.strip()])
        # 去重
        seen = set()
        unique_keywords = []
        for k in keywords:
            if k not in seen:
                seen.add(k)
                unique_keywords.append(k)
        keyword_prompt = "，".join(unique_keywords[:8])
        if style_prefix:
            keyword_prompt = style_prefix + keyword_prompt
        if lang == "英文" and keyword_prompt:
            keyword_prompt = "[English] " + keyword_prompt
        if not keyword_prompt:
            keyword_prompt = "包装，设计，礼品盒，高端"

        # ---- (4) 调试信息 ----
        debug_lines = ["=== 南光AI包装提示词调试信息 ==="]
        for key in field_order:
            val = fields.get(key, "")
            debug_lines.append(f"{key}: {val if val else '（空）'}")
        debug_lines.append(f"补充说明: {extra if extra else '（空）'}")
        debug_lines.append(f"风格强调: {style}")
        debug_lines.append(f"输出格式: {output_format}")
        debug_lines.append(f"语言: {lang}")
        debug_lines.append(f"启用高级模式: {'开启' if advanced else '关闭'}")
        debug_info = "\n".join(debug_lines)

        return (full_prompt, concise_prompt, keyword_prompt, debug_info)


# 节点注册
NODE_CLASS_MAPPINGS = {
    "Comfyui_NanGuangAI_Packaging_Tips": Comfyui_NanGuangAI_Packaging_Tips
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Comfyui_NanGuangAI_Packaging_Tips": "南光AI包装提示词"
}