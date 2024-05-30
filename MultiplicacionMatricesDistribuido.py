from mpi4py import MPI
import numpy as np

def matrix_vector_product(matrix_A, vector):
    return np.dot(matrix_A, vector)

def get_column(matrix, col_index):
    return matrix[:, col_index]

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    N = 4  # Tamaño de las matrices (N x N)

    if rank == 0:
        # Proceso maestro
        matrix_A = np.array([
                                [1, 2, 3, 4],
                                [5, 6, 7, 8],
                                [9, 10, 11, 12],
                                [13, 14, 15, 16]
                            ])
        matrix_B = np.array([
                                [16, 17, 18, 19],
                                [20, 21, 22, 23],
                                [24, 25, 26, 27],
                                [28, 29, 30, 31]
                            ])

        matrix_C = np.zeros((N, N))

        # Broadcast de matrix_A a todos los procesos
        comm.bcast(matrix_A, root=0)

        # Enviar columnas de matrix_B a los esclavos
        for i in range(1, min(size, N + 1)):
            comm.send(get_column(matrix_B, i - 1), dest=i, tag=i - 1)

        numsent = min(N, size - 1)
        numrec = 0

        while numrec < N:
            status = MPI.Status()
            column = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
            source_worker = status.Get_source()
            col_index = status.Get_tag()

            matrix_C[:, col_index] = column
            numrec += 1

            if numsent < N:
                comm.send(get_column(matrix_B, numsent), dest=source_worker, tag=numsent)
                numsent += 1
            else:
                comm.send(None, dest=source_worker, tag=N)

        #Imprimir matrices originales
        print("Matriz A:")
        print(matrix_A)
        print("\n")
        print("Matriz B:")
        print(matrix_B)
        print("\n")


        # Convertir a enteros antes de imprimir
        matrix_C = matrix_C.astype(int)
        print("Matriz C (resultado):")
        print(matrix_C)

    else:
        # Código del esclavo
        matrix_A = comm.bcast(None, root=0)

        while True:
            status = MPI.Status()
            column = comm.recv(source=0, tag=MPI.ANY_TAG, status=status)
            col_index = status.Get_tag()

            if col_index == N:
                break

            result = matrix_vector_product(matrix_A, column)
            comm.send(result, dest=0, tag=col_index)

if __name__ == '__main__':
    main()