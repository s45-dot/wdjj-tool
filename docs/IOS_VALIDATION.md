# iOS capInsets 验证指南
## 使用方法
1. 导出 ZIP 后取出 source PNG 和 ios/ios_cap_insets.json
2. 把 PNG 加入 Xcode Assets.xcassets
3. 读取 JSON 中的 capInsetsPt 值（注意用 pt 不是 px）
4. 使用 UIImage.resizableImage(withCapInsets:resizingMode:.stretch)
5. 设置到 UIImageView 或 UIButton 背景
## 验证清单
- UIImageView 单行：capInsets 正确，圆角不变
- UIImageView 多行：纵向拉伸正常
- UIButton 背景：padding 正确
- scale=1：pt=px
- scale=2：pt=px/2
- scale=3：pt=px/3
- 带尾巴气泡：尾巴不变形
- 透明背景：检查透明通道
## 注意事项
- 必须用 pt 值，不是 px
- resizingMode 用 .stretch 不用 .tile