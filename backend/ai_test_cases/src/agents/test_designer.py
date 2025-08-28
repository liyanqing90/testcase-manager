# src/agents/test_designer.py
import os
import ast
import autogen
from typing import Dict, List
import logging
from dotenv import load_dotenv
from src.utils.agent_io import AgentIO
load_dotenv()
logger = logging.getLogger(__name__)

# 使用 通义千问 配置
qwen_api_key = os.getenv("QWEN_API_KEY")      # 修改为通义千问API Key
qwen_base_url = os.getenv("QWEN_BASE_URL")    # 修改为通义千问URL
qwen_model = os.getenv("QWEN_MODEL")          # 修改为通义千问模型

class TestDesignerAgent:
    def __init__(self):
        self.config_list = [
            {
                "model": qwen_model,        # 通义千问模型
                "api_key": qwen_api_key,    # 通义千问API Key
                "base_url": qwen_base_url,  # 通义千问URL
            }
        ]
        
        # 初始化AgentIO用于保存和加载设计结果
        self.agent_io = AgentIO()
        
        self.agent = autogen.AssistantAgent(
            name="test_designer",
            system_message='''你是一位专业的测试设计师，擅长将需求转化为全面的测试策略。

你的主要职责包括：
1. 分析需求文档和需求分析结果
2. 设计全面的测试方法，包括但不限于：
   - 功能测试
   - 性能测试
   - 安全测试
   - 兼容性测试
   - 可用性测试
3. 创建详细的测试覆盖矩阵，确保所有功能点都被覆盖
4. 制定合理的测试优先级策略
5. 评估所需的测试资源

在提供测试策略时，你应该：
- 确保测试方法与需求紧密对应
- 提供具体的测试工具和框架建议
- 考虑测试执行的可行性
- 平衡测试覆盖率和资源限制

请按照以下 JSON 格式提供你的分析结果：
{
    "test_approach": {
        "methodology": [
            "测试方法1",
            "测试方法2"
        ],
        "tools": [
            "工具1",
            "工具2"
        ],
        "frameworks": [
            "框架1",
            "框架2"
        ]
    },
    "coverage_matrix": [
        {
            "feature": "功能点1",
            "test_type": "测试类型1"
        }
    ],
    "priorities": [
        {
            "level": "P0",
            "description": "关键功能描述"
        }
    ],
    "resource_estimation": {
        "time": "预计时间",
        "personnel": "所需人员",
        "tools": ["所需工具1", "所需工具2"],
        "additional_resources": ["其他资源1", "其他资源2"]
    }
}

注意：
1. 所有输出必须严格遵循上述 JSON 格式
2. 每个数组至少包含一个有效项
3. 所有文本必须使用双引号
4. JSON 必须是有效的且可解析的''',
            llm_config={"config_list": self.config_list}
        )
        
        # 添加last_design属性，用于跟踪最近的设计结果
        self.last_design = None
        
        # 尝试加载之前的设计结果
        self._load_last_design()

    def _load_last_design(self):
        """加载之前保存的设计结果"""
        try:
            result = self.agent_io.load_result("test_designer")
            if result:
                self.last_design = result
                logger.info("成功加载之前的测试设计结果")
        except Exception as e:
            logger.error(f"加载测试设计结果时出错: {str(e)}")
    
    def design(self, requirements: Dict) -> Dict:
        """基于分析后的需求设计测试策略。
        
        Args:
            requirements: 包含原始需求文档和需求分析结果的字典
                - original_doc: 原始需求文档
                - analysis_result: 需求分析结果
        """
        try:
            user_proxy = autogen.UserProxyAgent(
                name="user_proxy",
                system_message="需求提供者",
                human_input_mode="NEVER",
                code_execution_config={"use_docker": False}
            )

            # 创建测试策略
            user_proxy.initiate_chat(
                self.agent,
                message=f"""基于以下需求创建详细的测试策略：
                
                原始需求文档：
                {requirements.get('original_doc', '')}
                
                需求分析结果：
                功能需求：{requirements.get('analysis_result', {}).get('functional_requirements', [])}
                非功能需求：{requirements.get('analysis_result', {}).get('non_functional_requirements', [])}
                测试场景：{requirements.get('analysis_result', {}).get('test_scenarios', [])}
                风险领域：{requirements.get('analysis_result', {}).get('risk_areas', [])}
                
                请按照以下格式提供测试策略：
                
                1. 测试方法
                - 功能测试方法
                - 安全测试方法
                - 兼容性测试方法
                - 可用性测试方法
                
                2. 测试覆盖矩阵
                - 每个功能需求（不能简写，要如实描述需求）
                - 每个非功能需求的测试类型
                - 每个测试场景的覆盖方案
                - 风险领域的测试覆盖
                
                3. 测试优先级
                - P0：关键功能和高风险项
                - P1：核心业务功能
                - P2：重要但非核心功能
                - P3：次要功能
                - P4：低优先级功能
                
                4. 资源估算
                - 预计所需时间
                - 所需人员配置
                - 测试工具清单
                - 其他资源需求
                
                请直接提供分析结果，确保每个部分都有具体的内容和建议。""",
                max_turns=1  # 限制对话轮次为1，避免死循环
            )

            # 处理代理的响应
            response = self.agent.last_message()
            if not response:
                logger.warning("测试设计代理返回空响应")
                return {
                    "test_approach": {
                        "methodology": [],
                        "tools": [],
                        "frameworks": []
                    },
                    "coverage_matrix": [],
                    "priorities": [],
                    "resource_estimation": {
                        "time": None,
                        "personnel": None,
                        "tools": [],
                        "additional_resources": []
                    }
                }

            # 确保响应是字符串类型
            response_str = str(response) if response else ""
            if not response_str.strip():
                logger.warning("测试设计代理返回空响应")
                return {
                    "test_approach": {
                        "methodology": [],
                        "tools": [],
                        "frameworks": []
                    },
                    "coverage_matrix": [],
                    "priorities": [],
                    "resource_estimation": {
                        "time": None,
                        "personnel": None,
                        "tools": [],
                        "additional_resources": []
                    }
                }

            # 尝试解析JSON响应
            import json
            import re
            
            # 打印原始响应以便调试
            logger.info(f"AI响应内容: {response_str[:200]}...")  # 只打印前200个字符避免日志过长
            
            # 尝试从响应中提取JSON部分 - 支持多种格式
            json_match = re.search(r'```(?:json)?\s*({\s*".*?})\s*```', response_str, re.DOTALL)
            if not json_match:
                # 尝试直接从响应中查找JSON对象
                json_match = re.search(r'({[\s\S]*"test_approach"[\s\S]*})', response_str)
            
            if json_match:
                try:
                    # 提取JSON字符串并解析
                    json_str = json_match.group(1)
                    # 清理可能的格式问题
                    json_str = json_str.strip()
                    # print(f"json_str_type: {type(json_str)}  ")
                    json_str = re.sub(r'```json|```', '', json_str)
                    json_str = json_str.replace(r'\n', '\n').replace(r'\"', '"')
                    
                    # 尝试修复常见的JSON格式问题
                    json_str = self._fix_json_format(json_str)
                    
                    # 首先尝试直接解析JSON
                    try:
                        test_strategy = json.loads(json_str)
                        logger.info("成功直接解析JSON响应")
                    except json.JSONDecodeError as e:
                        logger.info(f"直接JSON解析失败: {str(e)}，尝试修复后重新解析")
                        # 尝试更强的JSON修复
                        json_str = self._fix_json_aggressive(json_str)
                        try:
                            test_strategy = json.loads(json_str)
                            logger.info("修复后JSON解析成功")
                        except json.JSONDecodeError:
                            logger.info("修复后JSON解析仍然失败，尝试Python字典格式解析")
                            # 尝试Python字典格式解析
                            try:
                                # print(f"content 的字符串内容：{json_str}")
                                json_str_fix = re.sub(r"'content':\s*'(.*?)'",  # 匹配content字段的值
                                    lambda m: "'content': '''{}'''".format(m.group(1).replace("'''", "\\'''")),  # 转换为三重引号
                                    json_str,
                                    flags=re.DOTALL
                                )
                                json_init_dict = ast.literal_eval(json_str_fix)
                                # print(f"json_init_dict 类型：{type(json_init_dict)}")
                                json_str = json.dumps(json_init_dict["content"])
                                test_strategy = json.loads(json_str)
                                logger.info("成功从Python字典格式解析测试策略")
                            except Exception as e:
                                logger.warning(f"Python字典格式解析失败: {str(e)}，尝试备用方法")
                                # 尝试备用JSON提取
                                test_strategy = self._extract_json_fallback(response_str)
                                if not test_strategy:
                                    logger.error("所有解析方法都失败了，记录详细信息用于调试")
                                    logger.error(f"原始响应内容: {response_str[:500]}...")
                                    logger.error(f"提取的JSON字符串: {json_str[:500]}...")
                                    logger.error(f"修复后的JSON字符串: {json_str[:500]}...")
                                    
                                    # 尝试最后的备用策略：从响应中提取关键信息
                                    test_strategy = self._extract_fallback_from_text(response_str)
                                    if not test_strategy:
                                        raise Exception("所有解析方法都失败了，包括文本提取备用策略")
                                    else:
                                        logger.info("文本提取备用策略成功")
                    
                    # 确保test_strategy是字典类型
                    if isinstance(test_strategy, str):
                        test_strategy = json.loads(test_strategy)
                    
                    # 保存设计结果到last_design属性
                    self.last_design = test_strategy
                    
                    # 将设计结果保存到文件
                    self.agent_io.save_result("test_designer", test_strategy)
            
                    logger.info("测试设计完成")

                    return test_strategy

                except Exception as e:
                    logger.error(f"测试设计错误: {str(e)}")
                    # 尝试更宽松的JSON提取
                    test_strategy = self._extract_json_fallback(response_str)
                    if test_strategy:
                        return test_strategy
                    
                    # 尝试文本提取备用策略
                    test_strategy = self._extract_fallback_from_text(response_str)
                    if test_strategy:
                        return test_strategy
                    
                    # 发生异常时返回默认结构
                    logger.warning("所有解析方法都失败，返回默认测试策略结构")
                    return {
                        "test_approach": {
                            "methodology": [],
                            "tools": [],
                            "frameworks": []
                        },
                        "coverage_matrix": [],
                        "priorities": [],
                        "resource_estimation": {
                            "time": None,
                            "personnel": None,
                            "tools": [],
                            "additional_resources": []
                        }
                    }
            else:
                # 如果无法提取JSON，返回默认结构
                logger.warning("无法从响应中提取JSON格式的测试策略")
                return {
                    "test_approach": {
                        "methodology": [],
                        "tools": [],
                        "frameworks": []
                    },
                    "coverage_matrix": [],
                    "priorities": [],
                    "resource_estimation": {
                        "time": None,
                        "personnel": None,
                        "tools": [],
                        "additional_resources": []
                    }
                }

        except Exception as e:
            logger.error(f"测试设计过程中出错: {str(e)}")
            # 发生异常时返回默认结构
            return {
                "test_approach": {
                    "methodology": [],
                    "tools": [],
                    "frameworks": []
                },
                "coverage_matrix": [],
                "priorities": [],
                "resource_estimation": {
                    "time": None,
                    "personnel": None,
                    "tools": [],
                    "additional_resources": []
                }
            }
    
    def _fix_json_format(self, json_str: str) -> str:
        """修复常见的JSON格式问题"""
        try:
            # 修复常见的引号问题
            json_str = re.sub(r'([^\\])"([^"]*?)([^\\])"', r'\1"\2\3"', json_str)
            
            # 修复可能的换行符问题
            json_str = json_str.replace('\n', '\\n').replace('\r', '\\r')
            
            # 修复可能的制表符问题
            json_str = json_str.replace('\t', '\\t')
            
            # 尝试修复不完整的JSON
            if json_str.strip().startswith('{') and not json_str.strip().endswith('}'):
                # 找到最后一个完整的键值对
                last_complete_pair = max(
                    json_str.rfind('",'),
                    json_str.rfind('"],'),
                    json_str.rfind('"},')
                )
                if last_complete_pair > 0:
                    json_str = json_str[:last_complete_pair+2] + '}'
            
            return json_str
        except Exception as e:
            logger.warning(f"JSON格式修复失败: {str(e)}")
            return json_str
    
    def _fix_json_aggressive(self, json_str: str) -> str:
        """更强的JSON修复方法，处理更严重的格式问题"""
        try:
            # 修复缺少逗号的问题
            # 在数组元素之间添加逗号
            json_str = re.sub(r'(\])\s*(\[)', r'\1,\2', json_str)
            
            # 在对象属性之间添加逗号
            json_str = re.sub(r'(")\s*(")', r'\1,\2', json_str)
            
            # 修复缺少引号的属性名
            json_str = re.sub(r'([{,])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', json_str)
            
            # 修复缺少引号的字符串值
            json_str = re.sub(r':\s*([a-zA-Z][a-zA-Z0-9\s]*?)([,}])', r': "\1"\2', json_str)
            
            # 修复数组中的字符串值
            json_str = re.sub(r'\[\s*([a-zA-Z][a-zA-Z0-9\s]*?)\s*([,\]])', r'["\1"\2', json_str)
            
            # 修复对象结尾缺少大括号
            if json_str.strip().startswith('{') and not json_str.strip().endswith('}'):
                # 尝试找到最后一个有效的属性
                last_valid_pos = max(
                    json_str.rfind('",'),
                    json_str.rfind('"],'),
                    json_str.rfind('"},'),
                    json_str.rfind('"')
                )
                if last_valid_pos > 0:
                    if json_str[last_valid_pos] == ',':
                        json_str = json_str[:last_valid_pos] + '}'
                    elif json_str[last_valid_pos] == '"':
                        json_str = json_str[:last_valid_pos+1] + '}'
                    else:
                        json_str = json_str[:last_valid_pos+2] + '}'
            
            # 修复数组结尾缺少方括号
            if json_str.strip().startswith('[') and not json_str.strip().endswith(']'):
                last_valid_pos = max(
                    json_str.rfind('",'),
                    json_str.rfind('},'),
                    json_str.rfind('"'),
                    json_str.rfind('}')
                )
                if last_valid_pos > 0:
                    if json_str[last_valid_pos] == ',':
                        json_str = json_str[:last_valid_pos] + ']'
                    elif json_str[last_valid_pos] in ['"', '}']:
                        json_str = json_str[:last_valid_pos+1] + ']'
                    else:
                        json_str = json_str[:last_valid_pos+2] + ']'
            
            return json_str
        except Exception as e:
            logger.warning(f"强JSON修复失败: {str(e)}")
            return json_str
    
    def _extract_json_fallback(self, response_str: str) -> Dict:
        """备用JSON提取方法，使用更宽松的匹配"""
        try:
            # 尝试查找包含关键字段的JSON对象
            patterns = [
                r'\{[^{}]*"test_approach"[^{}]*\}',
                r'\{[^{}]*"coverage_matrix"[^{}]*\}',
                r'\{[^{}]*"priorities"[^{}]*\}'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, response_str, re.DOTALL)
                if matches:
                    # 尝试扩展匹配到完整的JSON对象
                    for match in matches:
                        # 向前和向后扩展查找完整的JSON
                        start_pos = response_str.find(match)
                        if start_pos >= 0:
                            # 向前查找开始的大括号
                            brace_count = 0
                            start_brace = start_pos
                            for i in range(start_pos, -1, -1):
                                if response_str[i] == '{':
                                    brace_count += 1
                                elif response_str[i] == '}':
                                    brace_count -= 1
                                if brace_count == 1:
                                    start_brace = i
                                    break
                            
                            # 向后查找结束的大括号
                            brace_count = 0
                            end_brace = start_pos + len(match)
                            for i in range(start_pos + len(match), len(response_str)):
                                if response_str[i] == '{':
                                    brace_count += 1
                                elif response_str[i] == '}':
                                    brace_count -= 1
                                if brace_count == 0:
                                    end_brace = i + 1
                                    break
                            
                            # 提取完整的JSON
                            full_json = response_str[start_brace:end_brace]
                            try:
                                # 尝试修复和解析
                                fixed_json = self._fix_json_format(full_json)
                                parsed_result = json.loads(fixed_json)
                                if isinstance(parsed_result, dict):
                                    return self._build_structured_result(parsed_result)
                            except Exception:
                                continue
            
            return None
        except Exception as e:
            logger.warning(f"备用JSON提取失败: {str(e)}")
            return None
    
    def _build_structured_result(self, parsed_result: Dict) -> Dict:
        """构建结构化的测试策略结果"""
        return {
            "test_approach": {
                "methodology": parsed_result.get("methodology", []),
                "tools": parsed_result.get("tools", []),
                "frameworks": parsed_result.get("frameworks", [])
            },
            "coverage_matrix": parsed_result.get("coverage_matrix", []),
            "priorities": parsed_result.get("priorities", []),
            "resource_estimation": parsed_result.get("resource_estimation", {
                "time": None,
                "personnel": None,
                "tools": [],
                "additional_resources": []
            })
        }
    
    def _extract_fallback_from_text(self, response_str: str) -> Dict:
        """从文本响应中提取测试策略信息的备用方法"""
        try:
            logger.info("尝试从文本中提取测试策略信息")
            
            # 初始化默认结构
            test_strategy = {
                "test_approach": {
                    "methodology": [],
                    "tools": [],
                    "frameworks": []
                },
                "coverage_matrix": [],
                "priorities": [],
                "resource_estimation": {
                    "time": None,
                    "personnel": None,
                    "tools": [],
                    "additional_resources": []
                }
            }
            
            # 提取测试方法
            methodology_patterns = [
                r'测试方法[：:]\s*(.+)',
                r'测试策略[：:]\s*(.+)',
                r'测试方法包括[：:]\s*(.+)',
                r'采用.*?测试方法[：:]\s*(.+)'
            ]
            
            for pattern in methodology_patterns:
                matches = re.findall(pattern, response_str, re.IGNORECASE)
                if matches:
                    for match in matches:
                        # 分割多个方法
                        methods = re.split(r'[,，、;；]', match.strip())
                        for method in methods:
                            method = method.strip()
                            if method and len(method) > 2:
                                test_strategy["test_approach"]["methodology"].append(method)
                    break
            
            # 提取测试工具
            tools_patterns = [
                r'测试工具[：:]\s*(.+)',
                r'使用.*?工具[：:]\s*(.+)',
                r'工具包括[：:]\s*(.+)'
            ]
            
            for pattern in tools_patterns:
                matches = re.findall(pattern, response_str, re.IGNORECASE)
                if matches:
                    for match in matches:
                        tools = re.split(r'[,，、;；]', match.strip())
                        for tool in tools:
                            tool = tool.strip()
                            if tool and len(tool) > 2:
                                test_strategy["test_approach"]["tools"].append(tool)
                    break
            
            # 提取测试框架
            frameworks_patterns = [
                r'测试框架[：:]\s*(.+)',
                r'框架包括[：:]\s*(.+)',
                r'使用.*?框架[：:]\s*(.+)'
            ]
            
            for pattern in frameworks_patterns:
                matches = re.findall(pattern, response_str, re.IGNORECASE)
                if matches:
                    for match in matches:
                        frameworks = re.split(r'[,，、;；]', match.strip())
                        for framework in frameworks:
                            framework = framework.strip()
                            if framework and len(framework) > 2:
                                test_strategy["test_approach"]["frameworks"].append(framework)
                    break
            
            # 提取优先级信息
            priority_patterns = [
                r'优先级[：:]\s*(.+)',
                r'P[0-9][：:]\s*(.+)',
                r'高优先级[：:]\s*(.+)'
            ]
            
            for pattern in priority_patterns:
                matches = re.findall(pattern, response_str, re.IGNORECASE)
                if matches:
                    for match in matches:
                        priorities = re.split(r'[,，、;；]', match.strip())
                        for priority in priorities:
                            priority = priority.strip()
                            if priority and len(priority) > 2:
                                test_strategy["priorities"].append({
                                    "level": "P0",
                                    "description": priority
                                })
                    break
            
            # 如果没有提取到任何内容，添加默认值
            if not test_strategy["test_approach"]["methodology"]:
                test_strategy["test_approach"]["methodology"] = ["功能测试", "性能测试", "安全测试"]
            
            if not test_strategy["test_approach"]["tools"]:
                test_strategy["test_approach"]["tools"] = ["自动化测试工具", "性能测试工具"]
            
            if not test_strategy["test_approach"]["frameworks"]:
                test_strategy["test_approach"]["frameworks"] = ["测试框架"]
            
            if not test_strategy["priorities"]:
                test_strategy["priorities"] = [
                    {"level": "P0", "description": "关键功能测试"},
                    {"level": "P1", "description": "重要功能测试"}
                ]
            
            logger.info(f"从文本中提取的测试策略: {test_strategy}")
            return test_strategy
            
        except Exception as e:
            logger.error(f"文本提取备用策略失败: {str(e)}")
            return None

    def _extract_test_approach(self, message: str) -> Dict:
        """从代理消息中提取测试方法详情。"""
        test_approach = {
            'methodology': [],
            'tools': [],
            'frameworks': []
        }
        
        try:
            if not message:
                logger.warning("输入消息为空")
                return test_approach
                
            sections = message.split('\n')
            in_approach_section = False
            current_section = None
            
            for line in sections:
                try:
                    line = line.strip()
                    if not line:
                        continue
                        
                    if '1. 测试方法' in line:
                        in_approach_section = True
                        continue
                    elif '2. 测试覆盖矩阵' in line:
                        break
                    elif in_approach_section and not line.startswith('1.'):
                        # 分类方法详情
                        try:
                            # 检查是否是新的方法类型标题
                            if '功能测试' in line or '性能测试' in line or '安全测试' in line or '兼容性测试' in line or '可用性测试' in line:
                                current_section = line.strip()
                                test_approach['methodology'].append(current_section)
                            elif line.startswith('-') or line.startswith('*'):
                                # 提取具体的测试方法
                                content = line.strip('- *').strip()
                                if content:
                                    test_approach['methodology'].append(content)
                            elif '工具' in line.lower():
                                # 提取工具信息
                                if ':' in line or '：' in line:
                                    content = line.split(':', 1)[1].strip() if ':' in line else line.split('：', 1)[1].strip()
                                    test_approach['tools'].extend([t.strip() for t in content.split(',')])
                            elif '框架' in line.lower():
                                # 提取框架信息
                                if ':' in line or '：' in line:
                                    content = line.split(':', 1)[1].strip() if ':' in line else line.split('：', 1)[1].strip()
                                    test_approach['frameworks'].extend([f.strip() for f in content.split(',')])
                            elif current_section and line.strip():
                                # 将其他内容添加到当前部分
                                test_approach['methodology'].append(line.strip())
                        except IndexError as e:
                            logger.error(f"解析方法详情时出错: {str(e)}，行内容: {line}")
                            continue
                except Exception as e:
                    logger.error(f"处理单行内容时出错: {str(e)}，行内容: {line}")
                    continue
            
            # 去重并过滤空值
            test_approach['methodology'] = list(filter(None, set(test_approach['methodology'])))
            test_approach['tools'] = list(filter(None, set(test_approach['tools'])))
            test_approach['frameworks'] = list(filter(None, set(test_approach['frameworks'])))
            
            return test_approach
        except Exception as e:
            logger.error(f"提取测试方法错误: {str(e)}")
            return test_approach

    def _create_coverage_matrix(self, message: str) -> List[Dict]:
        """从代理消息中创建测试覆盖矩阵。"""
        coverage_matrix = []
        
        try:
            if not message:
                logger.warning("输入消息为空")
                return coverage_matrix
                
            sections = message.split('\n')
            in_matrix_section = False
            current_feature = None
            
            for line in sections:
                try:
                    line = line.strip()
                    if not line:
                        continue
                        
                    if '2. 测试覆盖矩阵' in line:
                        in_matrix_section = True
                        continue
                    elif '3. 测试优先级' in line:
                        break
                    elif in_matrix_section and not line.startswith('2.'):
                        try:
                            # 识别功能及其测试覆盖
                            if '|' in line:  # 处理表格格式
                                cells = [cell.strip() for cell in line.split('|')]
                                cells = [cell for cell in cells if cell]  # 移除空单元格
                                
                                if len(cells) >= 2:
                                    # 跳过表头和分隔行
                                    if not any(header in cells[0].lower() for header in ['需求类型', '用例编号', '-']):
                                        feature = cells[2] if len(cells) > 2 else cells[0]  # 使用描述列或第一列
                                        test_cases = cells[-1] if len(cells) > 3 else ''  # 使用最后一列作为测试用例
                                        
                                        if feature and test_cases:
                                            for test_case in test_cases.split(','):
                                                coverage_matrix.append({
                                                    'feature': feature.strip(),
                                                    'test_type': test_case.strip()
                                                })
                            elif line.strip().endswith(':') or line.strip().endswith('：'):
                                current_feature = line.strip().rstrip(':').rstrip('：').strip()
                            elif current_feature and any(line.strip().startswith(marker) for marker in ['-', '•', '*', '>', '+']):
                                test_type = line.strip()[1:].strip()
                                if test_type:  # 确保测试类型不为空
                                    coverage_matrix.append({
                                        'feature': current_feature,
                                        'test_type': test_type
                                    })
                            elif line.strip() and not any(marker in line for marker in ['测试覆盖', '覆盖矩阵']):
                                test_type = line.strip()
                                if current_feature and test_type:  # 确保特性和测试类型都不为空
                                    coverage_matrix.append({
                                        'feature': current_feature,
                                        'test_type': test_type
                                    })
                        except Exception as e:
                            logger.error(f"处理测试覆盖项时出错: {str(e)}，行内容: {line}")
                            continue
                except Exception as e:
                    logger.error(f"处理单行内容时出错: {str(e)}，行内容: {line}")
                    continue
            
            # 去重并过滤空值
            unique_matrix = []
            seen = set()
            for item in coverage_matrix:
                key = (item['feature'], item['test_type'])
                if key not in seen and item['feature'] and item['test_type']:
                    seen.add(key)
                    unique_matrix.append(item)
            
            return unique_matrix
        except Exception as e:
            logger.error(f"创建测试覆盖矩阵错误: {str(e)}")
            return coverage_matrix

    def _extract_priorities(self, message: str) -> List[Dict]:
        """从代理消息中提取测试优先级。"""
        priorities = []
        try:
            if not message:
                logger.warning("输入消息为空")
                return priorities
                
            sections = message.split('\n')
            in_priorities_section = False
            
            for line in sections:
                try:
                    line = line.strip()
                    if not line:
                        continue
                        
                    if '3. 测试优先级' in line:
                        in_priorities_section = True
                        continue
                    elif '4. 资源估算' in line:
                        break
                    elif in_priorities_section and not line.startswith('3.'):
                        try:
                            # 解析优先级和描述
                            if any(line.strip().lower().startswith(p) for p in ['p0', 'p1', 'p2', 'p3', 'p4']):
                                if ':' in line or '：' in line:
                                    priority, description = (line.split(':', 1) if ':' in line else line.split('：', 1))
                                    priority = priority.strip()
                                    description = description.strip()
                                    # 标准化优先级格式
                                    priority = f"P{priority[-1]}" if priority[-1].isdigit() else priority
                                    priorities.append({
                                        'level': priority.upper(),
                                        'description': description
                                    })
                        except (IndexError, ValueError) as e:
                            logger.error(f"解析优先级行时出错: {str(e)}，行内容: {line}")
                            continue
                except Exception as e:
                    logger.error(f"处理单行内容时出错: {str(e)}，行内容: {line}")
                    continue
            
            return priorities
        except Exception as e:
            logger.error(f"提取优先级错误: {str(e)}")
            return priorities

    def _extract_resource_estimation(self, message: str) -> Dict:
        """从代理消息中提取资源估算。"""
        resource_estimation = {
            'time': None,
            'personnel': None,
            'tools': [],
            'additional_resources': []
        }
        
        try:
            if not message:
                logger.warning("输入消息为空")
                return resource_estimation
                
            sections = message.split('\n')
            in_estimation_section = False
            
            for line in sections:
                try:
                    line = line.strip()
                    if not line:
                        continue
                        
                    if '4. 资源估算' in line:
                        in_estimation_section = True
                        continue
                    elif line.startswith('5.') or not line.strip():
                        break
                    elif in_estimation_section and not line.startswith('4.'):
                        try:
                            # 解析资源详情
                            if '时间:' in line.lower() or '时间：' in line:
                                resource_estimation['time'] = line.split(':', 1)[1].strip() if ':' in line else line.split('：', 1)[1].strip()
                            elif '人员:' in line.lower() or '人员：' in line:
                                resource_estimation['personnel'] = line.split(':', 1)[1].strip() if ':' in line else line.split('：', 1)[1].strip()
                            elif '工具:' in line.lower() or '工具：' in line:
                                tools = line.split(':', 1)[1].strip() if ':' in line else line.split('：', 1)[1].strip()
                                resource_estimation['tools'].append(tools)
                            else:
                                resource_estimation['additional_resources'].append(line.strip())
                        except IndexError as e:
                            logger.error(f"解析资源详情时出错: {str(e)}，行内容: {line}")
                            continue
                except Exception as e:
                    logger.error(f"处理单行内容时出错: {str(e)}，行内容: {line}")
                    continue
            
            return resource_estimation
        except Exception as e:
            logger.error(f"提取资源估算错误: {str(e)}")
            return resource_estimation