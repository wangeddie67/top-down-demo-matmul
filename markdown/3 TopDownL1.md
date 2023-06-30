
# Intel Top-down详解 之 TopDownL1

不论哪一个版本，Top-down的第一层都是分为4个分类，Frontend_Bound，Bad_Speculation，Retiring和Backend_Bound。

Top-down的第一层的观察点位于issue点，如下图所示。在这个位置是处理器流水线上最后一个保证指令顺序的点。在这个位置之后，指令进入乱序调度器。乱序调度器将依赖关系就绪的uop发射给对应的执行单元；完成的uop按照程序顺序进行退休。处理器流水线从这个点分为前端和后端两个部分（frontend和backend）。

Top-down第一层的度量单位是流水线slot，表示1个uop。每个周期，issue point能够发射的slot数量与issue width相同。在性能评估期间，能够发射的uop总量是仿真时间和issue width的乘积。理想情况下，所有的流水线slot都应该能够issue uop，不应该有空闲的slot。而且issue的uop不是投机的，能够退休。

## Top-down第一层和第二层分类

Top-down第一层的度量如下：

### Frontend_Bound

表示由于前端无法给后端提供足够负载而浪费的slot。

例如：

- 指令缓存缺失引起的前端stall。
- uop译码器和uop序列译码器切换引起的前端stall。

### Bad_Speculation

这个分类表示由于错误投机浪费的slot比例。包括了不能退休的uop占用的slot，以及为了从错误投机中恢复归来而阻塞发射流水线的slot。

例如：
- 由于分支预测错误而浪费的uop。
- 在Memory Ordering Nukes之后的错误数据投机。

### Retiring

这个分类表示被有效uop使用的slot的比例。理想情况下，所有的流水线slot都应该属于这个分类。Retiring达到100%表示达到了流水线的最大吞吐率。最大化吞吐率一般都会提高IPC。

需要注意的是，Retiring数值高不表示没有性能优化的空间：

- 微码assist被归类到Retiring，微码assist破坏性能，并且通常可以避免。
- 如果没有向量化的指令表现为retiring数值高，那么程序员可以考虑向量化代码。这样做可以在不增加指令数的情况下提高计算量，因此需要提升性能。

### Backend_Bound

这个分类表示由于后端无法接收uop而浪费的slot，通常是因为uop所需的资源无法得到满足。

例如：

- 数据缓存缺失引起的stall
- 由于除法单元过载引起的stall

## Top-down第一层计算公式

### V1.0版本

Silvermont和Knights Landing提供了

```python
Frontend_Bound = NO_ALLOC_CYCLES.NOT_DELIVERED / CPU_CLK_UNHALTED.CORE
Bad_Speculation = NO_ALLOC_CYCLES.MISPREDICTS / CPU_CLK_UNHALTED.CORE
Retiring = UOPS_RETIRED.ALL / 2 * CPU_CLK_UNHALTED.CORE
Backend_Bound = 1 - (retiring + bad_speculation + frontend)
```

- NO_ALLOC_CYCLES.NOT_DELIVERED用于度量front-end bound的时钟周期，表示前端无法给后端提供uop而且后端没有stall。
- NO_ALLOC_CYCLES.MISPREDICTS统计没有分配uop而且等待错误预测跳转而stall流水线。

由于乱序单元存在大量的stall相互重叠的情况，通过PMC直接统计或者PMC公式计算会引入误差。同时，为了保证第1级的四个分类之和为1，Backend_Bound是通过排除法得到的。

### V2.0版本的计算公式

计算公式为：

```python
SLOTS = Pipeline_Width * CPU_CLK_UNHALTED.CORE

Frontend_Bound = TOPDOWN_FE_BOUND.ALL / SLOTS
Bad_Speculation = TOPDOWN_BAD_SPECULATION.ALL / SLOTS
Retiring = TOPDOWN_RETIRING.ALL / SLOTS
Backend_Bound = TOPDOWN_BE_BOUND.ALL / SLOTS
```

Pipeline_width表示流水线宽度，Alderlake取值4，Elkhart取值5。

Alderlake和Elkhart直接提供了4个PMC，分别对应于四个度量：

- TOPDOWN_FE_BOUND.ALL Counts the total number of issue slots every cycle that were not consumed by the backend due to frontend stalls. 
- TOPDOWN_BAD_SPECULATION.ALL Counts the total number of issue slots that were not consumed by the backend because allocation is stalled due to a mispredicted jump or a machine clear. 
  - Only issue slots wasted due to fast nukes such as memory ordering nukes are counted. Other nukes are not accounted for. 
  - Counts all issue slots blocked during this recovery window including relevant microcode flows and while uops are not yet available in the instruction queue (IQ) even if an FE_bound event occurs during this period. 
  - Also includes the issue slots that were consumed by the backend but were thrown away because they were younger than the mispredict or machine clear. CORE: ECore
- TOPDOWN_RETIRING.ALL counts the total number of consumed retirement slots. CORE: ECore
- TOPDOWN_BE_BOUND.ALL counts the total number of issue slots every cycle that were not consumed by the backend due to backend stalls.

