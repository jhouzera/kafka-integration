from confluent_kafka import Consumer
import os

### Configurações e variáveis
broker = os.environ['BROKER_ADDRESS']
group_name = 'test-consumers'
topic_name = 'test-topic'

### Definição de função para consumir as mensagens
def consumer_msg_broker(broker, group_name, topic_name):
    
    ### Configuração do Consumer
    conf = {
        'bootstrap.servers': broker,
        'group.id': group_name,
        'auto.offset.reset': 'earliest'
    }
    
    ### Criação do Consumer com as configurações
    consumer = Consumer(conf)

    ### Criando uma função mostrar que o tópico foi assinado com informações da
    def print_assignment(consumer, partitions):
        print('Tópico assinado:', partitions)

    ### Assinar o tópico
    consumer.subscribe([topic_name], on_assign=print_assignment)

    ## Tentar obter as mensagens do tópico
    try:
        while True:
            msg = consumer.poll(0.1)
            if msg is None:
                continue
            if msg.error():
                print('Erro ao obter mensagem!\nERRO: {}'.format(msg.error()))
                continue
            print('Mensagem recebida com sucesso!\n{}'.format(msg.value().decode('utf-8')))
            print('---------------------------------')
    finally:
        ### Finaliza a sessão
        consumer.close()

consumer_msg_broker(broker, group_name, topic_name)