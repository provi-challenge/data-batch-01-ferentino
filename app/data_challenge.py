import requests
from sqlalchemy import create_engine
import re

connection_uri = "postgresql+psycopg2://{}:{}@{}:{}".format(
    'postgres',
    'postgres',
    'data-challenge-db',
    '5432'
)

engine = create_engine(connection_uri, pool_pre_ping=True)

#db = scoped_session(sessionmaker(bind=engine))
conn = engine.connect()

count_pokemons = requests.get('https://pokeapi.co/api/v2/pokemon/?offset=1').json()['count'] -1
count_abilities = requests.get('https://pokeapi.co/api/v2/ability/?offset=1').json()['count']-1
count_types = requests.get('https://pokeapi.co/api/v2/type/?offset=1').json()['count']-1


def loadAbilities(count):
    for i in range(1,count):
        try:
            resp = requests.get('https://pokeapi.co/api/v2/ability/'+ str(i)+'/?limit=200').json()  
            id = resp['id']
            name = resp['name']
            effect = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]','',(resp['effect_entries'][1]['effect']))
            query = "INSERT INTO db_abilities(id_ability, name, effect_entries) VALUES(%s,\'%s\', \'%s\') ON CONFLICT DO NOTHING;" % (id,name,effect)
            print(query)
            conn.execute(query)
        except:
            print("An exception occurred")
            pass

def loadTypes(count):
    for i in range(1,count):
        try:
            resp = requests.get('https://pokeapi.co/api/v2/type/'+ str(i)).json()   
            id = resp['id']
            name=resp['name']
            damage_relations = str(resp['damage_relations']).replace('\'','"')
            query = "INSERT INTO db_types(id_type, name, damage_relations) VALUES(%s,\'%s\', \'%s\') ON CONFLICT DO NOTHING;" % (id,name,damage_relations)
            print(query)
            conn.execute(query)
        except:
            print("An exception occurred")
            pass
        

def loadRelations(id_pokemon,id_item_relation,name_relation):
    print(name_relation)
    query = "INSERT INTO db_vinc_pokemon_%s (id_pokemon,id_%s) VALUES(%s,%s);" % (name_relation,name_relation,id_pokemon,id_item_relation)
    try:
        conn.execute(query)
    except:
        print("An exception occurred")
        pass

def loadPokemons(count):
    for i in range(1,count):
        try:
            resp = requests.get('https://pokeapi.co/api/v2/pokemon/'+ str(i)+'/?limit=200').json()   
            id_pokemon=resp['id']
            name=resp['name']
            base_experience=resp['base_experience']
            weight=resp['weight']
            height=resp['height']
            is_default=resp['is_default']
        #'order':[resp['order']]
        
            query = "INSERT INTO db_pokemons (id_pokemon, name, base_experience, weight, height, is_default) VALUES(%s, \'%s\', %s, %s, %s, %s) ON CONFLICT DO NOTHING;" % (id_pokemon,name,base_experience,weight,height,is_default)
            print(query)
            conn.execute(query)
        except:
            print("An exception occurred")
            pass
        
        for ability in resp['abilities']:
            loadRelations(
                resp['id'],
                (ability['ability']['url'].split('/')[-2]) ,
                'ability'
            )     
        
        for type in resp['types']:
            loadRelations(
                resp['id'],
                (type['type']['url'].split('/')[-2]),
                'type'
            )   
    
loadAbilities(100)
loadPokemons(30)
loadTypes(19)
