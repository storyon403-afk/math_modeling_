# 手机电池数字孪生建模与仿真系统

## 项目简介

本项目构建了一个面向智能手机锂离子电池的数字孪生（Digital Twin）模型，通过融合用户行为模型、电池等效电路模型（ECM）、热模型、SOC估计模型、SOH老化模型以及TTE续航预测模型，实现对手机电池运行状态的动态仿真与可视化分析。

项目支持：

* 电池放电过程仿真
* SOC（State of Charge）估计
* SOH（State of Health）估计
* 电池热行为分析
* TTE（Time To Empty）剩余续航预测
* 多场景用户行为分析
* 参数敏感性分析
* 数字孪生可视化展示

---

## 模型架构

用户行为模型

↓

负载功耗模型

↓

电池等效电路模型（ECM）

↓

SOC估计

↓

热模型

↓

SOH老化模型

↓

TTE预测

↓

可视化分析

---

## 项目目录结构

BatteryModel/

├── main.py

│

├── models/

│   ├── state.py

│   └── behavior.py

│

├── params/

│   ├── load_params.py

│   ├── electrical_params.py

│   ├── thermal_params.py

│   ├── soc_params.py

│   ├── aging_params.py

│   └── resistance_params.py

│

├── physics/

│   ├── load.py

│   ├── electrical.py

│   ├── thermal.py

│   ├── soc.py

│   ├── soh.py

│   ├── resistance.py

│   └── tte.py

│

├── simulation/

│   └── simulator.py

│

├── analysis/

│   ├── scenario_analysis.py

│   └── sensitivity.py

│

├── plots/

│   └── plot_0.py

│

└── data/

---

## 核心模型

### 1. 用户行为模型

输入用户行为参数：

* 屏幕亮度（Brightness）
* CPU负载率（CPU Load）
* GPU负载率（GPU Load）
* 网络流量（Network Traffic）
* 信号质量（Signal Quality）
* GPS状态（GPS On/Off）
* 后台应用功耗（Background Load）

输出总负载功率：

P_load

---

### 2. 电池等效电路模型

采用二阶RC模型：

OCV

↓

R0

↓

R1-C1

↓

R2-C2

↓

Terminal Voltage

用于模拟：

* 极化效应
* 动态电压响应
* 内阻变化

---

### 3. SOC模型

采用库仑积分法：

dSOC/dt = -I / Q_eff

考虑：

* 电流影响
* 温度影响
* 有效容量变化

---

### 4. SOH模型

采用Arrhenius老化模型：

dSOH/dt = f(T, C-rate, SOC)

考虑：

* 温度应力
* 充放电倍率
* SOC工作区间

---

### 5. 热模型

基于集中参数热模型：

C_th · dT/dt = Q_gen - Q_loss

用于描述：

* 焦耳热产生
* 环境散热
* 温度动态变化

---

### 6. TTE预测模型

根据当前：

* SOC
* SOH
* 电流
* 功率

实时估计：

Remaining Runtime

即：

Time To Empty (TTE)

---

## 场景分析

系统内置典型用户场景：

### 办公场景

* 低亮度
* 低CPU负载
* GPS关闭

### 视频场景

* 高亮度
* 中CPU负载
* 网络持续传输

### 导航场景

* 高亮度
* GPS开启
* 弱信号环境

分析指标：

* SOC
* SOH
* Temperature
* Voltage
* TTE

---

## 敏感性分析

支持以下参数自动扫描：

* Brightness
* CPU Load
* Network Traffic
* Signal Quality
* GPS

输出：

* 参数-TTE曲线
* 参数-温度曲线
* 参数-SOC曲线
* 参数-SOH曲线

---

## 输出图表

系统可自动生成：

1. SOC-Time
2. SOH-Time
3. Temperature-Time
4. Voltage-Time
5. SOC-Voltage
6. SOC-Temperature
7. SOC-Temperature-Voltage
8. Heat Map
9. TTE-Time
10. SOC-TTE
11. Power-TTE
12. TTE Heatmap

---

## 运行方式

运行主程序：

python main.py

选择：

1 -> 场景分析

2 -> 敏感性分析

根据提示输入对应编号即可完成仿真。

---

## 参数说明

项目当前采用：

* 机理模型
* 工程经验参数

参数来源包括：

* Android Power Profile
* Pixel XL公开功耗数据
* 锂离子电池模型文献
* 工程经验标定

由于缺乏真实长期实验数据，部分经验参数通过续航结果校准至合理区间。

---

## 应用价值

本项目可用于：

* 手机电池寿命预测
* 电池数字孪生研究
* 数学建模竞赛
* 电池管理系统（BMS）教学
* 电池状态估计研究
* 能耗优化分析

