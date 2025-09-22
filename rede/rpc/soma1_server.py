from concurrent import futures
import logging

import grpc
import soma1_pb2
import soma1_pb2_grpc


class Soma1RPCServicer(soma1_pb2_grpc.Soma1RPCServicer):
    def Soma1(self, request, context):
        print("Somando os seguintes numeros ",request.a, request.b)
        return soma1_pb2.RespostaSoma1(res=request.a+request.b) 



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    soma1_pb2_grpc.add_Soma1RPCServicer_to_server(
        Soma1RPCServicer(), server
    )
    print("server created..")
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()