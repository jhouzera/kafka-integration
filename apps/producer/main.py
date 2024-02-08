from confluent_kafka import Producer
import os
import random

### Configurações e variáveis
broker = os.environ['BROKER_ADDRESS']
topic_name = 'test-topic'
msg = 'Sequência randomica'

### Definindo uma função para validar o envio das mensagens:
def delivery_report(err, msg):
    if err is not None:
        print('Não foi possível enviar a mensagem\nERRO: {}'.format(err))
    else:
        print('Mensagem enviada com sucesso:\nTópico "{}" e partição[{}]'.format(msg.topic(), msg.partition()))
        print('------------------------------------')

### Definindo uma função para tentar eviar as mensagens:
def send_msg_to_broker(broker, topico, msg, max_attempt=3, wait_between_attempts=5):
    ### Quantidade de tentativas
    attempt = 1

    while attempt <= max_attempt:
        try:
            ### Configuração do Producer
            conf = {
                'bootstrap.servers': broker
                }

            ### Criação do Producer
            producer = Producer(conf)

            ### Envio das mensagens
            while True:
                n = random.random()
                producer.produce(topico, key=None, value="{0}: {1}".format(msg,n), callback=delivery_report)

                ### Aguardar confirmação de entrega
                producer.poll(1)

                ### Fechar o Producer
                producer.flush()

                ### Se chegou até aqui, a mensagem foi enviada com sucesso
                break

        except Exception as e:
            print('Erro ao enviar mensagem (attempt {}/{}): {}'.format(attempt, max_attempt, e))
            attempt += 1

            ### Aguardar um tempo antes de tentar enviar novamente
            import time
            time.sleep(wait_between_attempts)

send_msg_to_broker(broker, topic_name, msg)