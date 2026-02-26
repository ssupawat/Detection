from numpy import ndarray
from Channel import *
from DecisionRule import *
from Detection import *
from Transmitter import *
import matplotlib.pyplot as plt


def simulation(Pm0, var1, var2, var3, n, decision, noise_cov_matrix=None) -> ndarray:

    mi_array = generate_mi(Pm0, n)
    E = np.linspace(0.1, 10, num=100, endpoint=True)
    prob_of_error_array = []
    for e in E:
        s = transmit.voltage_s(mi_array, e)
        if decision == "optimalForNot":
            n1, n2, n3 = generate_correlated_noise(noise_cov_matrix, n)
        else:
            n1 = generate_noise(var1, n)
            n2 = generate_noise(var2, n)
            n3 = generate_noise(var3, n)
        r1 = received_voltage(s, n1)
        r2 = received_voltage(s, n2)
        r3 = received_voltage(s, n3)
        mhat_array = detection(Pm0=Pm0, E=e, r1=r1, r2=r2,
                               r3=r3, var1=var1, var2=var2, var3=var3,
                               decision=decision, noise_cov_matrix=noise_cov_matrix)
        prob_of_error_array.append(prob_of_error(mi_array, mhat_array))
    return np.array(prob_of_error_array)


if __name__ == '__main__':

    # Pm0, var1, var2, var3, message, decision = input(
    #     "Please enter Pm0, variance1, variance2, variance3, amount of random messages and decision method (optimal, arbitrary, optimalForNot):\n(ex. 0.5 9 9 9 50 optimalForNot)\n-> ").split(" ")
    # Pm0 = float(Pm0)
    # var1, var2, var3, message = [int(element)
    #                              for element in [var1, var2, var3, message]]
    # t1 = time.time()
    # print("processing...")
    # simulation(Pm0, var1, var2, var3, message, decision)
    # t2 = time.time() - t1
    # print(f'Calculated in {t2:0.2f} sec or {t2/60:0.2f} min.')

    n = 500000
    Pm0 = [0.5, 0.25, 0.5]
    var1 = [4, 9, 9]
    var2 = [9, 9, 16]
    var3 = [16, 9, 25]
    filename = ["opt_vs_abr1", "opt_vs_abr2", "opt_vs_abr3"]
    for i in range(3):
        figure, axis1 = plt.subplots(figsize=(8, 6))
        axis1.set_title("Optimal decision VS Arbitrary decision\n"+"Simulate transmittion using\n"
                        r"$P(m_{0})$" + f" = {Pm0[i]} " + r"$P(m_{1})$" + f" = {1-Pm0[i]} " + "\n" + r"$\sigma_{1}^2$" + f" = {var1[i]} " + r"$\sigma_{2}^2$" + f" = {var2[i]} " + r"$\sigma_{3}^2$" + f" = {var3[i]} ")
        axis1.set_yscale('log')
        E = np.linspace(0.1, 10, num=100, endpoint=True)
        optimal_prob_error_array = simulation(
            Pm0[i], var1[i], var2[i], var3[i], n, "optimal")
        arbitrary_prob_error_array = simulation(
            Pm0[i], var1[i], var2[i], var3[i], n, "arbitrary")
        axis1.plot(E, optimal_prob_error_array, label="Optimal decision")
        axis1.plot(E, arbitrary_prob_error_array, label="Arbitrary decision")
        axis1.set_xlabel('Signal energy')
        axis1.set_ylabel('Probability of Error')
        plt.legend(loc='upper left')
        plt.autoscale(enable=True, axis='x', tight=True)
        plt.tight_layout()
        plt.savefig(f'./Figure/{filename[i]}.png')
        # plt.show()

    filename = ["NOT_opt_vs_abr1", "NOT_opt_vs_abr2", "NOT_opt_vs_abr3"]
    for i in range(3):
        s1, s2, s3 = np.sqrt(var1[i]), np.sqrt(var2[i]), np.sqrt(var3[i])
        rho = 0.5
        noise_cov_matrix = np.array([
            [var1[i],        rho * s1 * s2, rho * s1 * s3],
            [rho * s1 * s2,  var2[i],       rho * s2 * s3],
            [rho * s1 * s3,  rho * s2 * s3, var3[i]]
        ])
        figure, axis1 = plt.subplots(figsize=(8, 6))
        axis1.set_title("Optimal decision VS Arbitrary decision\n"+"Simulate transmittion using\n"
                        r"$P(m_{0})$" + f" = {Pm0[i]} " + r"$P(m_{1})$" + f" = {1-Pm0[i]} " + "\n" + r"$\sigma_{1}^2$" + f" = {var1[i]} " + r"$\sigma_{2}^2$" + f" = {var2[i]} " + r"$\sigma_{3}^2$" + f" = {var3[i]} ")
        axis1.set_yscale('log')
        E = np.linspace(0.1, 10, num=100, endpoint=True)
        optimal_prob_error_array = simulation(
            Pm0[i], var1[i], var2[i], var3[i], n, "optimalForNot",
            noise_cov_matrix=noise_cov_matrix)
        arbitrary_prob_error_array = simulation(
            Pm0[i], var1[i], var2[i], var3[i], n, "arbitrary")
        axis1.plot(E, optimal_prob_error_array, label="Optimal decision")
        axis1.plot(E, arbitrary_prob_error_array, label="Arbitrary decision")
        axis1.set_xlabel('Signal energy')
        axis1.set_ylabel('Probability of Error')
        plt.legend(loc='upper left')
        plt.autoscale(enable=True, axis='x', tight=True)
        plt.tight_layout()
        plt.savefig(f'./Figure/{filename[i]}.png')
        # plt.show()
