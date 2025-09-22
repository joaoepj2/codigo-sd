from concurrent import futures
import logging

import grpc
import soma2_pb2
import soma2_pb2_grpc


class Soma2RPCServicer(soma2_pb2_grpc.Soma2RPCServicer):
    def Soma2(self, request_iterator, context):
        tmp = 0
        for num in request_iterator:
            print("Recebi o numero ", num)
            tmp = tmp + num
        return soma2_pb2.RespostaSoma2(res=tmp) 



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    soma2_pb2_grpc.add_Soma2RPCServicer_to_server(
        Soma2RPCServicer(), server
    )
    print("server created..")
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()