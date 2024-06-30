# Ravintolasovellus
Sovelluksessa näkyy tietyn alueen ravintolat, joista voi etsiä tietoa ja lukea arvioita. Sovelluksessa on myös reaaliaikaista ravintolatarjouksia.


Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä：
1. Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
2. Käyttäjä näkee ravintolat kartalla ja voi painaa ravintolasta, jolloin siitä näytetään lisää tietoa (kuten kuvaus ja aukioloajat).
3. Käyttäjä voi antaa arvion (tähdet ja kommentti) ravintolasta ja lukea muiden antamia arvioita.
4. Käyttäjät voivat etsiä ravintoloita etsimällä heidän nimiään.
5. Ylläpitäjä voi lisätä ja poistaa ravintoloita sekä määrittää ravintolasta näytettävät tiedot.
6. Ylläpitäjä voi tarvittaessa poistaa käyttäjän antaman arvion.
7. Ylläpitäjä voi luoda ryhmiä, joihin ravintoloita voi luokitella. Ravintola voi kuulua yhteen tai useampaan ryhmään.
8. Ylläpitäjät voivat hallita ravintolan tarjouksia.

# SOLVELLUKSEN TESTAAMINEN
Sovellusta ei ole testattavissa Fly.iossa. Käynnistään sovelluksen paikallisesti. Kloonaa tämä repositorio koneellesi ja siirry sen kansioon. Aktivoi virtuaaliympäristö komennoilla
```python
$ cd <file>
$ python3 -m venv venv  
$ source venv/bin/activate
```
Asenna riippuvuudet komennolla
```python
(venv) $ pip install -r requirements.txt
```

Luo Postgresiin uusi tietokanta ja määritä sitten tietokannan komennolla
```python
$ psql  
user=# CREATE DATABASE <tietokannan_nimi>;
$ psql -d <tietokannan_nimi> < schema.sql
```

Määritä salainen avaimesi ja tietokannan osoite. Luo sovelluksen kansiossa .env -tiedosto
```python
DATABASE_URL=postgresql:///<tietokannan_nimi> 
SECRET_KEY=<salainen avaimesi>
```

Nyt voit testaa sovellusta komennolla
```python
flask run
```