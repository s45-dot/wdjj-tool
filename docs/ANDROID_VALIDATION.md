# Android .9.png 验证指南

## 使用方法

1. 导出 ZIP 后取出 android/bubble.9.png
2. 放入 Android 项目 res/drawable/
3. 在 TextView 中使用 android:background="@drawable/bubble"
4. 在 View 中使用 android:background="@drawable/bubble"

## 验证清单

- 单行短文本：padding 正常，圆角不变形
- 长文本单行：横向拉伸，圆角不变形
- 多行文本：纵向拉伸正常
- 极窄宽度：不崩溃
- 极高高度：不崩溃
- 带尾巴气泡：尾巴不变形
- 透明背景：检查透明通道

## 注意事项

- .9.png 外层 1px 黑线不要裁掉
- padding 由 contentInsets 控制