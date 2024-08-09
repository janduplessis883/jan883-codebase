install:
	@pip install -e .
	@echo "🌵 pip install -e . completed!"

clean:
	@rm -f */version.txt
	@rm -f .DS_Store
	@rm -f .coverage
	@rm -rf */.ipynb_checkpoints
	@rm -Rf build
	@rm -Rf */__pycache__
	@rm -Rf */*.pyc
	@rm -f .cache.sqlite
	@echo "🧽 Cleaned up successfully!"

all: install clean

icloud:
	@python automation/icloud_email.py

weather:
	@python automation/weather_forcast.py

image_renamer:
	@python automation/image_renamer.py

browser:
	@python automation/browser_shortcut.py

scheduler:
	@python automation/automation_scheduler.py

git_merge:
	$(MAKE) clean
	@python git_automation/git_merge.py
	@echo "👍 Git Merge (master) successfull!"

git_push:
	$(MAKE) clean
	@python git_automation/git_push.py
	@echo "👍 Git Push (branch) successfull!"

test:
	@pytest -v tests

# Specify package name
lint:
	@black --check .
