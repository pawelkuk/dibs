.PHONY: initial_data pgadmin
initial_data:
	docker-compose exec app sh -c "python /src/api/manage.py initial_data"
pgadmin:
	docker-compose exec pgadmin sh -c "/venv/bin/python3.9 /pgadmin4/setup.py --load-servers /pgadmin/server.json --user admin@admin.com"
connect:
	./scripts/connect.sh