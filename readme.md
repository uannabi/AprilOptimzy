## Parsing Simple Wikipedia 

 
Your task is to submit a CLI tool that allows us to parse [Simple Wikipedia](https://simple.wikipedia.org/wiki/Main_Page) (which is a small subset of the English Wikipedia) and extract the counts of the pairs (anchor, target) around each link in every page of the XML dump. We have already done some heavy lifting for you and used the [rubyslippers](https://github.com/alvations/rubyslippers) library to transform the XML dump into JSON.

After downloading the data (see below), you should have the following structure in a local `data` folder:

```
total 18832
drwxr-xr-x  65535 staff   2.9M  9 Jun 15:11 pages/
-rw-r--r--      1 staff   9.2M 15 Jun 14:13 redirects.nt
```

The file `redirects.nt` corresponds to a file containing Wikipedia redirects that lead different spellings of a page title to the "real" title for the page. The structure of the file looks like this:

```
$ds_hr/wikiparsing │ wikipedia ?2  head -10 data/redirects.nt                                                                                  ✔ │ base Py │ 14:15:33 
<http://dbpedia.org/resource/'N_Sync> <http://dbpedia.org/ontology/wikiPageRedirects> <http://dbpedia.org/resource/NSYNC> .
<http://dbpedia.org/resource/1_E19_s_and_more> <http://dbpedia.org/ontology/wikiPageRedirects> <http://dbpedia.org/resource/Terasecond_and_longer> .
<http://dbpedia.org/resource/2010_World_Cup> <http://dbpedia.org/ontology/wikiPageRedirects> <http://dbpedia.org/resource/2010_FIFA_World_Cup> .
<http://dbpedia.org/resource/22_February_2006_al-Askari_Mosque_bombing> <http://dbpedia.org/ontology/wikiPageRedirects> <http://dbpedia.org/resource/2006_al-Askari_mosque_bombing> .
<http://dbpedia.org/resource/29_October> <http://dbpedia.org/ontology/wikiPageRedirects> <http://dbpedia.org/resource/October_29> .
<http://dbpedia.org/resource/2_August> <http://dbpedia.org/ontology/wikiPageRedirects> <http://dbpedia.org/resource/August_2> .
<http://dbpedia.org/resource/7UP> <http://dbpedia.org/ontology/wikiPageRedirects> <http://dbpedia.org/resource/7_Up> .
<http://dbpedia.org/resource/7_January> <http://dbpedia.org/ontology/wikiPageRedirects> <http://dbpedia.org/resource/January_7> .
<http://dbpedia.org/resource/9_August> <http://dbpedia.org/ontology/wikiPageRedirects> <http://dbpedia.org/resource/August_9> .
<http://dbpedia.org/resource/APG_II> <http://dbpedia.org/ontology/wikiPageRedirects> <http://dbpedia.org/resource/Angiosperm_Phylogeny_Group> .
```


The `pages` folder contains a bunch of JSON files each corresponding to a Wikipedia page and each has the following schema:

```
{
	"id": 892,
	"url": "http://en.wikipedia.org/wiki/Alfons_Maria_Jakob",
	"text": "Alfons Maria Jakob (2 July 1884 in Aschaffenburg/Bavaria \u2013 17 October 1931 in Hamburg) was a German neurologist who worked in the field of neuropathology.\nHe was born in Aschaffenburg, Bavaria and educated in medicine at the universities of Munich, Berlin, and Strasbourg, where he received his doctorate in 1908. During the following year, he began clinical work under the psychiatrist Emil Kraepelin and did laboratory work with Franz Nissl and Alois Alzheimer in Munich.\nIn 1911, by way of an invitation from Wilhelm Weygandt, he relocated to Hamburg, where he worked with Theodor Kaes and eventually became head of the laboratory of anatomical pathology at the psychiatric State Hospital Hamburg-Friedrichsberg. Following the death of Kaes in 1913, Jakob succeeded him as prosector. During World War I he served as an army physician in Belgium, and afterwards returned to Hamburg. In 1919 he obtained his habilitation for neurology and in 1924 became a professor of neurology. Under Jakob's guidance the department grew rapidly. He made significant contributions to knowledge on concussion and secondary nerve degeneration and became a doyen of neuropathology.\nJakob was the author of five monographs and nearly 80 scientific papers. His neuropathological research contributed greatly to the delineation of several diseases, including multiple sclerosis and Friedreich's ataxia. He first recognised and described Alper's disease and Creutzfeldt\u2013Jakob disease (named along with Munich neuropathologist Hans Gerhard Creutzfeldt). He gained experience in neurosyphilis, having a 200-bed ward devoted entirely to that disorder. Jakob made a lecture tour of the United States (1924) and South America (1928), of which, he wrote a paper on the neuropathology of yellow fever.\nHe suffered from chronic osteomyelitis for the last seven years of his life. This eventually caused a retroperitoneal abscess and paralytic ileus from which he died following operation.",
	"categories": [],
	"infobox_types": [],
	"annotations": [{
		"uri": "Aschaffenburg",
		"surface_form": "Aschaffenburg",
		"offset": 35
	}, {
		"uri": "Bavaria",
		"surface_form": "Bavaria",
		"offset": 49
	}, {
		"uri": "Hamburg",
		"surface_form": "Hamburg",
		"offset": 78
	}, {
		"uri": "Neurologist",
		"surface_form": "neurologist",
		"offset": 100
	}, {
		"uri": "Neuropathology",
		"surface_form": "neuropathology",
		"offset": 139
	}, {
		"uri": "Aschaffenburg",
		"surface_form": "Aschaffenburg",
		"offset": 170
	}, {
		"uri": "Bavaria",
		"surface_form": "Bavaria",
		"offset": 185
	},  ....
	]
}
```

You can download the data file from [this link](https://episerver99-my.sharepoint.com/:u:/g/personal/zsolt_pocsaji_episerver_com/EcOg8ysFNMNEg6Idch1DLiEBQthLmOKYaFoTzYEL_aVHdA?e=keAccx) and unpack it at the base folder.

The aim is to count how many times pairs of (`surface_form`, `uri`) occur in the whole dataset. This information can be extracted from the `annotations` field of each page. Note also that the final URIs need to be resolved using the `redirects` file provided. Let's walk through an example.

Suppose that in the redirects file, there's a line like this:

`<http://dbpedia.org/resource/Bavaria> <http://dbpedia.org/ontology/wikiPageRedirects> <http://dbpedia.org/resource/Bavaria_(German_region)> .`

If we take the example of the JSON schema above anc coult the `(surface_form, uri)`, we will find this entry:

 - `(Bavaria, Bavaria), 2`

Now, note that the URI is not resolved because `Bavaria` redirects to `Bavaria_(German_region)`, so the count for the page should be then transformed to:

 - `(Bavaria, Bavaria_(German_region)), 2`

Finally, it's important to note that we want the **global** count of pairs (not the counts by page), so you must somehow aggregate these counts over all the dataset to produce a final result. In other words, the count of `(Bavaria, Bavaria_(German_region))` should be much greater than `2` ;-) .


We have defined a helper `pair_counts.py` file to assist you. It has some boiler plate defined, but you need to fill it out yourself and write some extra functions or two. You can also solve this using another programming language like Scala (in which case the Python code might help you by acting as a guide).

If you use extra libraries, please amend the provided `requirements.txt` file and this README with instructions. The only library we placed there is the CLI tool `fire`. Once everything is ready, we could use the tool by running:

`python pair_counts.py --in-folder <path-to-data> --out-folder <path-to-counts-destination>` , where
	* `<path-to-data>` corresponds to the data folder , e.g. data
	* `<path-to-counts-destination>` corresponds to a folder that contains one or more `.tsv` files of the format

```
uri<tab>surface_form<tab>count
```
