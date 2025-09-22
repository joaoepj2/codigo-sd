import grpc
import soma2_pb2
import soma2_pb2_grpc


def run():
    canal = grpc.insecure_channel('localhost:50051')
    stub = soma2_pb2_grpc.Soma2RPCStub(canal)
    num_iterator = iterate()
    resposta = stub.Soma2(num_iterator)
    print("O resultado é ", resposta)


def iterate():
    while True:
        num = int(input('Entre com um valor (0 para terminar): '))
        if num == 0:
            break
        m = soma2_pb2.RequisicaoSoma2(a=num)
        yield m.a


if __name__ == "__main__":
    run()