#!/bin/bash

alias az="docker run --rm -v $(pwd):/root azuresdk/azure-cli-python az $@"
alias azssh="docker run --rm -it -v $(pwd):/root azuresdk/azure-cli-python ssh $@"
