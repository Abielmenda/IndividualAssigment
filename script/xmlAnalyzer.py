import os
import pandas as pd
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import nltk
from nltk.corpus import stopwords

# Descargar las stopwords si no se han descargado
nltk.download('stopwords', quiet=True)
# Obtención de las rutas de directorios de entrada y salida
scriptDir = os.path.dirname(os.path.abspath(__file__))
proyectoDir = os.path.dirname(scriptDir)
entradaDir = os.path.join(proyectoDir, "entryData")
salidaDir = os.path.join(proyectoDir, "analysisResult")
# Variables locales para almacenar los respectivos resultados
abstracts = []
figuresCantidad = []
links_per_paper = {}
print("Analizing the documentation.\n")

# Bucle para recorrer todos los archivos de entrada .xml
for xml in os.listdir(entradaDir):
    xmlDir = os.path.join(entradaDir, xml)
# Gracias a la biblioteca Sopa se puede buscar facilmente lo que se pida en el archivo xml
    with open(xmlDir, "r", encoding="utf8") as f:
        xmlSopa = BeautifulSoup(f, "xml")
    nombreXml = xml.replace(".xml", "")

    # Para encontrar el abstract del paper, simplemente hay que buscar la etiqueta "abstract" en el xml gracias a Soup
    abstractBusqueda = xmlSopa.find("abstract")
    abstractTexto = ""
    if abstractBusqueda:
        abstractTexto = abstractBusqueda.get_text(separator=" ", strip=True)

    abstracts.append(abstractTexto)

    # Para encontrar las figures del paper, hay que buscar la etiqueta "figure"  y, en ocasiones "ref type=figure", en el xml gracias a Soup y por último contar cuantas hay
    figures = xmlSopa.find_all("figure")
    figurRefs = xmlSopa.find_all("ref", {"type": "figure"})
    numFigures = len(figures) + len(figurRefs)

    figuresCantidad.append({"paper": nombreXml, "figures": numFigures})

    # Para encontrar los links del paper, hay que buscar las etiqueta "ref type=url" y, en ocasiones "ptr target", en el xml gracias a Soup y se guardan en un set para evitar duplicados
    links = set()
    for ref in xmlSopa.find_all("ref", {"type": "url"}):
        if ref.get("target"):
            links.add(ref["target"].strip())
    for ptr in xmlSopa.find_all("ptr"):
        if ptr.get("target"):
            links.add(ptr["target"].strip())

    # Sin embargo, observo que hay url que no aparecen como links por lo que decido incluir una búsqueda de url y limpiarlas para evitar duplicados de links
    text = xmlSopa.get_text()
    urlFormato = r'https?://[A-Za-z0-9\.-]+\.[A-Za-z]{2,}[^ \n]*'
    found = re.findall(urlFormato, text)
    for url in found:
        urlLimpia = url.rstrip(".,;:)")
        links.add(urlLimpia)
    
    links_per_paper[nombreXml] = list(links)


# Tras analizar todos los papers de entrada, procede la construcción de la wordcloud
# Elimino las palabras mas comunes en inglés y aquellas que suelen aparecer en ámbito científico que considero que no aportan nada relevante sobre de qué tratan los papers
print("Creating a Word Cloud.\n")
stopWordsInglisPitinglis = set(stopwords.words("english"))
stopwords100cia = {"paper","method","approach","result","results","show","shows","propose","proposed","based","using","use","model","models","data","task","tasks","problem","problems","methods","across","however","without", "challenge", "better", "example", "challenges", "examples"}
stopwordsTotal = stopWordsInglisPitinglis.union(stopwords100cia)
# Hay que unir todos los abstracts en un string para la nube de palabras
all_abstracts = " ".join(abstracts)
wordcloud = WordCloud(width=800, height=400, background_color="white", stopwords=stopwordsTotal).generate(all_abstracts)
# Una vez realizada la nube, se crea la figura resultado y se exporta al directorio salida de resultados
plt.figure(figsize=(10,5))
plt.imshow(wordcloud)
plt.axis("off")
plt.title("Keyword Cloud from the Abstracts")
plt.savefig(os.path.join(salidaDir, "keyword_cloud.png"))
plt.close()


# Gracias a las clasicas bibliotecas pandas y matplotlib, se pasan los datos a un dataframe y posteriormente se realiza un histograma resultado que se exporta al directorio salida de resultados
print("Creating an histogram from number of figures.\n")
df = pd.DataFrame(figuresCantidad)
plt.figure(figsize=(10,6))
plt.bar(df["paper"], df["figures"])
plt.xticks(rotation=45)
plt.ylabel("Number of Figures")
plt.title("Figures per Article")
plt.tight_layout()
plt.savefig(os.path.join(salidaDir, "figures_per_paper.png"))
plt.close()

#Finalmente se agrega a un fichero resultado la lista de links por paper
print("Creating a link list.\n")
with open(os.path.join(salidaDir, "links_per_paper.txt"), "w", encoding="utf8") as fichero:
    for paper, links in links_per_paper.items():
        fichero.write(paper + "\n")
        if len(links) == 0:
            fichero.write("  No links found\n")
        for link in links:
            fichero.write("  " + link + "\n")
        fichero.write("\n")

print("Mission complete. Check the results saved in 'analysisResult/' folder.")