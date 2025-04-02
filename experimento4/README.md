# Experimento 4 - Enviando com intervalos de espera aleatóreos

Esse experimento envia 100 mensagens em sequencia com intervalos aleatóreos entre os envios. Ás vezes por conta de congestionamento na rede algum datagrama pode seguir por um caminho diferente dos outros fazendo com que ele chegue antes ou depois dos outros. Isso ocorre porque o serviço não oferece nenhuma garantia de que os datagramas serão recebidos na mesma ordem em que foram enviados.

O udpReceiver já está rodando na máquina remota
1. Execute o udpSender até obter resultados fora de ordem algumas vezes.
Cole os resultados no trabalho

Observe a ordem de chegada dos Datagramas!