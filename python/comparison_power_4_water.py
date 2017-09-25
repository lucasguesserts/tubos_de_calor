from experiment_analysis import *

# comparison between natural and forced convection
# data of each experiment
temperatures_natural = []
temperatures_forced = []
temperatures_20 = [data[51][j] for j in range(3, 13)]
temperatures_40 = [data[52][j] for j in range(3, 13)]
temperatures_60= [data[53][j] for j in range(3, 13)]
temperatures_80 = [data[54][j] for j in range(3, 13)]
temperature_environment = data[53][13]

# configurations
fig_size = 8
figFontSize = 14
fig = plt.figure(0, figsize=(fig_size,fig_size))
ax = fig.add_subplot(111)

# plot
ax.plot(positions, temperatures_20, "-bs")
ax.plot(positions, temperatures_40, "-gs")
ax.plot(positions, temperatures_60, "-ys")
ax.plot(positions, temperatures_80, "-rs")
ax.axhline(y=temperature_environment, color="k", linestyle="-", linewidth=1.8)
ax.grid(True)

# figure insert information
figure_dir = r"experiment_analysis/"
figure_name = figure_dir + r"comparison_power_4_water.png"
text_title = r"Distribui\c c\~ao de temperatura no\\tubo de calor em fun\c c\~ao do comprimento"
text_xlabel = r"Comprimento [$mm$]"
text_ylabel = r"Temperatura [$C$]"
legend = ["20 $[W]$","40 $[W]$","60 $[W]$","80 $[W]$","Ambiente"]

# set figure informations
ax.set_title(text_title, multialignment="center")
ax.set_xlabel(text_xlabel, fontsize=figFontSize)
ax.set_ylabel(text_ylabel, fontsize=figFontSize)
ax.legend(legend)
fig.savefig(figure_name)
plt.close(fig)
