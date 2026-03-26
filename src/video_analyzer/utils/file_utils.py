#!/usr/bin/env python3
"""
文件工具模块 - 常用文件操作
"""
import os
from pathlib import Path
from typing import Optional, Union


def ensure_dir(path: Union[str, Path]) -> Path:
    """
    确保目录存在，如果不存在则创建
    
    参数:
        path: 目录路径
        
    返回:
        Path对象
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_video_duration(video_path: Union[str, Path]) -> Optional[float]:
    """
    获取视频时长
    
    参数:
        video_path: 视频文件路径
        
    返回:
        视频时长（秒），失败返回None
    """
    try:
        import cv2
        video = cv2.VideoCapture(str(video_path))
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        video.release()
        return duration
    except Exception as e:
        print(f"获取视频时长失败: {e}")
        return None


def get_file_size(path: Union[str, Path]) -> float:
    """
    获取文件大小（MB）
    
    参数:
        path: 文件路径
        
    返回:
        文件大小（MB）
    """
    try:
        size_bytes = Path(path).stat().st_size
        return size_bytes / (1024 * 1024)
    except Exception:
        return 0.0


def safe_filename(filename: str) -> str:
    """
    生成安全的文件名
    
    参数:
        filename: 原始文件名
        
    返回:
        安全的文件名
    """
    # 移除或替换不安全字符
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    return filename


def find_video_files(directory: Union[str, Path], 
                     extensions: tuple = ('.mp4', '.avi', '.mov', '.mkv')) -> list:
    """
    查找目录中的视频文件
    
    参数:
        directory: 目录路径
        extensions: 视频文件扩展名元组
        
    返回:
        视频文件路径列表
    """
    directory = Path(directory)
    video_files = []
    
    for ext in extensions:
        video_files.extend(directory.glob(f'*{ext}'))
    
    return sorted(video_files)


def cleanup_temp_files(temp_dir: Union[str, Path], pattern: str = '*') -> int:
    """
    清理临时文件
    
    参数:
        temp_dir: 临时目录
        pattern: 文件匹配模式
        
    返回:
        删除的文件数量
    """
    temp_dir = Path(temp_dir)
    count = 0
    
    if temp_dir.exists():
        for file_path in temp_dir.glob(pattern):
            try:
                if file_path.is_file():
                    file_path.unlink()
                    count += 1
            except Exception:
                pass
    
    return count
