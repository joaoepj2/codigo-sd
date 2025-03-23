import socket
import time
 
host = "44.201.233.10"
port = 50000

 
sock = socket.socket(socket.AF_INET, # Internet
    socket.SOCK_DGRAM) # UDP


for counter in range(1, 101):
    print("Enviando a mensagem " + str(counter) + " para o IP " + str(host) + ", porta " + str(port))
    message = "Eu sou o Datagrama numero " + str(counter) + " Lorem ipsum dolor sit amet. Nam veritatis molestiae et voluptatum sunt quo animi quasi qui expedita natus At internos itaque id excepturi distinctio. Est beatae veritatis 33 velit dolore ut doloremque numquam hic sunt excepturi qui minima voluptas! Et libero eligendi et aperiam consequatur in excepturi consequuntur qui incidunt suscipit et tenetur placeat est consequatur internos. Non porro rerum ab magnam voluptates ea amet voluptatem ut officia accusantium. Ad impedit exercitationem ut inventore voluptatem est ipsum voluptatum At officia distinctio est dolores impedit. Id iusto quia rem explicabo quos hic velit eius aut pariatur nisi. Sit numquam veritatis ab minus ullam aut porro numquam sed perferendis enim et nesciunt illo id corporis dolorem eum sint sequi. Non dignissimos cumque sed consectetur minus et corporis molestiae. Sit consequatur quibusdam id sunt quae 33 dolores deleniti qui voluptatem doloribus et alias minima ad iste veniam et voluptas voluptatibus! Sit officia cumque cum vitae atque qui suscipit voluptatem est dicta necessitatibus! Ex consectetur voluptas aut facilis distinctio et enim fugit non itaque voluptatum vel autem sapiente. Aut vero placeat est quia sequi et asperiores vitae id iste consequatur ex dolorem placeat sed vitae molestiae. Quo rerum nostrum et culpa accusantium id enim beatae et ullam pariatur et nulla aperiam quo ipsum beatae? Et suscipit expedita est incidunt laboriosam sed tempora voluptatem non nostrum quia ut deleniti eligendi vel quaerat fugiat. Eum nobis repellendus est saepe quis et repudiandae deserunt sit placeat impedit 33 excepturi quia hic veniam officiis eos error architecto! Ut consequatur recusandae ut veritatis dolorum ad reiciendis sequi. Et eius pariatur sit internos autem quo voluptatem deserunt. 33 maiores dignissimos eum itaque quod est officiis deleniti et rerum maxime et voluptatem nobis quo nostrum excepturi qui saepe culpa. Et consequatur nobis sed labore dolore et galisum tempora eos deserunt sint aut sunt inventore ut aperiam nobis ut odit quasi! Est sapiente amet et enim sunt aut eligendi magnam sed quia optio in voluptas quas. Eum voluptatum necessitatibus est consequatur sequi aut enim adipisci. Eum quod voluptatem in itaque laboriosam et voluptates quia qui distinctio aperiam ut dolores voluptatum. Aut doloremque blanditiis est incidunt rerum ut velit quibusdam ea impedit tempore. Ut dolor porro in voluptas omnis a pariatur minus est consequuntur iure. Aut nostrum voluptas et temporibus galisum vel maxime magni et voluptate dicta et alias voluptate et nisi atque. Ad amet soluta aut quia fugit et asperiores optio est voluptatibus commodi est tenetur illo qui voluptas galisum. Aut vitae voluptatem et veniam tempore vel saepe suscipit vel magnam vitae ea blanditiis aperiam eum enim iure?"
    messageBytes = bytearray(message, "ascii")
    
    time.sleep(0.1)
    sock.sendto(messageBytes, (host, port))