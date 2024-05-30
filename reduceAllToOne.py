from mpi4py import MPI
import numpy as np
import argparse

def all_to_one_reduce(d, my_id, m, X):
    comm = MPI.COMM_WORLD
    sum = np.copy(X)
    mask = 0

    for i in range(d):
        if (my_id & mask) == 0:
            if (my_id & (1 << i)) != 0:
                msg_destination = my_id ^ (1 << i)
                comm.Send([sum, MPI.DOUBLE], dest=msg_destination)
            else:
                msg_source = my_id ^ (1 << i)
                received_sum = np.empty(m, dtype='d')
                comm.Recv([received_sum, MPI.DOUBLE], source=msg_source)
                sum += received_sum
        mask ^= (1 << i)

    return sum

def main():

    parser = argparse.ArgumentParser(description='MPI vector.')
    parser.add_argument('m', type=int, help='The size of the vector')
    parser.add_argument('X', type=str, help='The vector to be reduced')

    args = parser.parse_args()

    comm = MPI.COMM_WORLD
    my_id = comm.Get_rank()
    num_procs = comm.Get_size()


    # Supongamos que cada procesador tiene el mismo vector X para simplificar.
    # En un escenario real, cada procesador podría tener diferentes datos.
    m = args.m

    if args.X == 'random':
        # Vector aleatorio
        X = np.random.rand(m).round(2) * 100

    if args.X == 'my_id':
        # Vector con el id del procesador
        X = np.full(m, my_id, dtype='d')

    if args.X == 'ones':
        # Vector de unos
        X = np.ones(m, dtype='d')

    print(f"Proceso {my_id} tiene el vector {X}")

    # Calcular d como el log2 del número de procesadores
    d = int(np.log2(num_procs))

    result = all_to_one_reduce(d, my_id, m, X)

    # Solo el procesador 0 imprimirá el resultado final.
    if my_id == 0:
        print("-------------------------")
        print("Resultado final en el nodo 0:", result)

if __name__ == "__main__":
    main()
