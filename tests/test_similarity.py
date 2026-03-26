#!/usr/bin/env python3
"""
测试不同的图像相似度计算方法
"""
import os
import sys
import time
import cv2
import numpy as np
from PIL import Image
from pathlib import Path


def method1_simple_mse(img1, img2):
    """方法1: 简单的均方误差(MSE)"""
    gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    small1 = cv2.resize(gray1, (64, 64))
    small2 = cv2.resize(gray2, (64, 64))
    diff = np.abs(small1.astype(np.float32) - small2.astype(np.float32)).mean()
    return diff


def method2_histogram(img1, img2):
    """方法2: 直方图比较 - 更好地检测颜色变化"""
    # 转换为HSV色彩空间
    hsv1 = cv2.cvtColor(img1, cv2.COLOR_RGB2HSV)
    hsv2 = cv2.cvtColor(img2, cv2.COLOR_RGB2HSV)
    
    # 计算直方图
    hist1 = cv2.calcHist([hsv1], [0, 1], None, [50, 60], [0, 180, 0, 256])
    hist2 = cv2.calcHist([hsv2], [0, 1], None, [50, 60], [0, 180, 0, 256])
    
    # 归一化
    cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    
    # 使用巴氏距离(Bhattacharyya distance)
    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
    # 转换为差异度(0-1,越大越不同)
    return similarity * 100


def method3_structural_similarity(img1, img2):
    """方法3: 结构相似性(SSIM) - 考虑亮度、对比度和结构"""
    gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    
    # 缩小以加快计算
    small1 = cv2.resize(gray1, (128, 128))
    small2 = cv2.resize(gray2, (128, 128))
    
    # 计算SSIM
    # SSIM返回值在-1到1之间,1表示完全相同
    C1 = (0.01 * 255) ** 2
    C2 = (0.03 * 255) ** 2
    
    mu1 = cv2.GaussianBlur(small1.astype(np.float32), (11, 11), 1.5)
    mu2 = cv2.GaussianBlur(small2.astype(np.float32), (11, 11), 1.5)
    
    mu1_sq = mu1 ** 2
    mu2_sq = mu2 ** 2
    mu1_mu2 = mu1 * mu2
    
    sigma1_sq = cv2.GaussianBlur(small1.astype(np.float32) ** 2, (11, 11), 1.5) - mu1_sq
    sigma2_sq = cv2.GaussianBlur(small2.astype(np.float32) ** 2, (11, 11), 1.5) - mu2_sq
    sigma12 = cv2.GaussianBlur(small1.astype(np.float32) * small2.astype(np.float32), (11, 11), 1.5) - mu1_mu2
    
    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))
    ssim_value = ssim_map.mean()
    
    # 转换为差异度(0-100,越大越不同)
    return (1 - ssim_value) * 100


def method4_phash(img1, img2):
    """方法4: 感知哈希(pHash) - 对图像变换更鲁棒"""
    def compute_phash(img):
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        resized = cv2.resize(gray, (32, 32))
        dct = cv2.dct(resized.astype(np.float32))
        dct_low = dct[:8, :8]
        avg = dct_low.mean()
        hash_value = (dct_low > avg).flatten()
        return hash_value
    
    hash1 = compute_phash(img1)
    hash2 = compute_phash(img2)
    
    # 计算汉明距离
    hamming_distance = np.sum(hash1 != hash2)
    # 归一化到0-100
    return (hamming_distance / 64) * 100


def method5_combined(img1, img2):
    """方法5: 组合方法 - 结合多种特征"""
    # 1. 直方图相似度
    hist_diff = method2_histogram(img1, img2)
    
    # 2. 边缘检测相似度
    gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    edges1 = cv2.Canny(gray1, 50, 150)
    edges2 = cv2.Canny(gray2, 50, 150)
    small_edges1 = cv2.resize(edges1, (64, 64))
    small_edges2 = cv2.resize(edges2, (64, 64))
    edge_diff = np.abs(small_edges1.astype(np.float32) - small_edges2.astype(np.float32)).mean() / 2.55
    
    # 3. 亮度差异
    brightness_diff = abs(gray1.mean() - gray2.mean()) / 2.55
    
    # 加权组合
    combined = hist_diff * 0.5 + edge_diff * 0.3 + brightness_diff * 0.2
    return combined


