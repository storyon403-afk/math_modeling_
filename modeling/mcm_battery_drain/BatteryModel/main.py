import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(
    os.path.join(current_dir, "..", "..", "..")
)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from modeling.mcm_battery_drain.BatteryModel.simulation.simulator import simulate
from modeling.mcm_battery_drain.BatteryModel.models.state import BatteryState
from modeling.mcm_battery_drain.BatteryModel.models.behavior import UserBehavior
from modeling.mcm_battery_drain.BatteryModel.plots import plot_0
from modeling.mcm_battery_drain.BatteryModel.params.load_params import LoadPowerParams
from modeling.mcm_battery_drain.BatteryModel.params.electrical_params import ElectricalParams
from modeling.mcm_battery_drain.BatteryModel.params.thermal_params import ThermalParams
from modeling.mcm_battery_drain.BatteryModel.params.soc_params import SocParams
from modeling.mcm_battery_drain.BatteryModel.params.aging_params import AgingParams
from modeling.mcm_battery_drain.BatteryModel.params.resistance_params import ResistanceParams
from modeling.mcm_battery_drain.BatteryModel.analysis.scenario_analysis import SCENARIOS
from modeling.mcm_battery_drain.BatteryModel.analysis.sensitivity import run_sensitivity , plot_sensitivity

def main():

    print("=" * 60)
    print("手机电池数字孪生仿真")
    print("=" * 60)

    # 预留CSV路径（目前不参与计算）

    data_dir = os.path.join(project_root, "data")

    power_profile_path = os.path.join(
        data_dir,
        "1.xlsx - 04_手机功耗参数.csv"
    )

    scenario_path = os.path.join(
        data_dir,
        "1.xlsx - 05_场景输入与功耗.csv"
    )

    print("\n数据文件检查:")

    if os.path.exists(power_profile_path):
        print("✓ 功耗参数CSV已找到")
    else:
        print("✗ 功耗参数CSV不存在")

    if os.path.exists(scenario_path):
        print("✓ 场景数据CSV已找到")
    else:
        print("✗ 场景数据CSV不存在")

    print("\n当前模式：")
    print("使用代码默认参数")
    print("尚未启用CSV驱动")

    # 初始状态

    state = BatteryState()

    load_params = LoadPowerParams()

    electrical_params = ElectricalParams()

    thermal_params = ThermalParams()

    soc_params = SocParams()

    aging_params = AgingParams()

    resistance_params = ResistanceParams()
    
    ip = int(input("选择分析：1（场景分析），2（敏感性分析）"))

    if ip == 1:

        choice = int(
            input(
                "选择场景(1办公 2视频 3导航): "
            )
        )

        cfg = SCENARIOS[choice]

        user = UserBehavior(
        brightness=cfg["brightness"],
        cpu=cfg["cpu"],
        gpu=cfg["gpu"],
        network_traffic=cfg["network_traffic"],
        signal_quality=cfg["signal_quality"],
        gps=cfg["gps"],
        background=cfg["background"]
)

        

        print("\n开始仿真...")

        # 仿真

        history = simulate(
            state,
            user,

            load_params,
            electrical_params,
            thermal_params,

            soc_params,
            aging_params,
            resistance_params,

            q_nom=3.45,
            dt=1.0,
            total_time=3600
        )

        print(f"仿真完成，共生成 {len(history)} 条记录")

        if len(history) > 0:

            print("\n最终状态:")

            last = history[-1]

            print(f"Time    : {last['time']:.2f}")

            if "soc" in last:
                print(f"SOC     : {last['soc']:.2f}%")

            if "soh" in last:
                print(f"SOH     : {last['soh']:.4f}%")

            if "temp" in last:
                print(f"Temp    : {last['temp']:.2f} °C")

            if "voltage" in last:
                print(f"Voltage : {last['voltage']:.3f} V")

            if "tte" in last:
                print(
                    f"TTE     : {last['tte']/3600:.2f} h"
                )

        print("\n开始绘图...")

        # 绘图

        plot_0.soc_plot(history)
        plot_0.soh_plot(history)
        plot_0.temp_plot(history)
        plot_0.behavior_plot(history)
        plot_0.ecm_plot(history)
        plot_0.soc_temp_plot(history)
        plot_0.soc_voltage_plot(history)
        plot_0.soc_temp_voltage_plot(history)
        plot_0.heat_map_plot(history)
        plot_0.tte_plot(history)
        plot_0.soc_tte_plot(history)
        plot_0.power_tte_plot(history)
        plot_0.tte_heatmap(history)
        

        print("\n所有图表生成完成！")

    elif ip == 2:

        print("""
            1 brightness
            2 cpu
            3 network
            4 signal
            """)

        choice = int(input("选择敏感性参数: "))

        if choice == 1:

            param_name = "brightness"

            values = [
                0.2,
                0.4,
                0.6,
                0.8,
                1.0
            ]

        elif choice == 2:

            param_name = "cpu"

            values = [
                0.1,
                0.3,
                0.5,
                0.7,
                0.9
            ]

        elif choice == 3:

            param_name = "network_traffic"

            values = [
                1,
                5,
                10,
                15,
                20
            ]

        elif choice == 4:

            param_name = "signal_quality"

            values = [
                1,
                2,
                3,
                4,
                5
            ]

        results = run_sensitivity(
            param_name=param_name,
            values=values,

            load_params=load_params,
            electrical_params=electrical_params,
            thermal_params=thermal_params,
            soc_params=soc_params,
            aging_params=aging_params,
            resistance_params=resistance_params
        )

        plot_sensitivity(
            results,
            param_name
        )

    else:
        raise ValueError("只能输入整数1，2进行选择")


##if __name__ == "__main__":
##    main()