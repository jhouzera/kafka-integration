# kafka-integration
Aplicação simples de um Producer e Consumer em Python para o Kafka (broker)

## Requisitos:
* Servidor Kafka configurado com um Broker e Zookeeper;
* Minikube para deploy das aplicações e stack de métricas;
* kubectl
* helm

## Deploy de Stack de Métricas no Minikube
1) Inicialize o Minikube:
```bash
$ minikube start
```
2) Crie um namespace chamado 'monitoring':
```bash
$ kubectl create ns monitoring
```
3) Adicione o repositório do helm chart 'prometheus-community':
```bash
$ helm repo add prometheus-community * https://prometheus-community.github.io/helm-charts
```
4) Altere os parametros que julgar necessário no values.yaml, crie um template a partir do helm chart e aplique:
```bash
$ helm template kube-prometheus-stack -f values.yaml . > monitoring-stack.yaml
$ kubectl apply -f monitoring-stack.yaml -n monitoring
```
5) Depois verifique se todos recursos foram aplicados e se os Pods inicializaram com sucesso:
```bash
$ kubectl get pods -n monitoring
```

## Deploy do Producer e Consumer no Minikube
1) Com o Minikube já inicializado, crie um namespace chamado kafka-integration:
```bash
$ kubectl create ns kafka-integration
```
2) Vá ao diretório 'app' e seguida 'deploy' para implementar o Consumer e Producer:
```bash
$ kubectl apply -f consumer.yaml -n kafka-integration
$ kubectl apply -f producer.yaml -n kafka-integration
```
3) Depois verifique se todos recursos foram aplicados e se os Pods inicializaram com sucesso::
```bash
$ kubectl get pods -n monitoring
```
4) Analise os logs do Consumer e do Producer para verificar se as mensagens estão sendo enviadas e consumidas (altere as variáveis pelo nome dos pods):
```bash
$ kubectl logs -f ${CONSUMER_POD_NAME} -n kafka-integration
$ kubectl logs -n ${PRODUCER_POD_NAME} -n kafka-integration
```

## Referências:
* https://github.com/confluentinc/confluent-kafka-python
* https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html
* https://github.com/prometheus/jmx_exporter/tree/main
* https://docs.confluent.io/platform/current/kafka/authentication_sasl/authentication_sasl_gssapi.html
* https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/managing_smart_cards/using_kerberos
* https://docs.cloudera.com/runtime/7.2.17/zookeeper-security/topics/zookeeper-configure-client-shell-kerberos-authentication.html
* https://docs.confluent.io/platform/current/kafka/monitoring.html
* https://medium.com/@rramiz.rraza/kafka-metrics-integration-with-prometheus-and-grafana-14fe318fbb8b
* https://grafana.com/grafana/dashboards/11962-kafka-metrics/
* https://github.com/grafana/helm-charts/tree/main/charts/grafana
* https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack
* https://github.com/shafiquejamal/kafka-zookeeper-kerberos/tree/master
* https://www.confluent.io/blog/kafka-listeners-explained/?utm_medium=sem&utm_source=google&utm_campaign=ch.sem_br.nonbrand_tp.prs_tgt.dsa_mt.dsa_rgn.latam_lng.eng_dv.all_con.blog&utm_term=&creative=&device=c&placement=&gad_source=1&gclid=Cj0KCQiAzoeuBhDqARIsAMdH14F6t3bgs3Zn-d-excEdWQ3z7aJBEfn5RrS342uD0IqTkyn91cOx5w0aAoztEALw_wcB
