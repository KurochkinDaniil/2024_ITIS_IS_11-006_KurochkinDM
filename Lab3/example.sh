#!/bin/bash

commands=(
    'python search.py "джедаи|меч|татуин"'
    'python search.py "джедаи&татуин|меч"'
    'python search.py "джедаи И меч И татуин"'
    'python search.py "джедаи & !меч | !татуин"'
    'python search.py "джедаи | !меч | !татуин"'
)

for cmd in "${commands[@]}"; do
  echo "Выполнение: $cmd"
  $cmd
  echo "Команда выполнена"
done
