from bs4 import BeautifulSoup
import bs4
import lxml
import feedparser
# from textblob_de import TextBlobDE as TextBlob
from pandas.core.common import flatten
import pandas as pd
from datetime import date
from datetime import datetime
import statistics
# import openpyxl
# from openpyxl import load_workbook
from flashtext import KeywordProcessor
import asyncio
import httpx
#import time
#import itertools
# import cchardet
# import gevent
import os
from bs4 import SoupStrainer
import psycopg2
import os
import urllib.parse as urlparse
import spacy
from spacy_sentiws import spaCySentiWS
import numpy as np


url = urlparse.urlparse(os.environ['DATABASE_URL'])
dbname = url.path[1:]
user = url.username

password = url.password
host = url.hostname
port = url.port

con = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
            )
dbCursor = con.cursor()
#print(dbname)

sqlCreateTable  = 'CREATE TABLE IF NOT EXISTS crawldata(date varchar(128), sentimentcdu numeric, sentimentgruene numeric, sentimentspd numeric, sentimentfdp numeric, sentimentafd numeric, linkscdu text,linksgruene text,linksspd text,linksfdp text,linksafd text);'
# sqlAddColumns = 'ALTER TABLE crawldata ADD COLUMN IF NOT EXISTS linkscdu varchar(2048),ADD COLUMN IF NOT EXISTS linksgruene varchar(2048),ADD COLUMN IF NOT EXISTS linksspd varchar(2048),ADD COLUMN IF NOT EXISTS linksfdp varchar(2048),ADD COLUMN IF NOT EXISTS linksafd varchar(2048)'
# sqlaltercolumns= 'ALTER TABLE crawldata ALTER COLUMN linkscdu TYPE varchar(2048),ALTER COLUMN linksgruene TYPE varchar(2048),ALTER COLUMN linksspd TYPE varchar(2048),ALTER COLUMN linksfdp TYPE varchar(2048),ALTER COLUMN linksafd TYPE varchar(2048)'
#sqlCreateTable  = 'CREATE TABLE crawldata(date,sentimentcdu,sentimentgruene,sentimentspd,sentimentfdp,sentimentafd);'
dbCursor.execute(sqlCreateTable);
# dbCursor.execute(sqlAddColumns);
# dbCursor.execute(sqlaltercolumns);




rss_urls=['https://www.spiegel.de/politik/index.rss','https://www.tagesschau.de/xml/rss2/','https://www.n-tv.de/politik/rss','https://rss.sueddeutsche.de/rss/Politik','https://www.faz.net/rss/aktuell/politik/']
content_cdu = []
content_gruene= []
content_fdp = []
content_spd = []
content_afd = []
links_cdu=[]
links_gruene=[]
links_fdp=[]
links_spd=[]
links_afd=[]
weight_cdu=[]
weight_gruene=[]
weight_fdp=[]
weight_spd=[]
weight_afd=[]
content= []

links = []
linklist=[]
tagesschau_links= []
ntv_links = []
sueddeutsche_links = []
# HTTP GET requests
h = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko)     Chrome/23.0.1271.64 Safari/537.11'}


whitelist = [
    'p'
    # 'article__text',
    # 'article-body',
    # 'content'
]
async def get_content(index: int, url: str) -> str:
    async with httpx.AsyncClient(timeout=None) as client:
        try:
            if ".faz.net" in url:
                url+="?printPagedArticle=true"
                response = await client.get(url)
                #print(url)
            else:
                response = await client.get(url)
            #print(url)
        except:
            print(f'Error response while requesting.')
            response ="0"
        #soup = bs4.BeautifulSoup(response.text, 'lxml', parse_only = SoupStrainer('p'))
        content.append((url,[t for t in bs4.BeautifulSoup(response.text, 'lxml',parse_only = SoupStrainer('p')).find_all(text=True) if t.parent.name in whitelist]))

        #del soup

