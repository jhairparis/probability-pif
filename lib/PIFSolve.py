from numpy import mean, std, linspace, percentile, exp
from math import gamma


def Solve(data, code: int, plt, print_: callable):
    #! Activity 1
    # Filter the data by the city code
    filtered_data = data[data["Cod_Div"] == code]
    wind_speed = filtered_data["Velocidad del Viento m/s"]
    temperature = filtered_data["Temperatura (°C)"]

    # Histogram wind vs temperature
    plt[0].hist2d(wind_speed, temperature, bins=(40), cmap="Reds")
    plt[0].set_xlabel("Velocidad")
    plt[0].set_ylabel("Temperatura")
    plt[0].set_title("Velocidad vs Temperatura")

    # Wind boxplot
    plt[1].boxplot(wind_speed)
    plt[1].set_title("Velocidad del viento")

    # Temperature boxplot
    plt[2].boxplot(temperature)
    plt[2].set_title("Temperatura")

    # Calculation of data to obtain the variables k and c
    average = mean(wind_speed)
    deviation = std(wind_speed)

    k = (deviation / average) ** -1.09
    print_("Valor de $k$: ", k)

    c = average / (gamma(1 + (1 / k)))
    print_("Valor de $c$: ", c)

    # Substitution of the values of k and c in the probability density function
    wind_values = linspace(min(wind_speed), max(wind_speed), len(wind_speed))
    pdf = (k / c) * ((wind_values / c) ** (k - 1)) * exp(-((wind_values / c) ** k))

    #! Activity 2
    # Graph of the probability density function
    plt[3].plot(wind_values, pdf, label="Distribución Weibull")
    plt[3].set_title("Distribución Weibull")
    plt[3].set_xlabel("Velocidad del viento")
    plt[3].set_ylabel("Función de densidad de probabilidad")

    # Most probable speed
    most_probable_speed = c * (((k - 1) / k) ** (1 / k))
    print_("Velocidad más probable: ", most_probable_speed)

    # Maximum energy speed
    max_energy_speed = c * (((k + 2) / k) ** (1 / k))
    print_("Velocidad máxima energía: ", max_energy_speed)

    #! Activity 3
    # Calculation of quartile 1, quartile 3 and interquartile range
    quartile1 = percentile(wind_speed, 25)
    print_("Cuartil 1 del viento: ", quartile1)

    quartile3 = percentile(wind_speed, 75)
    print_("Cuartil 3 del viento: ", quartile3)

    interquartile_range = quartile3 - quartile1
    print_("Rango intercuartil: ", interquartile_range)

    #  Function to determine the probability
    def weibull_cdf(v, c, k):
        return 1 - exp(-((v / c) ** k))

    # Probability that the wind speed is within the interquartile range
    range_probability = weibull_cdf(quartile3, c, k) - weibull_cdf(quartile1, c, k)
    print_(
        "Probabilidad de que la velocidad del viento esté \n  entre dentro del rango Intercuartil: ",
        range_probability,
    )

    # Probability that the wind speed is higher than the 60th percentile
    percentile60 = percentile(wind_speed, 60)
    probability_above_60 = 1 - weibull_cdf(percentile60, c, k)
    print_(
        "Probabilidad de que la velocidad del viento sea \n  superior al percentil 60: ",
        probability_above_60,
    )