dashboard:
	./dashboard.sh

check_services:
	./check_services.sh

run_backend:
	cd back/app && python3 app.py -p 0.0.0.0 --debug

start_mosquitto:
	sudo systemctl start mosquitto

restart_mosquitto:
	sudo systemctl restart mosquitto

listen_mosquitto:
	mosquitto_sub -t '#' -v
