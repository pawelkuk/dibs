.PHONY: initial_data pgadmin reset_db clean
initial_data:
	docker-compose exec app sh -c "python /src/api/manage.py initial_data"
	docker-compose restart read_model
pgadmin:
	docker-compose exec pgadmin sh -c "/venv/bin/python3.9 /pgadmin4/setup.py --load-servers /pgadmin/server.json --user admin@admin.com"
reset_db:
	docker-compose down
	rm -rf ./volumes/postgres*
	docker-compose up -d
clean:
	rm ./experiments/*.csv