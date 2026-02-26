import numpy as np
from Channel import received_voltage, generate_noise
import Transmitter as transmit
import DecisionRule
import time


def detection(Pm0, E, r1, r2, r3, var1, var2, var3, decision, noise_cov_matrix=None):
    mhat = []
    if decision == "optimal":
        for i in range(r1.shape[0]):
            decision_result = DecisionRule.ODR(
                Pm0=Pm0, E=E, r1=r1[i], r2=r2[i], r3=r3[i], var1=var1, var2=var2, var3=var3)
            mhat.append(decision_result)
    elif decision == "arbitrary":
        for i in range(r1.shape[0]):
            decision_result = DecisionRule.ABR(r1=r1[i], r2=r2[i], r3=r3[i])
            mhat.append(decision_result)
    elif decision == "optimalForNot":
        for i in range(r1.shape[0]):
            decision_result = DecisionRule.ODR_NOT(
                Pm0, E, r1[i], r2[i], r3[i], noise_cov_matrix)
            mhat.append(decision_result)
    return np.array(mhat)


def prob_of_error(mi, mhat):
    error = 0
    for mi_element, mhat_element in zip(mi, mhat):
        if mi_element != mhat_element:
            error += 1
        else:
            continue
    return error / mi.shape[0]


if __name__ == "__main__":
    # test
    mi_array = transmit.generate_mi(0.5, 5)
    E = 9
    Pm0 = 0.5
    var1 = 1
    var2 = 1
    var3 = 1
    s = transmit.voltage_s(mi_array, E)

    r1 = received_voltage(s, var1)
    r2 = received_voltage(s, var2)
    r3 = received_voltage(s, var3)

    result = detection(Pm0, E, r1, r2, r3, var1, var2, var3)
    print(s)
    print(r1)
    print(r2)
    print(r3)
    print(mi_array)
    print(result)
    print(result.shape[0])
    print(prob_of_error(mi=mi_array, mhat=result))
