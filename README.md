# Ravintolasovellus
Sovelluksessa näkyy tietyn alueen ravintolat, joista voi etsiä tietoa ja lukea arvioita. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

Sovelluksen ominaisuuksia ovat:
1. Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
2. Käyttäjä näkee ravintolat kartalla ja voi painaa ravintolasta, jolloin siitä näytetään lisää tietoa (kuten kuvaus ja aukioloajat).
3. Käyttäjä voi antaa arvion (tähdet ja kommentti) ravintolasta ja lukea muiden antamia arvioita.
4. Ylläpitäjä voi lisätä ja poistaa ravintoloita sekä määrittää ravintolasta näytettävät tiedot.
5. Käyttäjä voi etsiä kaikki ravintolat, joiden kuvauksessa on annettu sana.
6. Käyttäjä näkee myös listan, jossa ravintolat on järjestetty parhaimmasta huonoimpaan arvioiden mukaisesti.
7. Ylläpitäjä voi tarvittaessa poistaa käyttäjän antaman arvion.
8. Ylläpitäjä voi luoda ryhmiä, joihin ravintoloita voi luokitella. Ravintola voi kuulua yhteen tai useampaan ryhmään.

**Päivitys 2.6.2024:** Käyttäjärekisteröinti ja kirjautuminen valmis. Käyttäjät voivat tarkastella alueen ravintoloita kartalta. Käyttäjät voivat tarkastella muiden ihmisten kommentteja ja lähettää kommentteja itse.

**Päivitys 16.6.2024:** Käyttäjät ja ylläpitäjät luokitellaan rekisteröintivaiheen aikana. Toteutetut järjestelmänvalvojan oikeudet: lisätä, poistaa tai muokata ravintoloita informatioita. Poistaa kommenttia. Ajanpuutteesta johtuen olen jo kirjoittanut koodin ravintoloiden luokitteluun, mutta pieniä bugeja on vielä korjaamatta, joten ravintoloiden luokittelutoimintoa ei ole vielä toteutettu.

* Seuraavaksi täydentelen ravintoloiden luokittelua. Järjestelmänvalvojat voivat myös hallita luokkia. Lisäksi käyttäjät näkevät myös ravintolat luokitusten perusteella. Kun kaikki toiminnot on toteutettu, keskityn käyttökokemuksen parantamiseen, kuten sivun kaunistamiseen, ulkoasun lisäämiseen ja siihen, että toiminta ei ole enää yksisäikeistä. Lisäksi minun on myös selvitettävä, onko koodissa haavoittuvuusongelmia.

# SOLVELLUKSEN TESTAAMINEN
Sovellusta ei ole testattavissa Fly.iossa. Käynnistään sovelluksen paikallisesti.Kloonaa tämä repositorio koneellesi ja siirry sen juurikansioon. Aktivoi virtuaaliympäristö komennoilla
```python
$ cd <file>
$ python3 -m venv venv  
$ source venv/bin/activate
```
Asenna riippuvuudet komennolla
```python
(venv) $ pip install -r requirements.txt
```

Luo Postgresiin uusi tietokanta komennoilla ja Määritä sitten tietokannan skeema komennolla
```python
$ psql  
user=# CREATE DATABASE <tietokannan_nimi>;
$ psql -d <tietokannan_nimi> < schema.sql
```

Määritä siellä salainen avaimesi ja tietokannan osoite ja muistaa luodaan sovelluksen juurikansiossa vielä .env -tiedosto
```python
DATABASE_URL=postgresql:///<tietokannan_nimi> 
SECRET_KEY=<salainen avaimesi>
```

Nyt voit testaa sovellusta komennolla
```python
flask run
```