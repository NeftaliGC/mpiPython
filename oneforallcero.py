from mpi4py import MPI
import numpy as np
import argparse

def one_to_all_bc(d, my_id, X):
    mask = (1 << d) - 1  # 2^d - 1

    for i in range(d - 1, -1, -1):
        mask = mask ^ (1 << i)  # mask = mask XOR 2^i

        if (my_id & mask) == 0:
            if (my_id & (1 << i)) == 0:
                msg_destination = my_id ^ (1 << i)  # my_id XOR 2^i
                comm.send(X, dest=msg_destination)
            else:
                msg_source = my_id ^ (1 << i)  # my_id XOR 2^i
                X = comm.recv(source=msg_source)

    return X

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='MPI messaje.')
    parser.add_argument('X', type=str, help='The message to be broadcasted')

    args = parser.parse_args()

    comm = MPI.COMM_WORLD
    my_id = comm.Get_rank()
    num_procs = comm.Get_size()

    # Calculate the dimension 'd' of the hypercube
    d = int(np.log2(num_procs))
    assert 2**d == num_procs, "Number of processes must be a power of 2"

    # The message to be broadcasted
    if my_id == 0:
        X = args.X
    else:
        X = None

    X = one_to_all_bc(d, my_id, X)

    print(f"Process {my_id} received message: {X}")
