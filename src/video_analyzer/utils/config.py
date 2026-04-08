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
        
        # OCR 配置 (使用 Kimi)
        "OCR_API_KEY": None,  # 默认使用 LLM_API_KEY
        "OCR_BASE_URL": None,  # 默认使用 LLM_BASE_URL
        "OCR_MODEL": "kimi-k2.5",
        
        # ASR 配置
        "ASR_ENGINE": "whisper",  # whisper, kimi
        "ASR_API_KEY": None,  # 默认使用 LLM_API_KEY
        "ASR_BASE_URL": None,  # 默认使用 LLM_BASE_URL
        "ASR_MODEL": "kimi-k2.5",
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
                # 尝试转换为合适的类型
                default_value = self.DEFAULTS[key]
                if isinstance(default_value, bool):
                    self._config[key] = env_value.lower() in ('true', '1', 'yes', 'on')
                elif isinstance(default_value, int):
                    self._config[key] = int(env_value)
                elif isinstance(default_value, float):
                    self._config[key] = float(env_value)
                else:
                    self._config[key] = env_value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项
        
        参数:
            key: 配置项名称
            default: 默认值
            
        返回:
            配置项值
        """
        # 首先检查 _config
        if key in self._config:
            return self._config[key]
        
        # 然后检查 DEFAULTS
        if key in self.DEFAULTS:
            return self.DEFAULTS[key]
        
        return default
    
    def get_llm_config(self) -> Dict[str, Optional[str]]:
        """获取LLM配置"""
        return {
            "api_key": self.get("LLM_API_KEY"),
            "base_url": self.get("LLM_BASE_URL"),
            "model": self.get("LLM_MODEL"),
        }
    
    def get_ocr_config(self) -> Dict[str, Optional[str]]:
        """获取OCR配置"""
        return {
            "api_key": self.get("OCR_API_KEY") or self.get("LLM_API_KEY"),
            "base_url": self.get("OCR_BASE_URL") or self.get("LLM_BASE_URL"),
            "model": self.get("OCR_MODEL", "kimi-k2.5"),
        }
    
    def get_asr_config(self) -> Dict[str, Any]:
        """获取ASR配置"""
        return {
            "engine": self.get("ASR_ENGINE", "whisper"),
            "api_key": self.get("ASR_API_KEY") or self.get("LLM_API_KEY"),
            "base_url": self.get("ASR_BASE_URL") or self.get("LLM_BASE_URL"),
            "model": self.get("ASR_MODEL", "kimi-k2.5"),
            "language": self.get("ASR_LANGUAGE", "zh"),
        }
    
    def set(self, key: str, value: Any):
        """设置配置项"""
        self._config[key] = value
    
    def __getitem__(self, key: str) -> Any:
        """支持字典式访问"""
        return self.get(key)
    
    def __setitem__(self, key: str, value: Any):
        """支持字典式设置"""
        self.set(key, value)


# 全局配置实例
config = Config()