### V4.5版本计算公式

V4.5版本计算公式与不同微架构的PMC实现有关。

#### SandyBridge, IvyBridge, Haswell, Broadwell, Skylake, Cascade

计算公式为：

```python
SLOTS = Pipeline_Width * CORE_CLKS

Frontend_Bound = IDQ_UOPS_NOT_DELIVERED.CORE / SLOTS
Bad_Speculation = (UOPS_ISSUED.ANY - UOPS_RETIRED.RETIRE_SLOTS + Pipeline_Width * Recovery_Cycles) / SLOTS
Retiring = UOPS_RETIRED.RETIRE_SLOTS / SLOTS
Backend_Bound = 1 - (Frontend_Bound + Bad_Speculation + Retiring)
// After simplify
Backend_Bound = 1 - Frontend_Bound - (UOPS_ISSUED.ANY + Pipeline_Width * Recovery_Cycles) / SLOTS
```

- IDQ_UOPS_NOT_DELIVERED.CORE This event counts the number of uops not delivered to the back-end per cycle, per thread, when the back-end was not stalled. In the ideal case 4 uops can be delivered each cycle. The event counts the undelivered uops - so if 3 were delivered in one cycle, the counter would be incremented by 1 for that cycle (4 - 3). If the back-end is stalled, the count for this event is not incremented even when uops were not delivered, because the back-end would not have been able to accept them. This event is used in determining the front-end bound category of the top-down pipeline slots characterization.
- UOPS_ISSUED.ANY counts the number of Uops issued by the front-end of the pipeilne to the back-end.
UOPS_RETIRED.RETIRE_SLOTS counts the number of retirement slots used each cycle. There are potentially 4 slots that can be used each cycle - meaning, 4 micro-ops or 4 instructions could retire each cycle. This event is used in determining the 'Retiring' category of the Top-Down pipeline slots characterization.

在slot的计算中，考虑到了smt的情况。如果使能了smt，需要将PMC统计的clock均分。

```python
CORE_CLKS = CPU_CLK_UNHALTED.THREAD_ANY / 2
Recovery_Cycles = INT_MISC.RECOVERY_CYCLES_ANY / 2
```

如果关闭SMT。

```python
CORE_CLKS = CPU_CLK_UNHALTED.THREAD
Recovery_Cycles = INT_MISC.RECOVERY_CYCLES
```

- INT_MISC.RECOVERY_CYCLES_ANY Core cycles the allocator was stalled due to recovery from earlier clear event for any thread running on the physical core (e.g. misprediction or memory nuke).
- INT_MISC.RECOVERY_CYCLES Number of cycles waiting for the checkpoints in Resource Allocation Table (RAT) to be recovered after Nuke due to all other cases except JEClear (e.g. whenever a ucode assist is needed like SSE exception, memory disambiguation, etc...).

#### Icelake, Alderlake, Sapphire Rapids

提供了一种topdown_use_fixed模式。如果使能topdown_use_fixed

```python
PERF_METRICS_SUM = PERF_METRICS.FRONTEND_BOUND / TOPDOWN.SLOTS + PERF_METRICS.BAD_SPECULATION / TOPDOWN.SLOTS + PERF_METRICS.RETIRING / TOPDOWN.SLOTS + PERF_METRICS.BACKEND_BOUND / TOPDOWN.SLOTS
SLOTS = TOPDOWN.SLOTS
Frontend_Bound = PERF_METRICS.FRONTEND_BOUND / TOPDOWN.SLOTS / PERF_METRICS_SUM - INT_MISC.UOP_DROPPING / SLOTS
Bad_Speculation = max(1 - (Frontend_Bound + Backend_Bound + Retiring), 0)
Retiring = PERF_METRICS.RETIRING / TOPDOWN.SLOTS / PERF_METRICS_SUM
Backend_Bound = PERF_METRICS.BACKEND_BOUND / TOPDOWN.SLOTS / PERF_METRICS_SUM + Pipeline_Width * INT_MISC.RECOVERY_CYCLES:c1:e1 / SLOTS
```

如果关闭topdown_use_fixed：

```python
SLOTS = TOPDOWN.SLOTS
Frontend_Bound = (IDQ_UOPS_NOT_DELIVERED.CORE - INT_MISC.UOP_DROPPING) / SLOTS
Bad_Speculation = max(1 - (Frontend_Bound + Backend_Bound + Retiring), 0)
Retiring = UOPS_RETIRED.SLOTS / SLOTS
Backend_Bound = (TOPDOWN.BACKEND_BOUND_SLOTS + Pipeline_Width * INT_MISC.RECOVERY_CYCLES:c1:e1) / SLOTS
```

##### Alderlake, Sapphire Rapids的Backend_Bound

如果使能topdown_use_fixed

```python
Backend_Bound = PERF_METRICS.BACKEND_BOUND / TOPDOWN.SLOTS / PERF_METRICS_SUM
```

如果关闭topdown_use_fixed：

```python
Backend_Bound = TOPDOWN.BACKEND_BOUND_SLOTS / SLOTS
```
