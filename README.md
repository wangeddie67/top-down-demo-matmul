# top-down-demo-matmul

这个项目包括给本人知乎关于Top-down性能分析方法学专题的相关示例和图片的源码。

知乎链接：
- [Intel Top-down方法学综述](https://zhuanlan.zhihu.com/p/638160179)
- [Intel Top-down示例 优化矩阵乘法性能](https://zhuanlan.zhihu.com/p/638172567)

## 示例

首先运行make，可以编译生成配置并运行topdown。每一个配置生成一个可执行文件、反汇编文件.diss和top-down报告.csv。然后用configure.py收集数据。

配置可以单独运行，例如make op2等。

## 动画gif

进入figures/manim路径，运行：

```
manim -i -ql matmul_kmn.py MatmulKmn
manim -i -ql matmul_mkn.py MatmulMkn
manim -i -ql matmul_mnk.py MatmulMnk
manim -i -ql matmul_knmkn.py MatmulKnmkn
```
