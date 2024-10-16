# Auto-mate
Auto-mate is a Discord moderation bot created with the Discord.py library.

## Quick-start

```bash
## Clone the Repository
git clone https://github.com/CallumB04/Auto-mate.git

## Update working directory
cd ./Auto-mate

## Prepare docker-compose file
cp ./docker-compose.yml.example ./docker-compose.yml

## Open docker-compose.yml in your editor of choice and update environment variables accordingly
vim docker-compose.yml

## Deploy auto-mate
docker compose up -d
```

## Configuration
- Bot configuration files can be found in the `./data` directory.
- Token can be set using the `TOKEN` environment variable.