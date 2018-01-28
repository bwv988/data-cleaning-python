# BASH alias.

alias psql="docker exec -it db psql -U postgres"
alias createdb="docker exec -it db createdb $@"
alias dropdb="docker exec -it db dropdb $@"
