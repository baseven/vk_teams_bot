start_db:
	brew services start mongodb-community@7.0
	brew services start redis

clean_redis:
	redis-cli FLUSHALL

stop_db:
	brew services stop mongodb-community@7.0
	brew services stop redis
