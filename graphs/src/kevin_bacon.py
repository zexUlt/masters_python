import json
from os import path
import networkx as nx
import itertools

class KevinBacon():
    __KEVIN__ = 'Kevin Bacon'

    def constructGraph(self, path_to_json: str) -> None:
        with open(path_to_json, mode='r') as json_descr:
            self.actors_dict = json.load(json_descr)

        new_dict = dict()
        for item in self.actors_dict:
            new_dict[item['name']] = item['films']
        self.actors_dict = new_dict
        
        for k, v in self.actors_dict.items():
            title_year = list()
            for item in v:
                title_year.append((item['title'], item['year']))
            self.actors_dict[k] = title_year
        
        self.G = nx.Graph()
        self.G.add_nodes_from(self.actors_dict.keys())
        film_actors = dict()
        for actor in self.actors_dict:
            for film in self.actors_dict[actor]:
                if film in film_actors.keys():
                    film_actors[film].append(actor)
                else:
                    film_actors[film] = [actor]
        
        for film in film_actors:
            for actor_pair in itertools.combinations(film_actors[film], 2):
                self.G.add_edge(actor_pair[0], actor_pair[1], name=film)

    def calculateKBNumber(self, source=None, target='Kevin Bacon') -> dict:
        paths = nx.shortest_path(self.G, source=source, target=target)
        if self.__KEVIN__ in paths:
            del paths[self.__KEVIN__]
        return paths
    
    def getFilmByActors(self, actor_1: str, actor_2: str) -> dict:
        return self.G.get_edge_data(actor_1, actor_2)['name']
