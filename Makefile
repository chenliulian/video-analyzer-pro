.PHONY: help install install-dev test lint format clean run example

help:
	@echo "VideoAnalyzer Pro - 可用命令:"
	@echo ""
	@echo "  make install      - 安装项目依赖"
	@echo "  make install-dev  - 安装开发依赖"
	@echo "  make test         - 运行测试"
	@echo "  make lint         - 运行代码检查"
	@echo "  make format       - 格式化代码"
	@echo "  make clean        - 清理临时文件"
	@echo "  make run          - 运行示例 (需要配置.env)"
	@echo ""

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=src/video_analyzer --cov-report=html

lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .pytest_cache/ .mypy_cache/ .coverage htmlcov/

run:
	python main.py --video data/example.mp4

example:
	@echo "请先将视频文件放入 data/ 目录"
	@echo "然后运行: make run"
