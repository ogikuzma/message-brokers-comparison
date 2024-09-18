# Get Started

## Prerequisites
- `Linux` OS due to lacking support of `rocketmq-client-python` library for `Windows` OS and Mac computers with the `M` processors.

## Generation of test messages
Firstly, by following the steps below, prepare messages that will be used for execution of tests by creating txt filed with some random content:
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
1. In the `test_config.json` file set the preffered test configuration parameters:
- `msg_broker`: `rabbitmq | nats | rocketmq`
- `msg_size`: `mala | srednja | velika`
- `num_of_msgs`: number of messages
2. Start the consumer with the command `python consumer.py`
3. Once you get a message saying the consumer is ready, in another console, start the producer with the command `python producer.py`. Producer will start generating messages.
4. Upon receiving messages that both the producer and consumer finished their work, run the `python extract_metrics` command in order to see the test results in the console.
5. That's it. The test has been finished.

## Shutdown infrastructure
1. Shutdown the infrastructure upon finishing with tests execution:
```
make stop-infra
```