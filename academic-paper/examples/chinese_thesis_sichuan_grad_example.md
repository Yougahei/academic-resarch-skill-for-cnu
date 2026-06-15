# 四川大学硕士/博士学位论文示例

本示例展示一份完整的四川大学学位论文 markdown 输入文件。这份文件可以在 ARS 管道的阶段 ⑨（FINALIZE）中通过 `format-convert` 模式处理，输出符合四川大学格式规范的 DOCX 文件。

> **本文内容为 AI 生成的示范文本。** 所有数据、统计结果均为虚构，仅用于展示格式结构。请勿引用本文内容作为学术依据。

---

## 封面信息

```yaml
title: "基于深度学习的遥感图像语义分割方法研究"
title_en: "Research on Semantic Segmentation Methods for Remote Sensing Images Based on Deep Learning"
author: "王强"
student_id: "2024220001"
school: "电子信息学院"
major: "信息与通信工程"
direction: "图像处理与计算机视觉"
advisor: "陈明教授"
degree: "硕士"
date: "二〇二六年四月"
```

> **格式提示：** 四川大学学位论文封面包含学校名称、论文题目（小二号宋体）、作者姓名、培养单位、指导教师、专业、研究方向等信息。封面在阶段 ⑨ 自动生成。

---

## 声  明

本人声明所呈交的学位论文是本人在导师指导下进行的研究工作及取得的研究成果。据我所知，除了文中特别加以标注和致谢的地方外，论文中不包含其他人已经发表或撰写过的研究成果，也不包含为获得四川大学或其他教育机构的学位或证书而使用过的材料。与我一同工作的同志对本研究所做的任何贡献均已在论文中作了明确的说明并表示谢意。

本学位论文成果是本人在四川大学读书期间在导师指导下取得的，论文成果归四川大学所有，特此声明。

作者签名：                    导师签名：

                                  年    月    日

## 学位论文使用授权书

本学位论文作者完全了解四川大学有关保留、使用学位论文的规定，同意学校保留并向国家有关部门或相关机构送交论文的原件、复印件和电子版，允许论文被查阅和借阅。本人授权四川大学将本学位论文的全部或部分内容编入有关数据库进行信息技术服务，可以采用影印、缩印或扫描等复制手段保存、汇编学位论文，并用于学术活动。

（涉密学位论文在解密后适用于本授权书）

作者签名：                    导师签名：

                                  年    月    日

> **格式提示：** 声明与授权页的格式在阶段 ⑨ 自动排版。正文使用小四号宋体，"声明"二字使用小二号黑体居中。

---

## 摘  要

遥感图像语义分割是计算机视觉领域的重要研究方向，在土地利用分类、城市规划、环境监测等领域具有广泛的应用前景。近年来，基于深度学习的语义分割方法取得了显著进展，但遥感图像特有的类间尺度差异大、边界模糊、样本标注困难等问题仍然制约着分割精度的进一步提升。

本文针对上述问题，提出了一种面向遥感图像的语义分割方法——多尺度特征融合注意力网络。主要研究工作如下：

（1）针对遥感图像中地物目标尺度差异大的问题，设计了一种多尺度特征提取模块。该模块通过并行不同膨胀率的卷积核捕获多尺度上下文信息，有效提升了不同尺度目标的识别能力。

（2）针对遥感图像边界分割模糊的问题，引入了一种边界感知注意力机制。该机制通过显式建模边界区域的像素级注意力权重，增强了网络对目标边界的感知能力。

（3）针对遥感图像标注样本不足的问题，提出了一种基于对比学习的半监督训练策略。该策略利用大量无标签影像数据，通过对比学习预训练提升模型在有限标注样本下的分割性能。

在ISPRS Vaihingen和Potsdam数据集上的实验结果表明，本文提出的方法在mIoU指标上分别达到了84.6%和86.3%，较基线模型分别提升了5.2和4.8个百分点。消融实验和可视化分析进一步验证了各模块的有效性。

**关键词：** 遥感图像；语义分割；深度学习；注意力机制；多尺度特征融合

> **格式提示：** 四川大学硕士学位论文摘要约1000字，博士学位论文摘要约3000字。摘要中的"关键词"三字使用小四号黑体，关键词内容使用小四号宋体，关键词之间用空格分隔。

---

## ABSTRACT

