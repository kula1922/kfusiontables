# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'

help:           ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
 
# Everything below is an example
install:		## Install kfusiontable
	pip3 install -e . -r requirements.txt

clean:          ## Remove cache files
	find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf;

test: clean     ## Run tests 
	kft_test test $(TEST_PATH)

migrate:        ## Migrate databases
	kft_app migrate