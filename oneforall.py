from mpi4py import MPI
import numpy as np
import argparse

def general_one_to_all_bc(d, my_id, source, X):
    my_virtual_id = my_id ^ source
    mask = (1 << d) - 1  # 2^d - 1

    for i in range(d - 1, -1, -1):
        mask = mask ^ (1 << i)  # mask = mask XOR 2^i

        if (my_virtual_id & mask) == 0:
            if (my_virtual_id & (1 << i)) == 0:
                virtual_dest = my_virtual_id ^ (1 << i)
                physical_dest = virtual_dest ^ source
                if X is not None:
                    comm.send(X, dest=physical_dest)
            else:
                virtual_source = my_virtual_id ^ (1 << i)
                physical_source = virtual_source ^ source
                if X is None:
                    X = comm.recv(source=physical_source)
                else:
                    comm.send(X, dest=physical_source)

    return X

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='MPI messaje.')
    parser.add_argument('X', type=str, help='The message to be broadcasted')
    parser.add_argument('source', type=int, help='The source of the broadcast')

    args = parser.parse_args()

    comm = MPI.COMM_WORLD
    my_id = comm.Get_rank()
    num_procs = comm.Get_size()

    # Calculate the dimension 'd' of the hypercube
    d = int(np.log2(num_procs))
    assert 2**d == num_procs, "Number of processes must be a power of 2"

    # Source of the broadcast
    source = args.source  # You can change this to any valid rank
    # The message to be broadcasted
    if my_id == source:
        X = args.X
    else:
        X = None

    X = general_one_to_all_bc(d, my_id, source, X)

    print(f"Process {my_id} received message: {X}, source: {source}")
