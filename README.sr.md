# Kako početi

## Preduslovi
- `Linux` operativni sistem zbog nedostatka podrške biblioteke `rocketmq-client-python` za `Windows` operativni sistem, kao i Mac računare zasnovane na `M` procesorima
  - `rocketmq-client-python` biblioteka se može instalirati praćenjem uputstva sa linka:  https://github.com/apache/rocketmq-client-python

## Generisanje testnih poruka
Prvo je potrebno generisati tekstualne poruke nasumične sadržine koje će biti korišćene za izvršavanja testova:
1. Izvršiti komandu:
```
make generate-messages
```
2. Poruke različitih skladišnih dimenzija i nasumičnih sadržaja biće generisane i vidljive u `messages` direktorijumu

## Priprema za izvršenje testova
Kako bi izvršili eksperiment, pratite korake ispod:
1. Kreirati Python virtuelno okruženje sa neophodnim bibliotekama:
```
make generate-venv
```
2. Pokrenuti `Docker` ako nije već pokrenut
3. Pokrenuti neophodnu infrastrukturu izvršenjem komande ispod:
```
make start-[rabbitmq | nats | rocketmq]
```

## Izvršavanje testova
1. U `test_config.json` fajlu je potrebno podesiti željene parametre:
- `msg_broker`: `rabbitmq | nats | rocketmq`
- `msg_size`: `mala | srednja | velika`
- `num_of_msgs`: broj poruka
- `env`: okruženje u kojem se test izvršava
2. Pokrenuti konzumenta poruka sa komandom `python consumer.py`
3. Nakon što se u konzoli prikaže poruka da je konzument poruka spreman, 
u drugoj konzoli pokrenuti generatora poruka sa komandom `python producer.py`. Generator poruka će krenuti da generiše poruke.
4. Nakon što i generator i konzument poruka završe svoja zaduženja, potrebno je pokrenuti komandu `python extract_metrics.py` kako bi rezultati testa postali vidljivi u terminalu.

## Zaustavljanje pokrenutih resursa
1. Nakon završetka izvršavanja testova, osloboditi pokrenute resurse izvršenjem korake ispod:
```
make stop-[rabbitmq | nats | rocketmq]
```