Semantic segmentation of remote sensing images is a crucial research direction in computer vision, with broad applications in land use classification, urban planning, and environmental monitoring. In recent years, deep learning-based semantic segmentation methods have achieved remarkable progress. However, challenges inherent to remote sensing images—such as large inter-class scale variations, blurred boundaries, and limited annotated samples—continue to constrain further improvements in segmentation accuracy.

To address these challenges, this thesis proposes a multi-scale feature fusion attention network tailored for remote sensing image semantic segmentation. The main contributions are as follows:

(1) To tackle the large scale variations of ground objects in remote sensing images, a multi-scale feature extraction module is designed. This module captures multi-scale contextual information through parallel convolutional kernels with different dilation rates, effectively improving the recognition capability for targets at various scales.

(2) To address the issue of blurred boundary segmentation, a boundary-aware attention mechanism is introduced. By explicitly modeling pixel-level attention weights in boundary regions, this mechanism enhances the network's perception of object boundaries.

(3) To mitigate the problem of insufficient annotated samples, a semi-supervised training strategy based on contrastive learning is proposed. This strategy leverages large amounts of unlabeled image data through contrastive learning pre-training to improve segmentation performance under limited annotation conditions.

Experimental results on the ISPRS Vaihingen and Potsdam datasets demonstrate that the proposed method achieves mIoU scores of 84.6% and 86.3%, representing improvements of 5.2 and 4.8 percentage points over the baseline model, respectively. Ablation studies and visualization analyses further validate the effectiveness of each proposed module.

**Keywords:** Remote sensing image; Semantic segmentation; Deep learning; Attention mechanism; Multi-scale feature fusion

> **格式提示：** 英文摘要应与中文摘要内容对应。全文英文使用 Times New Roman 字体，字号小四（12pt），行距20磅。

---

## 目  录

```
摘要 ................................................................................ I
ABSTRACT ........................................................................... II
目录 ............................................................................... III
第一章 绪论 ......................................................................... 1
  1.1 研究背景与意义 ................................................................. 1
  1.2 国内外研究现状 ................................................................. 4
  1.3 主要研究内容 ................................................................... 9
  1.4 论文组织结构 ................................................................... 11
第二章 相关理论基础 .................................................................. 12
  2.1 卷积神经网络基础 ............................................................... 12
  2.2 语义分割经典网络 ............................................................... 18
  2.3 注意力机制 ..................................................................... 24
  2.4 对比学习 ....................................................................... 28
第三章 多尺度特征融合注意力网络 ...................................................... 31
  3.1 整体网络架构 ................................................................... 31
  3.2 多尺度特征提取模块 ............................................................. 34
  3.3 边界感知注意力模块 ............................................................. 38
  3.4 损失函数设计 ................................................................... 42
第四章 半监督训练策略 ................................................................ 45
  4.1 对比学习预训练 ................................................................. 45
  4.2 数据增强策略 ................................................................... 48
  4.3 微调与推理 ..................................................................... 50
第五章 实验与分析 .................................................................... 52
  5.1 实验设置 ....................................................................... 52
  5.2 数据集与评价指标 ............................................................... 54
  5.3 对比实验 ....................................................................... 57
  5.4 消融实验 ....................................................................... 62
  5.5 可视化分析 ..................................................................... 65
第六章 总结与展望 .................................................................... 68
  6.1 本文总结 ....................................................................... 68
  6.2 主要创新点 ..................................................................... 69
  6.3 未来工作展望 ................................................................... 69
参考文献 ............................................................................. 71
作者在读期间科研成果 ................................................................. 76
致谢 ................................................................................. 77
```

> **格式提示：** 目录在阶段 ⑨ 自动生成。目录中的标题层级通过 markdown 标题层级自动映射，页码自动右对齐。

---

# 第一章 绪论

## 1.1 研究背景与意义

遥感技术作为一种重要的空间信息获取手段，在过去的几十年中取得了长足的发展。高分辨率遥感卫星（如WorldView、GeoEye、高分系列等）和无人机遥感平台的普及，使得获取高空间分辨率遥感影像的成本大幅降低[1]。这些影像数据在城市规划、精准农业、灾害监测、国防安全等领域发挥着越来越重要的作用。

然而，如何从海量的遥感影像中快速、准确地提取出有价值的地物信息，始终是该领域的核心挑战。传统方法依赖于人工设计的特征和分类器，在简单场景下尚能取得较好的效果，但在复杂场景中往往表现出鲁棒性不足、泛化能力差等问题[2]。

