import numpy as np
import matplotlib.pyplot as plt
import Transmitter as transmit


def generate_noise(variance, n):
    return np.random.normal(0, np.sqrt(variance), n)


def generate_correlated_noise(noise_cov_matrix, n):
    samples = np.random.multivariate_normal([0, 0, 0], noise_cov_matrix, n)
    return samples[:, 0], samples[:, 1], samples[:, 2]


# def received_voltage(s_array, variance):
#     r_array = []
#     for s in s_array:
#         r = s + np.random.normal(0, np.sqrt(variance))
#         r_array.append(r)
#     return np.array(r_array)


def received_voltage(s_array, n_array):
    return s_array + n_array


def show_hist(rv):

    mu = np.mean(rv)
    sigma = np.sqrt(np.var(rv))
    # print("mu: ", mu)
    # print("sigma: ", sigma)
    count, bins, ignored = plt.hist(rv, 30, density=True)

    # plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
    #          np.exp(- (bins - mu)**2 / (2 * sigma**2)),
    #          linewidth=2, color='r')
    # plt.plot(np.sort(noise), 1/(sigma * np.sqrt(2 * np.pi)) *
    #          np.exp(- (np.sort(noise) - mu)**2 / (2 * sigma**2)),
    #          linewidth=2, color='r')
    plt.show()


if __name__ == "__main__":
    # test
    mi_array = transmit.generate_mi(0.5, 50)
    E = 9
    Pm0 = 0.5
    var1 = 1
    var2 = 9
    var3 = 9
    s = transmit.voltage_s(mi_array, E)
    n1 = generate_noise(var1, 50)
    n2 = generate_noise(var2, 50)
    n3 = generate_noise(var3, 50)
    print(n2)

    r1 = received_voltage(s, n1)
    r2 = received_voltage(s, n2)
    r3 = received_voltage(s, n3)

    print(r1)
