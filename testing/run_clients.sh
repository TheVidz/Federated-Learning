#!/bin/bash

NUM_CLIENTS=5  # Number of clients
for ((i=0; i<$NUM_CLIENTS; i++))
do
   python3 client.py $i $NUM_CLIENTS &
done

wait
