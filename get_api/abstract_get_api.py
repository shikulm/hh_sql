from abc import ABC, abstractmethod

class AbstractGetApi(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass


    @abstractmethod
    def get_employer(self):
        pass