async def main():
    print('##############run#######################')

    keyword_fdp = [
    'Grigorios Aggelidis',
    'Renata Alt',
    'Christine Aschenberg-Dugnus',
    'Nicole Bauer',
    'Jens Beeck',
    'Jens Brandenburg',
    'Mario Brandenburg',
    'Sandra Bubendorfer-Licht',
    'Marco Buschmann',
    'Karlheinz Busen',
    'Carl-Julius Cronenberg',
    'Britta Katharina Dassler',
    'Bijan Djir-Sarai',
    'Christian D??rr',
    'Hartmut Ebbing',
    'Marcus Faber',
    'Daniel F??st',
    'Otto Fricke',
    'Christopher Gohl',
    'Alexander Graf Lambsdorff',
    'Thomas Hacker',
    'Reginald Hanke',
    'Peter Heidt',
    'Katrin Helling-Plahr',
    'Markus Herbrand',
    'Torsten Herbst',
    'Katja Hessel',
    'Gero Hocker',
    'Manuel H??ferlin',
    'Christoph Hoffmann',
    'Reinhard Houben',
    'Ulla Ihnen',
    'Olaf in der Beek',
    'Gyde Jensen',
    'Karsten Klein',
    'Marcel Klinge',
    'Daniela Kluckert',
    'Pascal Kober',
    'Lukas K??hler',
    'Carina Konrad',
    'Wolfgang Kubicki',
    'Konstantin Kuhle',
    'Alexander Kulitz',
    'Ulrich Lechte',
    'Christian Lindner',
    'Michael Link',
    'Oliver Luksic',
    'Till Mansmann',
    'J??rgen Martens',
    'Christoph Meyer',
    'Alexander M??ller',
    'Roman M??ller-B??hm',
    'Frank M??ller-Rosentritt',
    'Martin Neumann',
    'Matthias N??lke',
    'Hagen Reinhold',
    'Bernd Reuther',
    'Thomas Sattelberger',
    'Christian Sauter',
    'Frank Sch??ffler',
    'Wieland Schinnenburg',
    'Matthias Seestern-Pauly',
    'Frank Sitta',
    'Judith Skudelny',
    'Hermann Otto Solms',
    'Bettina Stark-Watzinger',
    'Marie-Agnes Strack-Zimmermann',
    'Benjamin Strasser',
    'Katja Suding',
    'Linda Teuteberg',
    'Michael Theurer',
    'Stephan Thomae',
    'Manfred Todtenhausen',
    'Florian Toncar',
    'Andrew Ullmann',
    'Gerald Ullrich',
    'Johannes Vogel',
    'Sandra Weeser',
    'Nicole Westig',
    'Katharina Willkomm',
    'Volker Wissing',
    'FDP',
    'Freie Demokratische Partei',
    'FDP-',
    '(FDP)',
    ]

    keyword_cdu = [
        'CDU',
        'CSU',
        'CDU/CSU',
        '(CDU)',
        '(CSU)',
        'Union',
        'Christlich Demokratische Union',
        'Michael von Abercron',
        'Stephan Albani',
        'Norbert Altenkamp',
        'Peter Altmaier',
        'Philipp Amthor',
        'Peter Aumer',
        'Artur Auernhammer',
        'Dorothee B??r',
        'Thomas Barei??',
        'Norbert Barthle',
        'Maik Beermann',
        'Manfred Behrens',
        'Andr?? Berghegger',
        'Veronika Bellmann',
        'Sybille Benning',
        'Melanie Bernstein',
        'Marc Biadacz',
        'Christoph Bernstiel',
        'Peter Beyer',
        'Steffen Bilger',
        'Michael Brand',
        'Peter Bleser',
        'Norbert Brackmann',
        'Silvia Breher',
        'Sebastian Brehm',
        'Reinhard Brandl',
        'Helge Braun',
        'Heike Brehmer',
        'Carsten Brodesser',
        'Ralph Brinkhaus',
        'Gitta Connemann',
        'Astrid Damerow',
        'Alexander Dobrindt',
        'Michael Donth',
        'Marie-Luise D??tt',
        'Hansj??rg Durz',
        'Thomas Erndl',
        'Bernd Fabritius',
        'Hermann F??rber',
        'Uwe Feiler',
        'Enak Ferlemann',
        'Maria Flachsbarth',
        'Hans-Peter Friedrich',
        'Thorsten Frei',
        'Maika Friemnann-Jennert',
        'Michael Frieser',
        'Hans-Joachim Fuchtel',
        'Ingo G??dchens',
        'Thomas Gebhart',
        'Alois Gerig',
        'Eberhard Gienger',
        'Eckhard Gnodkte',
        'Hermann Gr??he',
        'Ursula Groden-Kranich',
        'Klaus-Dieter Gr??hler',
        'Michael Grosse-Br??mer',
        'Manfred Grund',
        'Astrid Grotel??schen',
        'Markus Gr??bel',
        'Oliver Grundmann',
        'Olav Gutting',
        'Monika Gr??tters',
        'Fritz G??ntzler',
        'Christian Haase',
        'Florian Hahn',
        'J??rgen Hardt',
        'Matthias Hauer',
        'Matthias Heider',
        'Frank Heinrich',
        'Mechtild Heil',
        'Thomas Heilmann',
        'Mark Helfrich',
        'Marc Henrichmann',
        'Rudolf Henke',
        'Michael Hennrich',
        'Ansgar Heveling',
        'Alexander Hoffmann',
        'Christian Hirte',
        'Heribert Hirte',
        'Hendrik Hoppenstedt',
        'Karl Holmeier',
        'Erich Irlstorfer',
        'Hans-J??rgen Irmer',
        'Thomas Jarzombek',
        'Andreas Jung',
        'Ingmar Jung',
        'Alois Karl',
        'Anja Karliczek',
        'Torbj??rn Kartes',
        'Volker Kauder',
        'Dr. Stefan Kaufmann',
        'Michael Kie??ling',
        'Ronja Kemmer',
        'Roderich Kiesewetter',
        'Georg Kippels',
        'Jens Koeppen',
        'Volkmar Klein',
        'Axel Knoerig',
        'Markus Koob',
        'Alexander Krau??',
        'Carsten K??ber',
        'Kordula Kovac',
        'Gunter Krichbaum',
        'Michael Kuffer',
        'G??nter Krings',
        'R??diger Kruse',
        'Roy K??hne',
        'Karl A. Lamers',
        'Andreas G. L??mmel',
        'Katharina Landgraf',
        'Ulrich Lange',
        'Silke Launert',
        'Paul Lehrieder',
        'Jens Lehmann',
        'Katja Leikert',
        'Andreas Lenz',
        'Andrea Lindholz',
        'Antje Lezius',
        'Carsten Linnemann',
        'Bernhard Loos',
        'Jan-Marco Luczak',
        'Saskia Ludwig',
        'Daniela Ludwig',
        'Yvonne Magwas',
        'Thomas de Maizi??re',
        'Gisela Manderla',
        'Astrid Mannes',
        'Hans-Georg von der Marwitz',
        'Andreas Mattfeldt',
        'Matern von Marschall',
        'Stephan Mayer',
        'Angela Merkel',
        'Jan Metzler',
        'Michael Meister',
        'Hans Michelbach',
        'Dietrich Monstadt',
        'Matthias Middleberg',
        'Karsten M??ring',
        'Elisabeth Motschmann',
        'Axel M??ller',
        'Carsten M??ller',
        'Sepp M??ller',
        'Stefan M??ller',
        'Christian Natterer',
        'Andreas Nick',
        'Petra Nicolaisen',
        'Michaela Noll',
        'Kristina Nordt',
        'Wilfried Oellers',
        'Florian O??ner',
        'Josef Oster',
        'Tim Ostermann',
        'Henning Otte',
        'Ingrid Pahlmann',
        'Sylvia Pantel',
        'Martin Patzelt',
        'Joachim Pfeiffer',
        'Stephan Pilsinger',
        'Eckhard Pols',
        'Christoph Plo??',
        'Thomas Rachel',
        'Kerstin Radomski',
        'Alexander Radwan',
        'Alois Rainer',
        'Eckhardt Rehberg',
        'Lothar Riebsamen',
        'Peter Ramsauer',
        'Josef Rief',
        'Erwin R??ddel',
        'Norbert R??ttgen',
        'Johannes R??ring',
        'Stefan Rouenhoff',
        'Albert Rupprecht',
        'Stefan Sauer',
        'Anita Sch??fer',
        'Wolfgang Sch??uble',
        'Andreas Scheuer',
        'Jana Schmike',
        'Christian Schmidt',
        'Tankred Schipanski',
        'Claudia Schmidtke',
        'Patrick Schnieder',
        'Felix Schreiner',
        'Nadine Sch??n',
        'Klaus-Peter Schulze',
        'Uwe Schummer',
        'Torsten Schweiger',
        'Johannes Selle',
        'Detlef Seif',
        'Reinhold Sendker',
        'Patrick Sensburg',
        'Thomas Silberhorn',
        'Bernd Siebert',
        'Bj??rn Simon',
        'Jens Spahn',
        'Katrin Staffler',
        'Tino Sorge',
        'Frank Steffel',
        'Andreas Steier',
        'Albert Stegemann',
        'Wolfgang Stefinger',
        'Peter Stein',
        'Johannes Steiniger',
        'Christian Frhr. von Stetten',
        'Sebastian Steineke',
        'Dieter Stier',
        'Stephan Stracke',
        'Max Straubinger',
        'Gero Storjohann',
        'Hermann-Josef Tebroke',
        'Hans-J??rgen Thies',
        'Alexander Throm',
        'Dietlind Tiemann',
        'Antje Tillmann',
        'Markus Uhl',
        'Volker Ullreich',
        'Arnold Vaatz',
        'Kerstin Vieregge',
        'Thomas Viesehon',
        'Volkmar Vogel',
        'Kees de Vries',
        'Johann David Wadephul',
        'Marco Wanderwitz',
        'Nina Warken',
        'Kai Wegner',
        'Marcus Weinberg',
        'Anja Weisberger',
        'Albert H. Weiler',
        'Peter Wei??',
        'Ingo Wellenreuther',
        'Kai Whittaker',
        'Sabine Weiss',
        'Marian Wendt',
        'Bettina Margarethe Wiesmann',
        'Elisabeth Winkelmeier-Becker',
        'Anette Widmann-Mauz',
        'Klaus-Peter Willsch',
        'Christoph de Vries',
        'Emmi Zeulner',
        'Paul Ziemiak',
        'Matthias Zimmer',
        'Armin Laschet',
        'Laschet',
        'Markus S??der',
        'Annegret Kramp-Karrenbauer',
        'Ursula von der Leyen',
        'Horst Seehofer',
        'CDU-',
        'CSU-',
        'CDU/CSU-',
        'Unionskanzlerkandidat',
        '(CDU)',
        ]

    keyword_gruene = ['Luise Amtsberg',
        'Lisa Badum','Annalena Baerbock','Margarete Bause','Canan Bayram','Franziska Brantner','Agnieszka Brugger',
        'Anna Christmann','Janosch Dahmen','Ekin Delig??z','Katharina Dr??ge','Harald Ebner','Marcel Emmerich','Matthias Gastel','Kai Gehring','Stefan Gelbhaar'
        'Katrin G??ring-Eckardt','Erhard Grundl','Anja Hajduk','Britta Ha??elmann','Bettina Hoffmann','Anton Hofreiter','Ottmar von Holtz'
        'Dieter Janecek','Kirsten Kappert-Gonther','Uwe Kekeritz','Katja Keul','Sven-Christian Kindler','Maria Klein-Schmeink','Sylvia Kotting-Uhl'
        'Oliver Krischer','Christian K??hn','Renate K??nast','Markus Kurth','Monika Lazar','Sven Lehmann','Steffi Lemke','Tobias Lindner'
        'Irene Mihalic','Claudia M??ller','Beate M??ller-Gemmeke','Ingrid Nestle','Konstantin von Notz','Omid Nouripour','Friedrich Ostendorff'
        'Cem ??zdemir','Lisa Paus','Filiz Polat','Tabea R????ner','Claudia Roth','Manuela Rottmann','Corinna R??ffer','Manuel Sarrazin','Ulle Schauws','Frithjof Schmidt'
        'Stefan Schmidt','Charlotte Schneidewind-Hartnagel','Kordula Schulz-Asche','Wolfgang Strengmann-Kuhn','Margit Stumpp','Markus Tressel','J??rgen Trittin'
        'Julia Verlinden','Daniela Wagner','Beate Walter-Rosenheimer','Wolfgang Wetzel','Gerhard Zickenheiner','Die Gr??nen','Gr??nen','Gr??nen-','(Die Gr??nen)']


    keyword_spd = ['Niels Annen', 'Ingrid Arndt-Bauer', 'Bela Bach', 'Heike Baehrens', 'Ulrike Bahr', 'Nezahat Baradari','Katarina Barley','Doris Barnett','Matthias Bartke',
    'S??ren Bartol','B??rbel Bas','Lothar Binding','Eberhard Brecht','Leni Breymaier','Karl-Heinz Brunner','Katrin Budde','Marco B??low','Martin Burkert','Lars Castellucci',
    'Bernhard Daldrup','Daniela De Ridder','Karamba Diaby','Esther Dilcher','Sabine Dittmar','Wiebke Esdar','Saskia Esken','Yasmin Fahimi','Johannes Fechner',
    'Fritz Felgentreu','Edgar Franke','Ulrich Freese','Dagmar Freitag','Sigmar Gabriel','Michael Gerdes','Martin Gerster','Angelika Gl??ckner','Timon Gremmels',
    'Kerstin Griese','Michael Gro??','Uli Gr??tsch','Bettina Hagedorn','Rita Hagl-Kehl','Metin Hakverdi','Sebastian Hartmann','Dirk Heidenblut',
    'Hubertus Heil','Gabriela Heinrich','Marcus Held','Wolfgang Hellmich','Barbara Hendricks','Gustav Herzog','Gabriele Hiller-Ohm','Thomas Hitschler',
    'Eva H??gl','Frank Junge','Josip Juratovic','Thomas Jurk','Oliver Kaczmarek','Johannes Kahrs','Elisabeth Kaiser','Ralf Kapschack','Gabriele Katzmarek',
    'Ulrich Kelber','Cansel Kiziltepe','Arno Klare','Lars Klingbeil','B??rbel Kofler','Daniela Kolbe','Elvan Korkmaz-Emre','Anette Kramme',
    'Christine Lambrecht','Christian Lange','Karl Lauterbach','Sylvia Lehmann','Helge Lindh','Burkhard Lischka','Hiltrud Lotze','Kirsten L??hmann',
    'Heiko Maas','Isabel Mackensen-Geis','Caren Marks','Dorothee Martin','Katja Mast','Christoph Matschie','Hilde Mattheis','Matthias Miersch',
    'Klaus Mindrup','Susanne Mittag','Falko Mohrs','Claudia Moll','Siemtje M??ller','Bettina M??ller','Detlef M??ller','Michelle M??ntefering',
    'Rolf M??tzenich','Andrea Nahles','Dietmar Nietan','Ulli Nissen','Thomas Oppermann','Josephine Ortleb','Mahmut ??zdemir','Aydan ??zo??uz',
    'Markus Paschke','Christian Petry','Detlev Pilger','Sabine Poschmann','Florian Post','Achim Post','Florian Pronold','Sascha Raabe',
    'Martin Rabanus','Mechthild Rawert','Carola Reimann','Andreas Rimkus','S??nke Rix','Dennis Rohde','Martin Rosemann','Ren?? R??spel',
    'Ernst Dieter Rossmann','Michael Roth','Susann R??thrich','Bernd R??tzel','Sarah Ryglewski','Johann Saathoff','Axel Sch??fer',
    'Nina Scheer','Marianne Schieder','Udo Schiefner','Nils Schmid','Uwe Schmidt','Ulla Schmidt','Dagmar Schmidt','Carsten Schneider',
    'Johannes Schraps','Michael Schrodi','Manja Sch??le','Ursula Schulte','Martin Schulz','Swen Schulz','Ewald Schurer','Frank Schwabe',
    'Stefan Schwartze','Andreas Schwarz','Rita Schwarzel??hr-Sutter','Rainer Spiering','Svenja Stadler','Martina Stamm-Fibich',
    'Sonja Amalie Steffen','Mathias Stein','Kerstin Tack','Claudia Tausend','Michael Thews','Markus T??ns','Carsten Tr??ger','Ute Vogt',
    'Marja-Liisa V??llers','Dirk V??pel','Gabi Weber','Joe Weingarten','Bernd Westphal','Dirk Wiese','G??listan Y??ksel','Dagmar Ziegler',
    'Stefan Zierke','Jens Zimmermann','SPD','sozialdemokraten','(SPD)','Sozialdemokratische Partei Deutschlands'
    ]

    keyword_afd = ['Dr. Bernd Baumann','Marc Bernhard','Andreas Bleck','Peter Boehringer','Stephan Brandner','J??rgen Braun','Marcus B??hl','Matthias B??ttner','Petr Bystron','Tino Chrupalla','Joana Cotar','Gottfried Curio','Siegbert F. Droese','Thomas Ehrhorn','Berengar Elsner von Gronow','Dr. Michael Espendiller','Peter Felser','Dietmar Friedhoff','Dr. Anton Friesen','Markus Frohnmaier','Dr. G??tz Fr??mming','Dr. Alexander Gauland','Prof. Dr. med. Axel Gehrke','Albrecht Glaser','Franziska Gminder','Wilhelm von Gottberg','Kay Gottschalk','Amin-Paulus Hampel','Mariana Harder-K??hnel','Dr. Roland Hartwig','Jochen Haug','Martin Hebner','Udo Hemmelgarn','Waldemar Herdt','Martin Hess','Heiko Hessenkemper','Karsten Hilse','Nicole H??chst','Martin Hohmann','Bruno Hollnagel','Leif-Erik Holm','Johannes Huber','Fabian Jacobi','Marc Jongen','Jens Kestner','Stefan Keuter','Norbert Kleinw??chter','Enrico Komning','J??rn K??nig','Steffen Kotr??','Rainer Kraft','R??diger Lucassen','Frank Magnitz','Lothar Maier','Jens Maier','Birgit Malsack-Winkemann','Corinna Miazga','Andreas Mrosek','Hansj??rg M??ller','Volker M??nz','Sebastian M??nzenmaier','Christoph Neumann','Jan Nolte','Ulrich Oehme','Gerold Otten','Tobias Matthias Peterka','Paul Viktor Podolay','J??rgen Pohl','Stephan Protschka','Martin Reichardt','Martin E. Renner','Roman Reusch','Ulrike Schielke-Ziesing','Robby Schlund','J??rg Schneider','Uwe Schulz','Thomas Seitz','Martin Sichert','Detlev Spangenberg','Dirk Spaniel','Ren?? Springer','Beatrix von Storch','Alice Weidel','Harald Weyel','Wolfgang Wiehle','Heiko Wildberg','Christian Wirth','Uwe Witt','AFD','afd','AfD','(AFD)','Alternative f??r Deutschland']

    # keyword_cdu2 = [i.split(' ', 1)[1] for i in keyword_cdu if ' ' in i & ""]
    # keyword_gruene2 = [i.split(' ', 1)[1] for i in keyword_gruene if ' ' in i]
    # keyword_fdp2 = [i.split(' ', 1)[1] for i in keyword_fdp if ' ' in i]
    # keyword_spd2 = [i.split(' ', 1)[1] for i in keyword_spd[:-1] if ' ' in i]
    # keyword_afd2 = [i.split(' ', 1)[1] for i in keyword_afd[:-1] if ' ' in i]
    #
    # keyword_cdu = keyword_cdu + keyword_cdu2
    # keyword_gruene = keyword_gruene + keyword_gruene2
    # keyword_fdp = keyword_fdp + keyword_fdp2
    # keyword_spd = keyword_spd + keyword_spd2
    # keyword_afd = keyword_afd + keyword_afd2

    keyword_dict = {
                'CDU': keyword_cdu,
                'Gruene':keyword_gruene,
                'FDP': keyword_fdp,
                'SPD': keyword_spd,
                'AFD': keyword_afd,
    }


    nlp = spacy.load("de_core_news_md")
    sentiws = spaCySentiWS(sentiws_path='data/sentiws/')
    nlp.add_pipe(sentiws)
    sentiment_cdu = []
    sentiment_gruene = []
    sentiment_fdp = []
    sentiment_spd = []
    sentiment_afd = []
    keyword_processor = KeywordProcessor()
    keyword_processor.add_keywords_from_dict(keyword_dict)
    del keyword_dict
    del keyword_cdu
    del keyword_spd
    del keyword_afd
    del keyword_gruene
    # del keyword_cdu2
    # del keyword_spd2
    # del keyword_afd2
    # del keyword_gruene2
    feeds = []
    for url in rss_urls:
        feeds.extend(feedparser.parse(url).entries)
        #print(feeds)
    for i in feeds:
        links.append(i.link)
        #print(links)
    del feeds

    task_list = []
    for index, link in enumerate(links):
        task_list.append(get_content(index, link))
    await asyncio.gather(*task_list)

    del task_list
    # for idx, i in enumerate(itertools.chain.from_iterable(content)):
    for idx in range(len(content)):
        #print(content[idx][0])
        keywords_found= keyword_processor.extract_keywords(str(content[idx][1]))
        count_gruene = keywords_found.count('Gruene')
        count_cdu = keywords_found.count('CDU')
        count_fdp = keywords_found.count('FDP')
        count_spd = keywords_found.count('SPD')
        count_afd = keywords_found.count('AFD')

        if count_gruene >= 1:
            content_gruene.append((content[idx][0],count_gruene,content[idx][1]))
        if count_cdu >= 1:
            content_cdu.append((content[idx][0],count_cdu,content[idx][1]))
        if count_fdp >= 1:
            content_fdp.append((content[idx][0],count_fdp,content[idx][1]))
        if count_spd >= 1:
            content_spd.append((content[idx][0],count_spd,content[idx][1]))
        if count_afd >= 1:
            content_afd.append((content[idx][0],count_afd,content[idx][1]))





    for cdu,gruene,fdp,spd,afd in zip(content_cdu, content_gruene, content_fdp, content_spd, content_afd ):
        blob= nlp(str(cdu[2:]))
        for token in blob:
            #print(token)
            if token._.sentiws is not None:
                sentiment_cdu.append(token._.sentiws)
                weight_cdu.append(cdu[1])
        if str(cdu[0]) not in links_cdu:
                links_cdu.append(str(cdu[0]))

        blob = nlp(str(gruene[2:]))
        for token in blob:
            if token._.sentiws is not None:
                sentiment_gruene.append(token._.sentiws)
                weight_gruene.append(gruene[1])
        if str(gruene[0]) not in links_gruene:
            links_gruene.append(str(gruene[0]))
        blob = nlp(str(fdp[2:]))
        for token in blob:
            if token._.sentiws is not None:
                sentiment_fdp.append(token._.sentiws)
                weight_fdp.append(fdp[1])
        if str(fdp[0]) not in links_fdp:
            links_fdp.append(str(fdp[0]))

        blob = nlp(str(spd[2:]))
        for token in blob:
            if token._.sentiws is not None:
                sentiment_spd.append(token._.sentiws)
                weight_spd.append(spd[1])
        if str(spd[0]) not in links_spd:
            links_spd.append(str(spd[0]))
        blob = nlp(str(afd[2:]))
        for token in blob:
            if token._.sentiws is not None:
                sentiment_afd.append(token._.sentiws)
                weight_afd.append(afd[1])
        if str(afd[0]) not in links_afd:
            links_afd.append(str(afd[0]))

        #print(sentiment_cdu)



    if sentiment_cdu:
        #meancdu = statistics.mean(sentiment_cdu)
        print(type(sentiment_cdu))
        print(type(weight_cdu))
        meancdu = np.average(sentiment_cdu, weights=weight_cdu)
    if sentiment_gruene:
        #meangruene = statistics.mean(sentiment_gruene)
        meangruene = np.average(sentiment_gruene, weights=weight_gruene)
    if sentiment_fdp:
        #meanfdp = statistics.mean(sentiment_fdp)
        meanfdp = np.average(sentiment_fdp, weights=weight_fdp)
    if sentiment_spd:
        #meanspd = statistics.mean(sentiment_spd)
        meanspd = np.average(sentiment_spd, weights=weight_spd)
    if sentiment_afd:
        #meanafd = statistics.mean(sentiment_afd)
        meanafd = np.average(sentiment_afd, weights=weight_afd)

    #today = date.today()
    now = datetime.now()
    today = str(now.strftime('%d/%m/%Y %H:%M:%S'))
    #sqlinsert = 'INSERT INTO crawldata (date,sentimentcdu,sentimentgruene,sentimentspd,sentimentfdp,sentimentafd) VALUES ();'
    #sqlinsert = 'INSERT INTO crawldata VALUES ();'




    mean = (today,meancdu,meangruene,meanfdp,meanspd,meanafd,links_cdu,links_gruene,links_spd,links_fdp,links_afd)


    add_data =  ("INSERT INTO crawldata "
               "(date,sentimentcdu,sentimentgruene,sentimentspd,sentimentfdp,sentimentafd,linkscdu,linksgruene,linksspd,linksfdp,linksafd) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    dbCursor.execute(add_data, mean)
    con.commit()




if __name__ == '__main__':
    asyncio.run(main(),debug=False)

print('done')




#if __name__ == '__main__':