def test_similarity_methods(frames_folder, sample_size=50):
    """测试不同的相似度计算方法"""
    print("=" * 70)
    print("图像相似度算法测试")
    print("=" * 70)
    
    # 获取所有帧文件
    frame_files = sorted([f for f in os.listdir(frames_folder) if f.endswith('.jpg')])
    
    if len(frame_files) < 2:
        print("帧文件太少,无法测试")
        return
    
    # 限制样本数量
    if len(frame_files) > sample_size:
        step = len(frame_files) // sample_size
        frame_files = frame_files[::step]
    
    print(f"\n测试样本: {len(frame_files)} 张图片")
    print(f"来源文件夹: {frames_folder}\n")
    
    methods = {
        '方法1-简单MSE': method1_simple_mse,
        '方法2-直方图': method2_histogram,
        '方法3-SSIM': method3_structural_similarity,
        '方法4-pHash': method4_phash,
        '方法5-组合': method5_combined,
    }
    
    results = {name: {'times': [], 'diffs': [], 'consecutive_diffs': []} for name in methods}
    
    print("正在计算相似度...\n")
    
    prev_frames = {}
    for name in methods:
        prev_frames[name] = None
    
    for i, frame_file in enumerate(frame_files):
        frame_path = os.path.join(frames_folder, frame_file)
        frame = cv2.imread(frame_path)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        for method_name, method_func in methods.items():
            start_time = time.time()
            
            if prev_frames[method_name] is not None:
                diff = method_func(prev_frames[method_name], frame)
                results[method_name]['diffs'].append(diff)
                
                # 记录连续帧的差异
                if i > 0 and i < len(frame_files):
                    results[method_name]['consecutive_diffs'].append(diff)
            
            elapsed = time.time() - start_time
            results[method_name]['times'].append(elapsed)
            prev_frames[method_name] = frame
        
        if (i + 1) % 10 == 0:
            print(f"  已处理 {i + 1}/{len(frame_files)} 张图片...")
    
    # 打印结果
    print("\n" + "=" * 70)
    print("测试结果分析")
    print("=" * 70)
    
    for method_name, data in results.items():
        print(f"\n【{method_name}】")
        print(f"  平均处理时间: {np.mean(data['times']) * 1000:.2f} ms")
        
        if data['consecutive_diffs']:
            diffs = np.array(data['consecutive_diffs'])
            print(f"  连续帧差异统计:")
            print(f"    - 平均值: {diffs.mean():.2f}")
            print(f"    - 中位数: {np.median(diffs):.2f}")
            print(f"    - 标准差: {diffs.std():.2f}")
            print(f"    - 最小值: {diffs.min():.2f}")
            print(f"    - 最大值: {diffs.max():.2f}")
            print(f"    - 25分位: {np.percentile(diffs, 25):.2f}")
            print(f"    - 75分位: {np.percentile(diffs, 75):.2f}")
    
    # 推荐阈值
    print("\n" + "=" * 70)
    print("推荐阈值设置")
    print("=" * 70)
    
    for method_name, data in results.items():
        if data['consecutive_diffs']:
            diffs = np.array(data['consecutive_diffs'])
            # 使用75分位数作为阈值,可以过滤掉大部分相似帧
            recommended_threshold = np.percentile(diffs, 75)
            print(f"\n{method_name}:")
            print(f"  推荐阈值: {recommended_threshold:.1f}")
            print(f"  说明: 差异大于此值的帧会被保存")
            
            # 估算保留率
            kept_rate = (diffs > recommended_threshold).sum() / len(diffs) * 100
            print(f"  预计保留: {kept_rate:.1f}% 的帧")


def compare_consecutive_frames(frames_folder, num_samples=10):
    """可视化对比连续帧的差异"""
    print("\n" + "=" * 70)
    print("连续帧对比分析")
    print("=" * 70)
    
    frame_files = sorted([f for f in os.listdir(frames_folder) if f.endswith('.jpg')])[:num_samples+1]
    
    if len(frame_files) < 2:
        return
    
    print(f"\n分析前 {num_samples} 对连续帧...\n")
    
    for i in range(min(num_samples, len(frame_files) - 1)):
        frame1_path = os.path.join(frames_folder, frame_files[i])
        frame2_path = os.path.join(frames_folder, frame_files[i + 1])
        
        frame1 = cv2.imread(frame1_path)
        frame2 = cv2.imread(frame2_path)
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        
        print(f"对比 {frame_files[i]} vs {frame_files[i+1]}")
        print(f"  简单MSE:  {method1_simple_mse(frame1, frame2):.2f}")
        print(f"  直方图:   {method2_histogram(frame1, frame2):.2f}")
        print(f"  SSIM:     {method3_structural_similarity(frame1, frame2):.2f}")
        print(f"  pHash:    {method4_phash(frame1, frame2):.2f}")
        print(f"  组合方法: {method5_combined(frame1, frame2):.2f}")
        print()


def main():
    frames_folder = "extracted_frames"
    
    if not os.path.exists(frames_folder):
        print(f"错误: 找不到文件夹 {frames_folder}")
        print("请先运行 video_analyzer.py 提取帧")
        sys.exit(1)
    
    # 测试相似度方法
    test_similarity_methods(frames_folder, sample_size=100)
    
    # 对比连续帧
    compare_consecutive_frames(frames_folder, num_samples=10)
    
    print("\n" + "=" * 70)
    print("结论和建议")
    print("=" * 70)
    print("""
基于测试结果:
1. 如果视频内容变化较大(如PPT翻页、场景切换): 使用"方法2-直方图"或"方法5-组合"
2. 如果视频内容变化细微(如讲师移动、文字标注): 使用"方法3-SSIM"或"方法5-组合"
3. 如果追求速度: 使用"方法1-简单MSE"或"方法4-pHash"
4. 推荐: 使用"方法5-组合",平衡准确度和性能

建议阈值设置:
- 严格过滤(提取更少): 使用75-90分位数
- 平衡过滤(推荐): 使用50-75分位数
- 宽松过滤(提取更多): 使用25-50分位数
""")


if __name__ == "__main__":
    main()
