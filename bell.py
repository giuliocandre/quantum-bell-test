from qiskit import *
import numpy as np
import matplotlib.pyplot as plt

def convert_basis(num):
    return 1 if num else -1

def get_correlation(result_list):
    sum = 0
    i = 0
    for pair in result_list:
        first = convert_basis(int(pair[0]))
        second = convert_basis(int(pair[1]))
        sum += first*second
        i += 1
    
    return sum/i

def eprb_experiment(angle=0):

    # Initialize quantum circuit and add 2 classical and 2 quantum registers
    qc = QuantumCircuit()
    qr = QuantumRegister(2, 'qreg')
    cr = ClassicalRegister(2,'creg')
    qc.add_register(qr)
    qc.add_register(cr)

    # Goal: build singlet entangled state
    qc.x(qr[1])
    qc.x(qr[0])
    qc.z(qr[1])
    # Now I have -|11> state
    qc.h(qr[0])
    qc.cx(qr[0], qr[1])
    # Now I have a singlet 2-qubit state. I expect correlation to be exaclty -1
    
    # rotate one of two qubits before measuring
    if (angle):
        qc.rx(angle, qr[1])

    qc.measure(qr[0],cr[0])
    qc.measure(qr[1],cr[1])
    # qc.draw(output='mpl').show()

    emulator = Aer.get_backend('qasm_simulator')
    job = execute(qc, emulator, memory=True, shots=2048)
    res = job.result()

    return res.get_memory()

def draw_correlation_plot():
    angles = np.linspace(0, 2*np.pi, 400)
    correlations = []
    theta = 0
    for theta in angles:
        results = eprb_experiment(angle=theta)
        corr = get_correlation(results)
        correlations.append(corr)

    predicted = -np.cos(angles)
    angles = [x*180/np.pi for x in angles]
    plt.plot(angles, correlations)
    plt.plot(angles, predicted)
    plt.ylabel("Correlation")
    plt.xlabel("Angle between detectors (degrees)")
    # plt.xscale()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    draw_correlation_plot()