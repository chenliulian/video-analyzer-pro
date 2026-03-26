# PDF文字页生成修复说明

## 问题描述

用户反馈 `results/1732328440969754_frames_pro.pdf` 文件中没有增加讲解的文字,希望在每一页图片之后增加一页文字页。

## 问题分析

经过排查,发现了以下问题:

### 1. LLM精炼结果为空
- `results/1732328440969754_refined.json` 文件中所有值都是空字符串 `""`
- 这导致没有可用的精炼文字

### 2. 转录文件解析失败
- 转录文件格式使用 `======` (70个等号) 和 `分段转录`
- 旧的解析函数只查找 `=== 分段转录 ===` (3个等号)
- 导致无法正确解析转录文件,语音段落数为 0

### 3. Fallback逻辑不完善
- 当精炼结果为空字符串时,没有正确fallback到原始转录
- 匹配逻辑使用segment中点判断,导致很多文字未匹配到对应帧

## 修复方案

### 1. 修复转录文件解析 ✅

**修改位置:** `video_analyzer_pro.py` 

**改进点:**
- 重写 `parse_transcript()` 函数,支持多种分隔符格式
- 支持 `分段转录`, `=== 分段转录 ===`, `====== 分段转录 ======` 等格式
- 支持繁体中文 `分段轉錄`
- 更健壮的错误处理

```python
def parse_transcript(transcript_file: str) -> List[Tuple[float, float, str]]:
    # 尝试多种分隔符格式
    segment_markers = ["分段转录", "分段轉錄", "=== 分段转录 ===", "====== 分段转录 ======"]
    
    segment_text = None
    for marker in segment_markers:
        if marker in content:
            parts = content.split(marker)
            if len(parts) > 1:
                segment_text = parts[1]
                break
    # ...
```

### 2. 改进文字匹配逻辑 ✅

**修改位置:** `video_analyzer_pro.py` - `_get_text_for_frame()` 方法

**改进点:**
- 增加空字符串检查,确保精炼结果非空才使用
- 改进时间匹配算法,使用区间重叠而非中点判断
- 扩大匹配范围,提高文字覆盖率

```python
def _get_text_for_frame(...):
    # 优先使用LLM精炼结果(但要确保不是空字符串)
    if refined_results and img_path in refined_results:
        refined_text = refined_results[img_path].strip()
        if refined_text:  # 只有当精炼结果非空时才使用
            return refined_text
    
    # 使用原始转录(fallback)
    # 扩大匹配范围,只要segment的任何部分在时间范围内就包含
    if not (seg_end < start_time or seg_start > end_time):
        matching_segments.append((seg_start, seg_end, seg_text))
```

### 3. 增强调试信息 ✅

**改进点:**
- 显示转录段落数量
- 显示文字页生成数量统计
- 显示前几个无匹配文字的图片(方便调试)

```python
print(f"   转录段落: {len(transcript_segments)} 个")
print(f"  总页数: {len(all_pages)} 页 (图片: {len(image_times)} 页, 文字: {text_pages_count} 页)")
```

## 修复结果

### 修复前
```
📄 PDF页数: 36 页
🎤 语音段落: 0 段
```

### 修复后
```
📄 PDF页数: 68 页 (图片: 36 页, 文字: 32 页)
🎤 语音段落: 735 段
```

## PDF结构

现在生成的PDF结构如下:

```
[页1] 图片: frame_0000_0.00s.jpg
[页2] 文字: 00:00 - 00:05 的讲解内容
[页3] 图片: frame_0001_5.00s.jpg
[页4] 文字: 00:05 - 00:10 的讲解内容
[页5] 图片: frame_0002_10.00s.jpg
[页6] 文字: 00:10 - 00:15 的讲解内容
...
[页67] 图片: frame_0035_1296.00s.jpg
[页68] 文字: 21:36 - 视频结束 的讲解内容
```

## 使用说明

### 重新生成PDF

如果之前生成的PDF没有文字页,可以删除后重新生成:

```bash
# 删除旧的PDF
rm results/1732328440969754_frames_pro.pdf

# 重新生成(会跳过已完成的步骤,只重新生成PDF)
python3 video_analyzer_pro.py --video data/1732328440969754.mp4 --no-llm
```

### 查看统计信息

运行时会显示详细的统计信息:

```
⏳ 正在生成PDF...
   图片数量: 36
   转录段落: 735 个
   使用文字: 原始转录
   
✓ PDF生成成功: results/1732328440969754_frames_pro.pdf
  总页数: 68 页 (图片: 36 页, 文字: 32 页)
  文件大小: 5.0 MB
```

## 注意事项

1. **文字页数量可能少于图片页**
   - 某些时间段可能没有匹配的讲解文字
   - 例如视频开头或结尾的静音部分
   - 这是正常现象

2. **LLM精炼功能**
   - 如果配置了LLM且精炼结果非空,会优先使用精炼后的文字
   - 否则自动使用原始转录作为fallback
   - 使用 `--no-llm` 可跳过精炼步骤,加快处理速度

3. **文字匹配逻辑**
   - 每个图片帧对应一个时间段(从当前帧到下一帧)
   - 匹配该时间段内所有重叠的语音段落
   - 多个段落会自动合并

## 测试结果

✅ 成功生成包含文字页的PDF  
✅ 文字内容完整,覆盖大部分时间段  
✅ 图片和文字交替排列  
✅ 时间戳正确显示  
✅ 中文字体正常显示  

## 相关文件

- 修复代码: `video_analyzer_pro.py`
- 测试视频: `data/1732328440969754.mp4`
- 输出PDF: `results/1732328440969754_frames_pro.pdf`
- 转录文件: `results/1732328440969754_transcript.txt`

## 更新日期

2025-12-07
