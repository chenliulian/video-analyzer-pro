import cv2, numpy as np

def calc_diff(f1, f2):
    hsv1 = cv2.cvtColor(f1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(f2, cv2.COLOR_BGR2HSV)
    hist1 = cv2.calcHist([hsv1], [0, 1], None, [50, 60], [0, 180, 0, 256])
    hist2 = cv2.calcHist([hsv2], [0, 1], None, [50, 60], [0, 180, 0, 256])
    cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    hist_diff = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA) * 100
    gray1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)
    edges1 = cv2.Canny(gray1, 50, 150)
    edges2 = cv2.Canny(gray2, 50, 150)
    small_edges1 = cv2.resize(edges1, (64, 64))
    small_edges2 = cv2.resize(edges2, (64, 64))
    edge_diff = np.abs(small_edges1.astype(np.float32) - small_edges2.astype(np.float32)).mean() / 2.55
    brightness_diff = abs(gray1.mean() - gray2.mean()) / 2.55
    return hist_diff * 0.5 + edge_diff * 0.3 + brightness_diff * 0.2

f1 = cv2.imread('extracted_frames/frame_0020_101.00s.jpg')
f2 = cv2.imread('extracted_frames/frame_0021_106.00s.jpg')
f3 = cv2.imread('extracted_frames/frame_0022_111.00s.jpg')

print('PDF第21-23页相似度检查:')
d12 = calc_diff(f1,f2)
d23 = calc_diff(f2,f3)
d13 = calc_diff(f1,f3)
print(f'21<->22: {d12:.2f} - {"✓不重复" if d12 >= 3 else "❌重复"}')
print(f'22<->23: {d23:.2f} - {"✓不重复" if d23 >= 3 else "❌重复"}')
print(f'21<->23: {d13:.2f} - {"✓不重复" if d13 >= 3 else "❌重复"}')
