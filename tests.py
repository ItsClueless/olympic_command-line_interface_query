from input_parser import InputParser, CommandNotFoundError
from database import Database
import unittest

class InputParserTestCase(unittest.TestCase):
    def test_parse_input(self):
        assert InputParser().parse_input("list") == ["list"], "Should return ['list']"
        assert InputParser().parse_input("count medals Uganda") == ["count", "medals", "uganda"], "Should return ['count', 'medals', 'uganda']"
        assert InputParser().parse_input("list athletes 'Czech Republic'") == ["list", "athletes", "czech republic"], f"Should return ['list', 'athletes', 'czech republic']"
        self.assertRaises(CommandNotFoundError, InputParser().parse_input, "bad command"), "Should raise CommandNotFoundError"


class DatabaseTestCase(unittest.TestCase):
    def test_load_data(self):
        database = Database()
        database.load_data()
    def test_select_query(self):
        assert Database.select_query(self,["fldPopulation"],True,["pmkCountrycode"],['United States']), "Should return [SELECT fldPopulation FROM tblCountries WHERE pmkCountryCode = “United States”]"
        assert Database.select_query(self, ['fldCountryName'], False, ['NA'],["NA"]), "Should return [SELECT fldCountryName FROM tblCountries]"
        assert Database.select_query(self, ['fldEvent'], True, ['fldName'], ['Marilyn Agliotti']), "Should return [SELECT fldEvent FROM tblOlympicAthletes WHERE fldName = 'Marilyn Agliotti']"
    def test_column_query(self):
        assert Database.columns_query(self, 'countries'), "Should return ['code', 'country', 'gold', 'silver', 'bronze', 'total', 'population']"
        assert Database.columns_query(self, 'athletes'), "Should return ['id', 'athlete', 'sex', 'age', 'height', 'weight', 'nationality', 'year', 'city', 'sport', 'event']]"
    def test_min_max_query(self):
        assert Database.min_max_query(self,['fldCountryName'], True,'fldNumGoldMedals'), "Should return [SELECT fldCountryName FROM tblCountries JOIN (SELECT MAX(fldNumGoldMedals) AS most  FROM tblCountries) tblCountries ON fldNumGoldMedals most = fldNumGoldMedals]"
        assert Database.min_max_query(self,['fldCountryName'], False,'fldNumBronzeMedals'), "Should return [SELECT fldCountryName FROM tblCountries JOIN (SELECT MIN(fldNumGoldMedals) AS least  FROM tblCountries) tblCountries ON fldNumGoldMedals least = fldNumGoldMedals]"
    def test_inner_join_query(self):
        assert Database.inner_join_query(self, ['fldCountryName'], 'tblCountries', 'tblOlympicAthletes', 'pmkCountryCode', 'fpkNationality', True, ['fldName'], ['Marilyn Agliotti'] ), "Should return [SELECT fldCountryName FROM tblCountries INNER JOIN tblOlympicAthletes ON tblCountries.pmkCountryCode = tblOlympicAthletes.fpkNationality WHERE tblOlympicAthletes.fldName = 'Marilyn Agliotti']"
    def test_submit_query(self):
        assert Database.submit_query(self, "SELECT fldCountryName FROM tblCountries INNER JOIN tblOlympicAthletes ON tblCountries.pmkCountryCode = tblOlympicAthletes.fpkNationality WHERE tblOlympicAthletes.fldName = 'Marilyn Agliotti'"), "Should return ['Netherlands']"
        assert Database.submit_query(self, "SELECT fldEvent FROM tblOlympicAthletes WHERE fldName = 'Marilyn Agliotti'"), "Should return [Hockey Women's Hockey\n]"
        

if __name__ == "__main__":
    unittest.main()