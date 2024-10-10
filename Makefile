test:
	poetry run pytest

start_db:
	brew services start mongodb-community
	brew services start redis

clean_redis:
	redis-cli FLUSHALL

stop_db:
	brew services stop mongodb-community
	brew services stop redis
