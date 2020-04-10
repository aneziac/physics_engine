init:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

lint:
	flake8 --max-line-length=160 --ignore=E402

clear_event_logs:
	rm -rf logs/event_logs
	mkdir logs/event_logs
