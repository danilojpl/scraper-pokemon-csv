import scrapy
import json 

class PokemonScrapper(scrapy.Spider):
  name = 'pokemon_scrapper'
  domain = 'https://bulbapedia.bulbagarden.net'
  start_urls = ['https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number']
  

  def parse (self, response):
    pokemons = colecoes = response.css('tr')
    for pokemon in pokemons:
     pokemon_url = pokemon.css('td>a::attr(href)').get()
     if pokemon_url is not None:
      yield response.follow(self.domain + pokemon_url, self.parse_pokemon)
  
  def parse_pokemon(self, response):
    yield {'pokemon_numero': response.xpath("*//tbody/tr[1]/th/big/big/a/span/text()").re_first(r'#+(\w+)')
        ,'pokemon_nome': response.xpath("*//table/tbody/tr/td[1]/big/big/b/text()").get()
        ,'pokemon_altura': ''.join(s.strip('/[]|\n\"') for s in response.xpath("*//div/table[2]/tbody/tr[6]/td[1]/table/tbody/tr[1]/td/text()").getall()).replace('\\',' ')
        ,'pokemon_peso': ''.join(s.strip() for s in response.xpath("*//div/table[2]/tbody/tr[6]/td[2]/table/tbody/tr[1]/td/text()").getall())
        ,'pokemon_cor_pokedex': ''.join(s.strip() for s in response.xpath("*//tr[11]/td[1]/table/tbody/tr/td/text()").get())}
  

