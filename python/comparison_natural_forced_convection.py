from experiment_analysis import *

# comparison between natural and forced convection
# data of each experiment
temperatures_natural = []
temperatures_forced = []
temperatures_natural = [data[0][j] for j in range(3, 13)]
temperatures_forced = [data[1][j] for j in range(3, 13)]
temperature_environment = data[0][13]

for i in range(len(data)):

    # configurations
    fig_size = 8
    figFontSize = 14
    fig = plt.figure(i, figsize=(fig_size,fig_size))
    ax = fig.add_subplot(111)

    # plot
    ax.plot(positions, temperatures_natural, "-ks")
    ax.plot(positions, temperatures_forced, "-k^")
    ax.axhline(y=temperature_environment, color="k", linestyle="-", linewidth=1.8)
    ax.grid(True)

    # figure insert information
    figure_dir = r"experiment_analysis/"
    figure_name = figure_dir + r"comparison_natural_forced_convection.png"
    text_title = r"Distribui\c c\~ao de temperatura no\\tubo de calor em fun\c c\~ao do comprimento"
    text_xlabel = r"Comprimento [$mm$]"
    text_ylabel = r"Temperatura [$C$]"
    legend = ["Convec\c c\~ao natural", "Convec\c c\~ao for\c cada", "Ambiente"]

    # set figure informations
    ax.set_title(text_title, multialignment="center")
    ax.set_xlabel(text_xlabel, fontsize=figFontSize)
    ax.set_ylabel(text_ylabel, fontsize=figFontSize)
    ax.legend(legend)
    fig.savefig(figure_name)
    plt.close(fig)
