# textWordCount
A Python library that facilitates text analysis, utilizing [NLTK's capabilities](https://www.nltk.org/index.html). 

Documentation: https://yitsymc.github.io/textWordCount/textwordcount.html#textwordcount-class 

### Install
1. Download or clone this repository.
2. Run
`pip install /LOCALLY_PATH_OF_THE_PROJECT/dist/textwordcount-0.1.0-py3-none-any.whl`

### Usage
This library requires a **text** or the **path of a public URL** to analyze.
It supports multilanguage (English and Spanish), by default works in English.

#### Static text in English
> from textwordcount.functions import TextWordCount
> 
> sample_text="""Python is an easy to learn, powerful programming language. 
    It has efficient high-level data structures and a simple but 
    effective approach to object-oriented programming. 
    Python’s elegant syntax and dynamic typing, together with its 
    interpreted nature, make it an ideal language for scripting and 
    rapid application development in many areas on most platforms."""
> 
> t = TextWordCount(text=text)
> 
> t.top_used_words(count=5)

`Output: ['Python', 'programming', 'language', 'easy', 'learn']`

#### Static text in Spanish
For Spanish, you need to specify the language, otherwise won't work properly (see an example below)

> from textwordcount.functions import TextWordCount
> 
> spanish_text="""Python es un lenguaje de programación potente y fácil de aprender. Tiene estructuras de datos de alto nivel eficientes y un simple pero efectivo sistema de programación orientado a objetos. La elegante sintaxis de Python y su tipado dinámico, junto a su naturaleza interpretada lo convierten en un lenguaje ideal para scripting y desarrollo rápido de aplicaciones en muchas áreas, para la mayoría de plataformas."""
> 
> t = TextWordCount(text=spanish_text, language="spanish", iso_639_lang="es")
> 
> t.top_used_words(count=5)

`Output: ['Python', 'lenguaje', 'programación', 'potente', 'fácil']`

#### URL source in English
Important: The URL needs to be public, otherwise the library can't fetch the content.
> from textwordcount.functions import TextWordCount
> 
> source = "https://docs.python.org/3/tutorial/index.html"
> 
> t = TextWordCount(html_source=source)
> 
> t.count_word_usage_in_text(['Python'])

`Output: {'python': 33}`

#### URL source in Spanish
> from textwordcount.functions import TextWordCount
> 
> source = "https://docs.python.org/es/3/tutorial/index.html"
> 
> t = TextWordCount(html_source=source)
> 
> t.count_word_usage_in_text(['Python', 'lenguaje', 'funcionalidades'])

`Output: {'python': 32, 'lenguaje': 8, 'funcionalidades': 2}`
