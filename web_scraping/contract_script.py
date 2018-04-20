'''
This script is designed to scrape relevant contract information given a player's
name:
	- Contract length
	- Contract total value
	- Contract value per year (list)

'''

import urllib2
from bs4 import BeautifulSoup


# ------- Functions ------------------------------------------------------------

# Given a player's first and last names, the expression needed to generate the
# URL for that player is created - consisting of a player's first 5 characters  
# of his last name combined with the first 2 characters of his first name
def gen_player_exp(first_name, last_name):

	# Get a string of the first 5 characters of player's last name
	last_name_s = last_name.lower()

	# Get a string of the first 2 characters of player's first name
	first_name_s = first_name.lower()

	# Return the expression 
	return first_name_s + '-' + last_name_s



# This function takes as input a player's name, and uses it to generate the URL
# to that player's page on Basektball Reference
def get_url(player_name):

	# Split player's name into first and last
	player_names_list = player_name.replace('.','').split()
	first_name = player_names_list[0]
	last_name = player_names_list[1]

	# Generate the expression needed to create the URL (1st 5 of last name + 
	#	1st 2 of first name)
	exp = gen_player_exp(first_name, last_name)

	# Create the URL based on the expression
	url = 'http://hoopshype.com/player/' + exp + '/salary/'

	return url


def parse_website(contract_url):
	# Query the website and create the BeautifulSoup object
	site_query = urllib2.urlopen(contract_url)
	soup = BeautifulSoup(site_query)

	# Find the specific table we wish to parse from, defined by its class name
	contract_table = soup.find('div', class_="player-bio-text")

	# Get the 2017-18 contract monetary value
	contract_17_18 = contract_table.findAll("span")[-1]
	
	# Strip the tabs, dollar sign, and commas, and then return the value of the 
	# contract as an integer
	return int(contract_17_18.text.strip().strip('$').replace(',',''))
		


# ------- Main Code ------------------------------------------------------------

def main(): 
	sample_player_name = 'Kevin Durant'

	contract_url = get_url(sample_player_name)

	this_season_value = parse_website(contract_url)

	print this_season_value


if __name__ == '__main__':
	main()