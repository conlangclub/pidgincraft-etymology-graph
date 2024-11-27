#!/bin/bash

git submodule update --remote --merge &&
wget https://docs.google.com/spreadsheets/d/1_SCZqJMZ1UrwqbQ69Bxpf0JZVwz93x3tBZFf4DPrEDM/gviz/tq\?tqx\=out:csv\&sheet\=pidgincraft-vocab -O vocab.csv &&
python3 ./vocab.csv