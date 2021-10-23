import requests
from pprint import pprint

dbpedia_url = "http://dbpedia.org/sparql"

entity = "http://dbpedia.org/resource/Charles_Plosser"
query = "PREFIX dbr: <http://dbpedia.org/resource/> \n" + "SELECT ?propertyLabel (GROUP_CONCAT(DISTINCT ?valueLabel ; SEPARATOR=\", \") AS ?valueLabel ) {\n"+ "<" + entity + """> ?property ?value .
		OPTIONAL {?property rdfs:comment ?auxProperty .}
		FILTER (!bound(?auxProperty ) || !strstarts(str(?auxProperty),
						str("Reserved for DBpedia")))

		FILTER (!strstarts( str(?property),
						str("http://dbpedia.org/ontology/abstract")))

		?property rdfs:label ?propertyLabel .
		FILTER (LANGMATCHES(LANG(?propertyLabel ), "en"))

		OPTIONAL {?value rdfs:label ?auxValue .}
		BIND (IF(isLiteral(?value), ?value, ?auxValue) AS ?valueLabel)
		FILTER (isNumeric(?valueLabel) || 
						LANGMATCHES(LANG(?valueLabel ), "en"))
	}
	"""

query1 = "PREFIX dbr: <http://dbpedia.org/resource/> \n" + "SELECT ?propertyLabel (GROUP_CONCAT(DISTINCT ?valueLabel ; SEPARATOR=\", \") AS ?valueLabel ) { \n" + """<http://dbpedia.org/resource/Charles_Plosser> ?property ?value . 
    OPTIONAL {?property rdfs:comment ?auxProperty .}
    FILTER (!bound(?auxProperty ) || !strstarts(str(?auxProperty),
                    str("Reserved for DBpedia")))

    FILTER (!strstarts( str(?property),
                    str("http://dbpedia.org/ontology/abstract")))

    ?property rdfs:label ?propertyLabel .
    FILTER (LANGMATCHES(LANG(?propertyLabel ), "en"))

    OPTIONAL {?value rdfs:label ?auxValue .}
    BIND (IF(isLiteral(?value), ?value, ?auxValue) AS ?valueLabel)
    FILTER (isNumeric(?valueLabel) ||
                    LANGMATCHES(LANG(?valueLabel ), "en"))
    }
    """

query2 = "PREFIX dbr: <http://dbpedia.org/resource/> \n" + "SELECT ?propertyLabel (GROUP_CONCAT(DISTINCT ?valueLabel ; SEPARATOR=\", \") AS ?valueLabel ) { \n" + "?value ?property  <" + entity + """>.
    OPTIONAL {?property rdfs:comment ?auxProperty .}
    FILTER (!bound(?auxProperty ) || !strstarts(str(?auxProperty),
                    str("Reserved for DBpedia")))

    FILTER (!strstarts( str(?property),
                    str("http://dbpedia.org/ontology/abstract")))

    ?property rdfs:label ?propertyLabel .
    FILTER (LANGMATCHES(LANG(?propertyLabel ), "en"))

    OPTIONAL {?value rdfs:label ?auxValue .}
    BIND (IF(isLiteral(?value), ?value, ?auxValue) AS ?valueLabel)
    FILTER (isNumeric(?valueLabel) ||
                    LANGMATCHES(LANG(?valueLabel ), "en"))
    }
    """


payload = {
    'default-graph-uri': 'http://dbpedia.org', 
    'query': query, 
    'format': 'application/json', 
    'timeout': 30000, 
    'signal_void':'on', 
    'signal_unconnected':'on' }


response = requests.get(dbpedia_url, params=payload)

pprint(response.json())
print("\n")

payload = {
    'default-graph-uri': 'http://dbpedia.org', 
    'query': query2, 
    'format': 'application/json', 
    'timeout': 30000, 
    'signal_void':'on', 
    'signal_unconnected':'on' }


response = requests.get(dbpedia_url, params=payload)

pprint(response.json())

