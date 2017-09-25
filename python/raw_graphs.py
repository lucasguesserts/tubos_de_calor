from experiment_analysis import *
# data of each experiment
experiment_simple_data = []
powers = []
for i in range(len(data)):
    experiment_simple_data.append([data[i][j] for j in range(3, 13)])

# for row in experiment_simple_data:
    # print(row)
for fix_axis_limits in [True, False]:
    for i in range(len(data)):
        fig_size = 8
        figFontSize = 14
        fig = plt.figure(i, figsize=((1/0.7)*fig_size,fig_size))
        ax = fig.add_subplot(111)
        ax.plot(positions, experiment_simple_data[i], "-ks")
        ax.axhline(y=data[i][13], color="k", linestyle="-", linewidth=1.8)
        ax.grid(True)
        # Experiment description
        experiment_info = r"Experimento {}:\\\\\\".format(data[i][0])
        power_info = r"Pot\^encia: {:2.0f} [$W$]\\\\".format(data[i][2])
        inclination_info = r"Inclina\c c\~ao: {:2.0f} [$graus$]\\\\".format(data[i][1])
        fluid_info = r"Fluido: {:2.1f} $ml$ de {:s}\\\\".format(data[i][15], data[i][14])
        refrigeration_info = r"Refrigera\c c\~ao: convec\c c\~ao {:s}\\\\".format(data[i][16])
        air_velocity_info = r"Velocidade do ar: {:2.1f} [$m/s$]\\\\".format(data[i][17])
        adiabatic_info = r"Comprimento da se\c c\~ao\\adiab\'atica removido: {:2.0f} [$mm$]\\\\\\".format(1000*data[i][18])
        # temperature difference
        evaporator_temperatures = [data[i][j] for j in range(3,7)]
        adiabatic_temperatures = [data[i][j] for j in range(7,9)]
        condenser_temperatures = [data[i][j] for j in range(9,13)]
        all_temperatures = [data[i][j] for j in range(3,13)]
        DT_evaporator = max(evaporator_temperatures) - min(evaporator_temperatures)
        DT_adiabatic = max(adiabatic_temperatures) - min(adiabatic_temperatures)
        DT_condenser = max(condenser_temperatures) - min(condenser_temperatures)
        DT_total = max(all_temperatures) - min(all_temperatures)
        dt_evaporator_text = r"$\Delta T_{evaporador}$ = " + r"{:2.0f} [$C$]\\\\".format(DT_evaporator)
        dt_adiabatic_text = r"$\Delta T_{adiabatico}$ = " + r"{:2.0f} [$C$]\\\\".format(DT_adiabatic)
        dt_condenser_text = r"$\Delta T_{condensador}$ = " + r"{:2.0f} [$C$]\\\\\\".format(DT_condenser)
        environment_temperature = r"$T_{ambiente}$ = " + r"{:2.0f} [$C$]".format(data[i][13])
        T_max_text = r"$T_{max}$ = " + r"{:2.0f} [$C$]\\\\".format(max(all_temperatures))
        T_min_text = r"$T_{min}$ = " + r"{:2.0f} [$C$]\\\\".format(min(all_temperatures))
        dt_total_text = r"$\Delta T_{total}$ = " + r"{:2.0f} [$C$]\\\\".format(DT_total)
        description = experiment_info + power_info + inclination_info + fluid_info + refrigeration_info + air_velocity_info + adiabatic_info + dt_evaporator_text + dt_adiabatic_text + dt_condenser_text + T_max_text + T_min_text + dt_total_text + environment_temperature
        # figure insert information
        if fix_axis_limits:
            figure_dir = r"fixed_limits/"
        else:
            figure_dir = r"variable_limits/"
        figure_name = figure_dir + r"experiment_{}_power_{:2.0f}.png".format(data[i][0], data[i][2])
        text_title = r"Distribui\c c\~ao de temperatura no\\tubo de calor em fun\c c\~ao do comprimento"
        text_xlabel = r"Comprimento [$mm$]"
        text_ylabel = r"Temperatura [$C$]"
        legend = ["Tubo de calor", "Ambiente"]
        if fix_axis_limits:
            ylim = [20, 150]
            ax.set_ylim(ylim)
        else:
            pass
        ax.set_title(text_title, multialignment="center")
        ax.set_xlabel(text_xlabel, fontsize=figFontSize)
        ax.set_ylabel(text_ylabel, fontsize=figFontSize)
        ax.legend(legend)
        fig.text(0.72, 0.2, description, fontsize=figFontSize)
        fig.subplots_adjust(right=0.7)
        fig.savefig(figure_name)
        plt.close(fig)