近年来，以卷积神经网络为代表的深度学习方法在计算机视觉的各个领域取得了突破性进展[3]。全卷积网络及其变体在语义分割任务上大幅超越了传统方法，使得基于深度学习的遥感图像语义分割成为当前的主流技术路线。

## 1.2 国内外研究现状

### 1.2.1 语义分割方法发展

语义分割的目标是为图像中的每个像素分配一个类别标签。早期的语义分割方法主要基于手工特征和随机森林[4]、支持向量机[5]等传统分类器。Long等[6]提出的全卷积网络（FCN）开创了端到端语义分割的新范式，该网络将全连接层替换为卷积层，实现了任意尺寸图像的像素级分类。

在此基础上，研究者们提出了多种改进方案。Ronneberger等[7]提出的U-Net采用跳跃连接融合浅层和深层特征，在小样本医学图像分割中表现优异。Chen等[8]提出的DeepLab系列引入了空洞卷积和空间金字塔池化模块，有效扩大了感受野并捕获多尺度上下文信息。

### 1.2.2 遥感图像分割面临的挑战

尽管通用语义分割方法取得了显著进展，但遥感图像的特殊性带来了额外的挑战[9]：

（1）**类间尺度差异大**。遥感图像中地物目标的尺度差异极为显著。例如，一辆汽车可能仅占据数十个像素，而一片农田可能覆盖整幅图像。通用分割方法难以同时兼顾大尺度和小尺度目标的准确分割。

（2）**边界模糊**。遥感图像中地物边界常常模糊不清，尤其是植被覆盖区域的过渡带、建筑物阴影区域等，给精确的边界分割带来了困难。

（3）**标注样本不足**。遥感图像的像素级标注需要专业知识，人工标注成本极高。有限标注样本下如何训练高性能分割模型是一个重要的研究课题。

## 1.3 主要研究内容

针对上述挑战，本文从网络结构设计和训练策略优化两个层面展开研究：

（1）设计多尺度特征融合模块，在不解耦特征分辨率的前提下，通过多分支的空洞卷积捕获不同尺度的上下文信息。

（2）引入边界感知注意力机制，在特征空间中显式增强目标边界的表征能力。

（3）提出基于对比学习的半监督训练策略，充分利用无标签数据提升模型性能。

## 1.4 论文组织结构

本文共分为六章，各章内容安排如下：

第一章介绍研究背景与意义，综述国内外研究现状，明确研究内容和论文结构。

第二章介绍相关理论基础，包括卷积神经网络基础、经典语义分割模型、注意力机制和对比学习等。

第三章提出多尺度特征融合注意力网络，详细阐述各模块的设计思路和实现细节。

第四章介绍基于对比学习的半监督训练策略。

第五章在公开数据集上进行实验验证，通过对比实验、消融实验和可视化分析评估方法的有效性。

第六章总结本文工作，分析不足并展望未来研究方向。

---

# 第二章 相关理论基础

## 2.1 卷积神经网络基础

### 2.1.1 卷积层

卷积层是卷积神经网络的核心组成部分。对于输入特征图 $\mathbf{X} \in \mathbb{R}^{H \times W \times C_{in}}$ 和卷积核 $\mathbf{W} \in \mathbb{R}^{k \times k \times C_{in} \times C_{out}}$，卷积操作可表示为：

