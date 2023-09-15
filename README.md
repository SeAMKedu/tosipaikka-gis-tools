[![DOI](https://zenodo.org/badge/691898018.svg)](https://zenodo.org/badge/latestdoi/691898018)

![kuva](/images/tosipaikka_logot.png)

# TosiPaikka - GIS-työkalut

Kokoelma pieniä demosovelluksia paikkatiedon käsittelyyn ja visualisointiin.

## BlenderGIS

Blender-ohjelmalle on saatavilla ilmainen BlenderGIS-lisäosa, jolla voidaan ladata karttoja verkosta ja visualisoida paikkatietodataa. Tässä demomallissa Blenderiin tuodaan shapefile-tiedosto, joka sisältää GNSS-vastaanottimen vaaka- ja pystysuuntaisen paikannustarkkuuden kuljetulla reitillä. Paikannustarkkuudet visualisoidaan värillisinä pylväinä karttapohjan päällä.

Demomallin teossa käytetty Youtube-tutoriaali:

[https://www.youtube.com/watch?v=WviTi0q2BpA](https://www.youtube.com/watch?v=WviTi0q2BpA)

Blender ja BlenderGIS-lisäosa:

[https://www.blender.org/download/](https://www.blender.org/download/)

[https://github.com/domlysz/BlenderGIS](https://github.com/domlysz/BlenderGIS)

![kuva](/images/blender_gis_demo.png)

Karttanäkymää voidaan 
* lähentää ja loitontaa hiiren vierityspainikkeella
* kiertää painamalla vierityspainiketta ja liikuttamalla hiirtä
* liikuttaa painamalla vieritys- ja SHIFT-painiketta ja liikuttamalla hiirtä

Klikkaamalla *Scene Collection*-paneelissa vaakasuuntaisen (route_hacc) tai pystysuuntaisen (route_vacc) paikannustarkkuuden silmä-ikonia, kartan päällä olevat pylväät voidaan näyttää tai piilottaa.

![kuva](/images/blender_scene_collection.png)

Paikkatieto tuodaan Blender-ohjelmaan shp-tiedostona (shapefile), joka on avoin vektoripohjainen tiedostomuoto geospatiaalisen tiedon tallentamiseen paikkatietojärjestelmissä.

Alikansiossa on pieni Python-sovellus, joka lukee tekstitiedostosta sijaintidataa ja luo sitten datan perusteella seuraavat tiedostot:
* route.cpg (ESRI Cope Page File)
* route.dbf (dBase database file)
* route.prj (projektiotiedosto)
* route.shp (shapefile)
* route.shx (Autodesk AutoCAD:in kääntämä shapefile)

## Folium

Tämä demosovellus luo HTML-tiedoston, jossa visualisoidaan GNSS-vastaanottimen sijaintia lämpökartan avulla. 

Karttanäkymää voidaan lähentää ja loitontaa hiiren vierityspainikkeella tai kartan vasemmassa ylänurkassa olevilla painikkeilla.

![kuva](/images/folium_demo.png)

Sovellus lukee GNSS-vastaanottimen sijaintitiedot tekstitiedostosta. Visualisoinnissa hyödynnetään folium ja Leaflet.js kirjastoja.

[https://pypi.org/project/folium/](https://pypi.org/project/folium/)

[https://leafletjs.com/](https://leafletjs.com/)

## Geopandas

Tämä demosovellus luo HTML-tiedoston, jossa visualisoidaan bensiini- ja dieseljakeluasemien hintatietoja. Huomautus: hinnat ovat täysin kuvitteellisia.

![kuva](/images/geopandas_demo.png)

Sovellus hyödyntää geokoodausta eli prosessia, jossa osoite muutetaan paikkatiedoksi. Geopandas-kirjaston geocode-funktio käyttää *Nominatim*-palvelua, jolla on mahdollista hakea paikkatietoa OpenStreetMap:stä. Funktiolle annetaan lista osoitteista ja se palauttaa *geodataframe*-objektin.

```
geo = geocode(myAddressList, provider="nominatim", user_agent="demo", timeout=8)
```

Lisätietoja *Nominatim*-palvelusta:

[https://wiki.openstreetmap.org/wiki/Nominatim](https://wiki.openstreetmap.org/wiki/Nominatim)

Sovellus luo karttapohjan päälle jakeluasemia vastaavat markkerit, joita klikkaamalla avautuu asemalta saatavien polttoaineiden hintatiedot.

## Matplotlib

Sovelluksessa käytetään *matplotlib*-kirjastoa visualisoimaan GNSS-vastaanottimen paikannustarkkuutta karttapohjan päällä. Vaaka- ja pystysuuntainen paikannustarkkuus näytetään rinnakkain.

![kuva](/images/matplotlib_demo.png)

Sovellus käyttää *contextily*-kirjastoa kartan lataamiseen *OpenStreetMap*:stä. Kartta tallennetaan *tif*-tiedostona.

Muita käytettyjä kirjastoja ovat *geopandas*, *pyproj* ja *shapely*.

## Node-RED Worldmap

Demossa visualisoidaan auton kulkemaa reittiä Node-RED:in *worldmap*-lisäosan avulla.

[https://flows.nodered.org/node/node-red-contrib-web-worldmap](https://flows.nodered.org/node/node-red-contrib-web-worldmap)

![kuva](/images/worldmap_demo.png)

Kartta aukeaa verkkoselaimessa uuteen välilehteen, kun Node-RED:ssä painaa CTRL+SHIFT+m.

Python-sovellus lukee sijaintidataa tekstitiedostosta ja lähettää sijainnin Node-RED:ssä olevalle MQTT-palvelimelle, josta sijainti siirtyy kartalle.

![kuva](/images/node_red_demo.png)

## Tekijätiedot

Hannu Hakalahti, Asiantuntija TKI, Seinäjoen ammattikorkeakoulu

## Hanketiedot

* Hankkeen nimi: Tosiaikaisen paikkadatan hyödyntäminen teollisuudessa (TosiPaikka)
* Rahoittaja: Etelä-Pohjanmaan liitto (EAKR)
* Aikataulu: 01.12.2021 - 31.08.2023
* Hankkeen kotisivut: [https://projektit.seamk.fi/alykkaat-teknologiat/tosipaikka/](https://projektit.seamk.fi/alykkaat-teknologiat/tosipaikka/)
