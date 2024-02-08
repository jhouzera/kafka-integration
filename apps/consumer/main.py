from confluent_kafka import Consumer, KafkaError
import os

# Configurações e variáveis
broker = os.environ['BROKER_ADDRESS']
grupo = 'test-consumers'
topico = 'test-topic'

def consume_msg_kafka(broker, grupo, topico):
    # Configuração do Consumer
    conf = {
        'bootstrap.servers': broker,
        'group.id': grupo,
        'auto.offset.reset': 'earliest'
    }

    # Criar Consumer
    consumer = Consumer(conf)

    # Assinar o Tópico
    consumer.subscribe([topico])

    try:
        while True:
            # Aguardar mensagens
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # Fim da partição, continuar consumindo
                    continue
                else:
                    print('Erro ao tentar ler a mensagem!\nERRO: {}'.format(msg.error()))
                    break

            # Processar as mensagens
            print('Mensagem recebida com sucesso!\n{}'.format(msg.value().decode('utf-8')))
            print('---------------------------------')

    except KeyboardInterrupt:
        pass
    finally:
        # Fechar o Consumer
        consumer.close()

consume_msg_kafka(broker, grupo, topico)
