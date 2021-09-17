from typing import Text
import scrapy
import json 

class PokemonScrapper2(scrapy.Spider):
  name = 'pokemon_scrapper2'
  domain = 'https://www.serebii.net'
  start_urls = ['https://www.serebii.net/pokedex-swsh']
  

  def parse (self, response):
    pokemons = colecoes = response.css('option')
    for pokemon in pokemons:
      pokemon_url = pokemon.css("::attr(value)").get()
      if pokemon_url is not None: 
        yield response.follow(self.domain + pokemon_url, self.parse_pokemon) 
  
  def parse_pokemon(self, response):
    yield {'pokemon_numero': response.css("td:nth-child(1) table tr td:nth-child(2) h1::text").re_first(r'#+(\w*)\s')
          ,'pokemon_nome': response.css("td:nth-child(1) table tr td:nth-child(2) h1::text").re_first(r'\s+(\w+).*\s*(\w*)')
          ,'pokemon_evolucao': response.css("table tr td.pkmn a>img ::attr(alt)").getall() or response.css("table tr td.pkmn a::attr(href)").re(r'swsh\/(\w*)')
          ,'pokemon_tipo_dano': response.css("tr:nth-child(2) td>a>img::attr(alt)").re(r'Type:\s*(\w*)-')
          ,'pokemon_dano': response.css("table tr:nth-child(3) td.footype::text").getall()
          ,'pokemon_tipo': response.css("tr:nth-child(2) td.cen a>img::attr(alt)").re(r'\s*(\w*)-')}