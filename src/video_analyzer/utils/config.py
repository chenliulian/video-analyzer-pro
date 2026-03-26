#!/usr/bin/env python3
"""
配置管理模块 - 统一管理项目配置
"""
import os
from typing import Optional, Dict, Any
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Config:
    """配置管理类"""
    
    # 默认配置
    DEFAULTS = {
        # LLM 配置
        "LLM_API_KEY": None,
        "LLM_BASE_URL": "https://api.openai.com/v1",
        "LLM_MODEL": "gpt-4",
        
        # OCR 配置
        "DASHSCOPE_API_KEY": None,
        "QWEN_OCR_MODEL": "qwen-vl-max",
        
        # ASR 配置
        "ASR_ENGINE": "whisper",
        "ASR_REGION": "intl",
        "ASR_LANGUAGE": "zh",
        
        # 视频处理配置
        "SCENE_THRESHOLD": 30,
        "MIN_INTERVAL": 5.0,
        "WHISPER_MODEL": "base",
    }
    
    def __init__(self):
        """初始化配置"""
        self._config = {}
        self._load_from_env()
    
    def _load_from_env(self):
        """从环境变量加载配置"""
        for key in self.DEFAULTS.keys():
            env_value = os.getenv(key)
            if env_value is not None:
                self._config[key] = env_value
            else:
                self._config[key] = self.DEFAULTS[key]
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项
        
        参数:
            key: 配置键名
            default: 默认值
            
        返回:
            配置值
        """
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """
        设置配置项
        
        参数:
            key: 配置键名
            value: 配置值
        """
        self._config[key] = value
    
    def get_llm_config(self) -> Dict[str, Optional[str]]:
        """
        获取LLM配置
        
        返回:
            LLM配置字典
        """
        return {
            "api_key": self.get("LLM_API_KEY"),
            "base_url": self.get("LLM_BASE_URL"),
            "model": self.get("LLM_MODEL"),
        }
    
    def get_ocr_config(self) -> Dict[str, Optional[str]]:
        """
        获取OCR配置
        
        返回:
            OCR配置字典
        """
        return {
            "api_key": self.get("DASHSCOPE_API_KEY"),
            "model": self.get("QWEN_OCR_MODEL"),
        }
    
    def get_asr_config(self) -> Dict[str, Any]:
        """
        获取ASR配置
        
        返回:
            ASR配置字典
        """
        return {
            "api_key": self.get("DASHSCOPE_API_KEY"),
            "region": self.get("ASR_REGION"),
            "language": self.get("ASR_LANGUAGE"),
            "engine": self.get("ASR_ENGINE"),
        }


# 全局配置实例
_config_instance = None


def get_config() -> Config:
    """
    获取全局配置实例
    
    返回:
        Config实例
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance


def load_config(config_file: Optional[str] = None) -> Config:
    """
    加载配置文件
    
    参数:
        config_file: 配置文件路径
        
    返回:
        Config实例
    """
    config = get_config()
    
    if config_file and Path(config_file).exists():
        # 可以扩展支持JSON/YAML配置文件
        pass
    
    return config


def get_api_key(service: str) -> Optional[str]:
    """
    获取API密钥
    
    参数:
        service: 服务名称 ('llm', 'ocr', 'asr')
        
    返回:
        API密钥
    """
    config = get_config()
    
    if service == "llm":
        return config.get("LLM_API_KEY")
    elif service in ("ocr", "asr"):
        return config.get("DASHSCOPE_API_KEY")
    
    return None
