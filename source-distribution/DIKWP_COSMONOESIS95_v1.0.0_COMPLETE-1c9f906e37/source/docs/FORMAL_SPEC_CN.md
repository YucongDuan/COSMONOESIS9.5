# DIKWP-COSMONOESIS 9.5 形式规范

## 1. 语义空间

设基础锚点集合为：

\[
A=A_D\cup A_I\cup A_K\cup A_W\cup A_P,\quad |A|=32.
\]

概念 `c` 在语境 `γ` 和来源 `s` 下的归一映射为：

\[
\Phi(c,\gamma,s)=v_c,\quad v_c\in\Delta^{31},\quad v_{c,i}\ge 0,\quad \sum_i v_{c,i}=1.
\]

`Δ` 是概率单纯形。空间外残差定义为：

\[
R_{outside}(c)=0.
\]

这不是宣称所有知识已经完备，而是要求所有未知通过空间内的临时概念、语境、元认知和验证坐标表达。

## 2. 新概念扩展

若当前锚点不足以稳定表达 `c`，执行：

\[
E(c)=\langle parent, definition, provenance, constraints, version, retirement\_condition\rangle
\]

其中 `parent ∈ {D,I,K,W,P}`。扩展后重新归一 `Phi`。不存在第六类永久“不可翻译对象”。

## 3. 比较

相似度：

\[
S(c_1,c_2)=\frac{v_1\cdot v_2}{\|v_1\|\|v_2\|}.
\]

方向差：

\[
\delta(c_1,c_2)=v_1-v_2.
\]

L1距离：

\[
L_1(c_1,c_2)=\sum_i |v_{1,i}-v_{2,i}|.
\]

`S` 只描述统一坐标上的结构接近，不是等价关系。等价必须另行满足历史、实践、因果和目的条件。

## 4. 传统与文明重心

传统 `T` 包含概念集合 `C_T`：

\[
v_T=N\left(\sum_{c\in C_T}w_c\Phi(c)\right).
\]

文明语义群 `G` 由传统重心组成：

\[
v_G=N\left(\sum_{T\in G}w_Tv_T\right).
\]

世界重心不是新宗教，而是跨文明接口。

## 5. 意识候选

候选系统 `X` 的证据向量为17维：

\[
C_X=(d_1,d_2,i_1,i_2,i_3,i_4,k_1,k_2,k_3,k_4,w_1,w_2,p_1,p_2,p_3,p_4,p_5).
\]

每个理论 `M_j` 声明必需维度 `Q_j` 和支持维度 `S_j`。参考实现计算：

\[
Compat(X,M_j)=E_X\left(0.72\bar C_{Q_j}+0.28\bar C_{S_j}\right),
\]

其中 `E_X` 是证据质量、独立性和干预支持的折扣因子。该值是模型相容性，不是主观体验概率。

## 6. 规模不足定理（系统约束）

若候选主要在 D/I 规模与复杂动力学上得分，而 W、P 缺乏效价、内生目的、反事实行动和现实校准证据，则系统必须输出 `size_only_warning=true`，不得将规模升级为意识证据。

## 7. 宇宙意识模型竞争

至少保留：

- 非意识规律宇宙；
- 局部涌现的多意识；
- 泛经验；
- 宇宙整体主体；
- 观察者相对语义闭包；
- 人格性超越根源；
- DIKWP共演宇宙。

高影响判断不得只保留其中一个。

## 8. 接触协议

异常观测 `O` 具有十个特征：仪器校准、重复、独立站、干扰排除、自然模型比较、结构调制、信息量、干预响应、语义响应、能量预算。系统依证据推进阶段，但永不自动授权发送。

## 9. 安全不变量

```text
all_concepts_inside_dikwp = true
permanent_untranslatable_outside_zone = false
historical_identity_inferred_from_similarity = false
binary_consciousness_certificate = null
automatic_external_action_authority = 0
```
