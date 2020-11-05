from recipe_scrapers import scrape_me

scraper = scrape_me('https://cookpad.com/uk/recipes/13777213-andhra-chicken-pulao?via=search&search_term=Andhra%20Chicken%20Pulao')

#print('- ' + scraper.instructions().replace('\n', '\n- '))
print(scraper.instructions())
