from modeling.mcm_battery_drain.BatteryModel.simulation.simulator import simulate
from modeling.mcm_battery_drain.BatteryModel.models.state import BatteryState
from modeling.mcm_battery_drain.BatteryModel.models.behavior import UserBehavior
from modeling.mcm_battery_drain.BatteryModel.plots import plot_0 

def main():

    state = BatteryState()
    user = UserBehavior()
    history = simulate(state, user)
    
    plot_0.soc_plot(history)
    plot_0.soh_plot(history)
    plot_0.temp_plot(history)
    plot_0.behavior_plot(history)
    plot_0.ecm_plot(history)
    plot_0.soc_temp_plot(history)
    plot_0.soc_voltage_plot(history)
    plot_0.soc_temp_voltage_plot(history)
    plot_0.heat_map_plot(history)

if __name__ == "__main__":
    main()
    
