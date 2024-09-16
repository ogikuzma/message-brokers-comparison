# Get Started

## Generation of test messages
Firstly, by following the steps below, prepare messages with the random content that will be used for execution of tests:
1. Run command:
```
make generate-messages
```
2. That's it. Messages in varying storage sizes will be generated in the directory with the random content.

## Test preparation
In order to execute an experiment in a local environment, follow the steps below:
1. Create a Python virtuel environment with required libraries:
```
make generate-venv
```
2. Start `Docker` if not started
3. Start the required infrastructure:
```
make start-infra
```

## Test execution
A test is run in 3 steps.
1. Execute the `python -m drivers.[MESSAGE_BROKER].consumer` command with the preffered parameters in other to start a consumer. 
Example below starts a RabbitMQ consumer that listens for 1000 small size messages. 
```
python -m drivers.rabbitmq.consumer --msg_size mala --num_of_msgs 1000
```
2. Once you get a message saying the consumer is ready, in another bash terminal run the `python -m drivers.[MESSAGE_BROKER].producer` command with the preffered parameters in other to start a producer. The producer parameters should match the consumer parameters for the proper test execution.
Example:
```
python -m drivers.rabbitmq.producer --msg_size mala --num_of_msgs 1000
```
3. Upon receiving messages that both the producer and consumer finished their work, you could run the `python -m metrics_extractor.extract_metrics --msg_broker [MESSAGE_BROKER]` command in order to see the test results in the console.
4. That's it. The test has been finished.

## Shutdown infrastructure
1. Shutdown the infrastructure upon finishing with tests execution:
```
make stop-infra
```