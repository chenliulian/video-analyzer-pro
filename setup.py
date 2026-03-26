#!/usr/bin/env python3
"""
VideoAnalyzer Pro - 安装脚本
兼容旧版pip安装
"""

from setuptools import setup, find_packages

setup(
    name="video-analyzer-pro",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
)