$$
\mathbf{Y}(i,j,c) = \sum_{u=1}^{k} \sum_{v=1}^{k} \sum_{c'=1}^{C_{in}} \mathbf{W}(u,v,c',c) \cdot \mathbf{X}(i+u-1, j+v-1, c') + \mathbf{b}(c) \tag{2-1}
$$

其中，$\mathbf{b} \in \mathbb{R}^{C_{out}}$ 为偏置项。

### 2.1.2 空洞卷积

空洞卷积通过在标准卷积核的元素之间插入空洞来扩大感受野[8]，而不增加参数量。对于膨胀率 $r$ 的空洞卷积，其等效感受野大小为：

$$
K_{eff} = k + (k-1) \times (r-1) \tag{2-2}
$$

### 2.1.3 残差连接

He等[10]提出的残差连接有效解决了深层网络中的梯度消失问题。残差块可表示为：

$$
\mathbf{x}_{l+1} = \mathbf{x}_l + F(\mathbf{x}_l, \mathcal{W}_l) \tag{2-3}
$$

其中 $F(\cdot)$ 为残差函数，通常包含两个或多个卷积层。

> **格式提示：** 公式（2-1）至（2-3）的编号在阶段 ⑨ 自动添加，并右对齐。公式内字母使用 Times New Roman，五号（10.5pt）。行距固定20磅。公式下方的参数说明保持左对齐。

---

# 第三章 多尺度特征融合注意力网络

## 3.1 整体网络架构

本文提出的多尺度特征融合注意力网络以ResNet-101[10]为骨干网络，在编码器-解码器架构的基础上，引入多尺度特征提取模块和边界感知注意力模块。整体网络架构如图3-1所示。

![网络整体架构](figures/network_architecture.png)

**图3-1 多尺度特征融合注意力网络整体架构**

**Fig.3-1 Overall Architecture of Multi-Scale Feature Fusion Attention Network**

## 3.2 多尺度特征提取模块

多尺度特征提取模块的设计灵感来源于空洞空间金字塔池化[8]和特征金字塔网络[11]。给定输入特征图 $\mathbf{X} \in \mathbb{R}^{H \times W \times C}$，该模块通过4个并行的空洞卷积分支提取多尺度特征：

$$
\mathbf{F}_r = \text{Conv}_{3\times3}(\mathbf{X}, r) \quad r \in \{1, 3, 6, 12\} \tag{3-1}
$$

其中 $\text{Conv}_{3\times3}(\cdot, r)$ 表示膨胀率为 $r$ 的 $3 \times 3$ 空洞卷积。各分支输出经拼接和 $1 \times 1$ 卷积降维后，得到多尺度融合特征：

$$
\mathbf{F}_{ms} = \text{Conv}_{1\times1}\left( \big[\mathbf{F}_1; \mathbf{F}_3; \mathbf{F}_6; \mathbf{F}_{12}\big] \right) \tag{3-2}
$$

## 3.3 边界感知注意力模块

为增强模型对遥感图像中目标边界的感知能力，本模块显式地构建了边界注意力图。对于特征 $\mathbf{F} \in \mathbb{R}^{H \times W \times C}$，首先通过 Sobel 算子计算梯度幅值，得到边界响应图 $\mathbf{G} \in \mathbb{R}^{H \times W \times 1}$，然后使用 sigmoid 函数生成注意力权重：

$$
\mathbf{A}_{bd} = \sigma\left( \text{Conv}_{3\times3}(\mathbf{G}) \right) \tag{3-3}
$$

最终的输出特征为：

$$
\mathbf{F}_{out} = \mathbf{F} \odot \mathbf{A}_{bd} + \mathbf{F} \tag{3-4}
$$

---

# 第四章 半监督训练策略

## 4.1 对比学习预训练

受SimCLR[12]和MoCo[13]等对比学习方法的启发，本文设计了一种适用于遥感图像的对比学习预训练策略。给定一批训练图像，对每张图像进行两种随机数据增强得到两个视图 $x_i$ 和 $x_j$，对比学习损失函数定义为：

$$
\mathcal{L}_{cl} = -\log \frac{\exp(\text{sim}(\mathbf{z}_i, \mathbf{z}_j) / \tau)}{\sum_{k=1}^{2N} \mathbb{1}_{[k \neq i]} \exp(\text{sim}(\mathbf{z}_i, \mathbf{z}_k) / \tau)} \tag{4-1}
$$

其中 $\mathbf{z}_i = \text{Proj}(\text{Enc}(x_i))$ 为投影头输出的特征向量，$\tau$ 为温度系数，$N$ 为batch大小。

---

# 第五章 实验与分析

## 5.1 实验设置

### 5.1.1 硬件环境

实验在以下硬件环境中进行：Intel Xeon Gold 6248R CPU @ 3.00GHz × 2，NVIDIA Tesla V100 GPU（32GB显存），256GB RAM。

### 5.1.2 训练参数

优化器采用AdamW，初始学习率为0.0001，采用余弦退火学习率调度策略。模型训练共进行200个epoch，batch size设为8。

## 5.2 数据集与评价指标

### 5.2.1 ISPRS Vaihingen数据集

Vaihingen数据集包含33张真彩色正射影像图，空间分辨率为9cm，图像尺寸约为2000×2000像素。标注类别包括：不透水面、建筑物、低矮植被、树木、汽车和背景等6类。

### 5.2.2 评价指标

本文使用以下指标评价分割性能：

- 平均交并比（mIoU）
- 类别像素准确率（mAcc）
- 总体像素准确率（OA）

## 5.3 对比实验

本文与多种主流语义分割方法进行了对比，实验结果如表5-1所示。

**表5-1 不同方法在ISPRS Vaihingen数据集上的对比结果**

**Tab.5-1 Comparison Results of Different Methods on the ISPRS Vaihingen Dataset**

| 方法 | 不透水面 | 建筑物 | 低矮植被 | 树木 | 汽车 | 背景 | mIoU(%) | OA(%) |
|------|---------|--------|----------|------|------|------|---------|-------|
| FCN-8s[6] | 87.2 | 88.5 | 75.1 | 82.4 | 66.3 | 70.5 | 78.3 | 85.1 |
| U-Net[7] | 88.1 | 89.3 | 76.8 | 83.9 | 68.7 | 72.1 | 79.8 | 86.2 |
| DeepLabV3+[8] | 89.5 | 91.2 | 78.6 | 85.1 | 72.4 | 74.3 | 81.8 | 88.0 |
| **本文方法** | **91.3** | **93.1** | **81.7** | **87.5** | **77.2** | **76.8** | **84.6** | **90.2** |

> **格式提示：** 三线表格式在阶段 ⑨ 自动应用。表标题在上方居中、五号（10.5pt）加粗，表内容五号宋体，表前和表后各空一行。

## 5.4 消融实验

为验证各模块的有效性，本文进行了消融实验，结果如表5-2所示。

**表5-2 Vaihingen数据集上的消融实验结果**

**Tab.5-2 Ablation Study Results on the Vaihingen Dataset**

| 模型配置 | 多尺度模块 | 边界注意力 | 半监督 | mIoU(%) |
|---------|-----------|-----------|--------|---------|
| 基线 | - | - | - | 79.4 |
| +多尺度 | ✓ | - | - | 82.1 |
| +边界注意力 | ✓ | ✓ | - | 83.5 |
| 完整模型 | ✓ | ✓ | ✓ | 84.6 |

以下图片展示了不同模型在测试图像上的分割结果对比。

![Vaihingen分割结果对比](figures/vaihingen_comparison.png)

**图5-1 不同方法在Vaihingen数据集上的分割结果对比**

**Fig.5-1 Segmentation Result Comparison on the Vaihingen Dataset**

## 5.5 可视化分析

为进一步理解本文提出方法的行为，我们对中间层特征图进行了可视化分析，如图5-2所示。

![特征图可视化](figures/feature_visualization.png)

**图5-2 多尺度特征图可视化**

**Fig.5-2 Multi-Scale Feature Map Visualization**

---

# 第六章 总结与展望

## 6.1 本文总结

本文针对遥感图像语义分割中类间尺度差异大、边界模糊、样本标注不足三个核心问题，提出了多尺度特征融合注意力网络和基于对比学习的半监督训练策略。实验结果表明，本文方法在两个公开数据集上均取得了具有竞争力的性能。

## 6.2 主要创新点

（1）设计了多尺度特征提取模块，通过并行多分支空洞卷积和自适应融合策略，有效提升了模型对不同尺度目标的识别能力。

（2）引入了边界感知注意力机制，通过显式建模边界注意力权重，显著改善了遥感图像中目标边界的分割精度。

（3）提出了基于对比学习的半监督训练策略，在标注样本有限的条件下有效提升了模型性能。

## 6.3 未来工作展望

未来的研究方向包括：（1）探索轻量化网络结构，满足实时处理需求；（2）融合多模态数据（如LiDAR点云）提升分割精度；（3）研究域适应方法，提升模型在不同遥感数据集间的泛化能力。

---

# 参考文献

[1] 张兵. 遥感大数据时代的高光谱遥感[J]. 遥感学报, 2022, 26(6): 1023-1037.

[2] Zhu X X, Tuia D, Mou L, et al. Deep learning in remote sensing: A comprehensive review and list of resources[J]. IEEE Geoscience and Remote Sensing Magazine, 2017, 5(4): 8-36.

[3] LeCun Y, Bengio Y, Hinton G. Deep learning[J]. Nature, 2015, 521(7553): 436-444.

[4] Breiman L. Random forests[J]. Machine Learning, 2001, 45(1): 5-32.

[5] 丁世飞, 齐丙娟, 谭红艳. 支持向量机理论与算法研究综述[J]. 电子科技大学学报, 2011, 40(1): 2-10.

[6] Long J, Shelhamer E, Darrell T. Fully convolutional networks for semantic segmentation[C]. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, 2015: 3431-3440.

[7] Ronneberger O, Fischer P, Brox T. U-Net: Convolutional networks for biomedical image segmentation[C]. International Conference on Medical Image Computing and Computer-Assisted Intervention, 2015: 234-241.

[8] Chen L C, Papandreou G, Kokkinos I, et al. DeepLab: Semantic image segmentation with deep convolutional nets, atrous convolution, and fully connected CRFs[J]. IEEE Transactions on Pattern Analysis and Machine Intelligence, 2018, 40(4): 834-848.

[9] 李德仁, 王树良, 李德毅. 空间数据挖掘理论与应用（第二版）[M]. 北京: 科学出版社, 2019.

[10] He K, Zhang X, Ren S, et al. Deep residual learning for image recognition[C]. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, 2016: 770-778.

[11] Lin T Y, Dollár P, Girshick R, et al. Feature pyramid networks for object detection[C]. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, 2017: 2117-2125.

[12] Chen T, Kornblith S, Norouzi M, et al. A simple framework for contrastive learning of visual representations[C]. International Conference on Machine Learning, 2020: 1597-1607.

[13] He K, Fan H, Wu Y, et al. Momentum contrast for unsupervised visual representation learning[C]. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2020: 9729-9738.

[14] Wang Y, Wang L, Hu H, et al. SSA: Semantic structure-aware semi-supervised semantic segmentation[J]. IEEE Transactions on Image Processing, 2023, 32: 5412-5425.

---

# 作者在读期间科研成果

## 学术论文

1. **王强**, 陈明, 赵峰. 多尺度特征融合的遥感图像语义分割方法[J]. 电子与信息学报, 2025, 47(8): 1-9.（EI核心）
2. **Wang Q**, Chen M, Zhao F. Boundary-aware attention network for remote sensing image segmentation[J]. IEEE Geoscience and Remote Sensing Letters, 2025, 22: 6006505.（SCI, JCR Q2）

## 参与科研项目

1. 国家自然科学基金面上项目（编号：62471234）：基于深度学习的遥感图像智能解译方法研究，2023-2026.
2. 四川省重点研发计划（编号：2024YFG0012）：遥感大数据智能分析平台关键技术研究，2024-2025.

> **格式提示：** 在读期间科研成果为四川大学学位论文特有章节。"作者在读期间科研成果"作为一级标题，格式与一级标题一致。此部分在阶段 ⑨ 会按照正文样式统一排版。

---

# 致  谢

三年硕士研究生的学习生活即将画上句号。回首这段时光，我深感成长与收获。

首先，衷心感谢我的导师陈明教授。从入学之初的学业规划，到研究方向的确定，再到论文的选题、实验和撰写，陈老师都给予了悉心的指导和热情的帮助。陈老师严谨的治学态度、敏锐的学术洞察和包容的教学风格，让我在研究工作中不断探索和进步。在论文完成之际，谨向陈老师致以最诚挚的谢意。

感谢电子信息学院各位授课老师的教导，为我的研究工作打下了坚实的基础。感谢课题组赵峰师兄、李明师弟在实验和论文修改中的帮助。

感谢我的家人，你们的理解和支持是我坚持完成学业的动力。

最后，感谢四川大学为研究生提供的优质学术平台和科研环境。

> **格式提示：** 致谢格式（字体、字号、行距）在阶段 ⑨ 自动应用正文样式：宋体小四号（12pt），固定20磅行距，首行缩进2字符。

---

> **关于本示例：**
>
> 本文件展示了一份 markdown 格式的四川大学硕士学位论文完整输入结构。
> 在阶段 ⑨（FINALIZE）中，选择 `sichuan-grad` profile 后，AR 管道会自动：
> 1. 通过 Pandoc 将 markdown 转换为 DOCX
> 2. 应用四川大学学位论文页面设置（16开、页边距等）
> 3. 格式化中英文摘要
> 4. 生成目录
> 5. 设置页眉（四川大学硕士学位论文）和页脚（居中页码）
> 6. 应用三线表格式
> 7. 格式化图题和公式编号
>
> 要使用此示例，将本文件放入您的 ARS 项目中，然后运行 `/ars-format-convert` 并选择 `sichuan-grad` profile。
