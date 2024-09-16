# Kako početi

## Generisanje testnih poruka
Prvo je potrebno generisati poruke nasumične sadržine koje će biti korišćene za izvršavanja testova:
1. Izvršiti komandu:
```
make generate-messages
```
2. Poruke različitih skladišnih dimenzija i nasumičnih sadržaja biće generisane i vidljive u `messages` direktorijumu

## Priprema za izvršenje testova
Kako bi izvršili eksperiment u lokalnom okruženju, pratite korake ispod:
1. Kreirati Python virtuelno okruženje sa neophodnim bibliotekama:
```
make generate-venv
```
2. Pokrenuti `Docker` ako nije već pokrenut
3. Pokrenuti neophodnu infrastrukturu izvršenjem komande ispod:
```
make start-infra
```

## Izvršavanje testova
Svaki test je potrebno izvršiti u 3 koraka:

1. Izvršiti komandu `python -m drivers.[MESSAGE_BROKER].consumer` sa željenim parametrima kako bi se pokrenuo konzument poruka.
Primer naveden ispod pokreće RabbitMq konzument poruka koji osluškuje i čeka 1000 malih poruka:
```
python -m drivers.rabbitmq.consumer --msg_size mala --num_of_msgs 1000
```
2. Nakon što se u konzoli prikaže poruka da je konzument poruka spreman, u drugom terminalu je potrebno pokrenuti komandu `python -m drivers.[MESSAGE_BROKER].producer` sa željenim parametrima kako si pokrenuo generator poruka. Parametri navedeni ovde moraju da se poklapaju sa parametrima postavljenim prilikom pokretanja konzumenta poruka.
Primer:
```
python -m drivers.rabbitmq.producer --msg_size mala --num_of_msgs 1000
```
3. Nakon što i generator i konzument poruka završe svoj posao, potrebno je pokrenuti komandu `python -m metrics_extractor.extract_metrics --msg_broker [MESSAGE_BROKER]` kako bi rezultati testa postali vidljivi u konzoli.

## Zaustavljanje pokrenutih resursa
1. Nakon završetka izvršavanja testova, osloboditi pokrenute resurse izvršenjem korake ispod:
```
make stop-infra
```