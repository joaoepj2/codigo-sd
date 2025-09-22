import grpc
import soma1_pb2
import soma1_pb2_grpc


def run():
    canal = grpc.insecure_channel('localhost:50051')
    stub = soma1_pb2_grpc.Soma1RPCStub(canal)
    num1 = input('Entre com o 1º valor: ')
    num2 = input('Entre com o 2º valor: ')
    requisicao = soma1_pb2.RequisicaoSoma1(a=int(num1),b=int(num2))
    resposta = stub.Soma1(requisicao)
    print("O resultado é ", resposta)


if __name__ == "__main__":
    run()