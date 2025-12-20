"""CSC108: Fall 2025 -- Assignment 3: arxiv.org metadata

Instructions (READ THIS FIRST!)
===============================

Make sure that the files constants.py, a3_checker.py, and checker_generic.py
are in the same directory as this file.


Copyright and Usage Information
===============================

This code is provided solely for the personal and private use of students
taking CSC108 at the University of Toronto. Copying for purposes other than
this use is expressly prohibited. All forms of distribution of this code, 
whether as given or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2025 CSC108H1 Teaching Team
"""

import pprint # needed to format output
import copy  # needed in examples of functions that modify input dict
from typing import TextIO
from constants import (ID, TITLE, CREATED, MODIFIED, AUTHORS, ABSTRACT, END,
                       NameType, ArticleType, ArxivType)

##############################################################################
# Sample data for use in docstring examples
##############################################################################

# NOTE: Some dictionary keys are set using the values of provided constants.

EXAMPLE_ARXIV = {
    '5090': {
        ID: '5090',
        TITLE: "Increasing Students' Engagement to Reminder Emails",
        CREATED: '',
        MODIFIED: '2022-08-02',
        AUTHORS: [('Yanez', 'Fernando'), ('Zavaleta-Bernuy', 'Angela')],
        ABSTRACT: 'Our metric of interest is open email rates.'},
    '03221': {
        ID: '03221',
        TITLE: 'Stargazer: An Interactive Camera Robot for How-To Videos',
        CREATED: '2023-03-01',
        MODIFIED: '2023-03-06',
        AUTHORS: [('Grossman', 'Tovi')],
        ABSTRACT: 'We present Stargazer, a novel approach for assisting ' +
                  'with tutorial content creation.'},
    '0001': {
        ID: '0001',
        TITLE: 'Cats and Dogs Can Co-Exist',
        CREATED: '2023-08-20',
        MODIFIED: '2023-10-02',
        AUTHORS: [('Smith', 'Jacqueline E.'), ('Sharmin', 'Sadia')],
        ABSTRACT: 'We show a formal proof that cats and dogs\n' +
        'can peacefully co-exist!'},
    '108': {
        ID: '108',
        TITLE: 'CSC108 is the Best Course Ever',
        CREATED: '2023-09-01',
        MODIFIED: '',
        AUTHORS: [('Smith', 'Jacqueline E.'), ('Zavaleta-Bernuy', 'Angela'),
                  ('Campbell', 'Jen')],
        ABSTRACT: 'We present clear evidence that Introduction to\n'
        + 'Computer Programming is the best course'},
    '42': {
        ID: '42',
        TITLE: '',
        CREATED: '2023-05-04',
        MODIFIED: '2023-05-05',
        AUTHORS: [],
        ABSTRACT: 'This is a strange article with no title\n'
        + 'and no authors.\n\nIt also has a blank line in its abstract!'}
}

EXAMPLE_BY_AUTHOR = {
    ('Campbell', 'Jen'): ['108'],
    ('Grossman', 'Tovi'): ['03221'],
    ('Sharmin', 'Sadia'): ['0001'],
    ('Smith', 'Jacqueline E.'): ['0001', '108'],
    ('Yanez', 'Fernando'): ['5090'],
    ('Zavaleta-Bernuy', 'Angela'): ['108', '5090']
}

EXAMPLE_ARXIV_1 = {
    '123': {
        ID: '123', 
        TITLE: 'Stigma and Stamen: Onagraceae Organisation', 
        CREATED: '2022-09-30', 
        MODIFIED: '2025-09-30', 
        AUTHORS: [('Genet', 'Emmeline F.')], 
        ABSTRACT: 'Fuchsia-poeisis with a special focus on the Chilco flower, '
        + 'or Fuchsia magellanica.'}, 
    '456': {
        ID: '456', 
        TITLE: 'Communication and Control', 
        CREATED: '2014-25-12', 
        MODIFIED: '', 
        AUTHORS: [('Maus', 'John')], 
        ABSTRACT: 'I situate and analyze the increasingly informatic, '
        + 'molecular, and distributed technologies of power characteristic of '
        + '"control societies" on a thoroughly substantive level.'},
    '789': {
        ID: '789', 
        TITLE: 'Beyond One-Dimensional Theory and Praxis: '
        + 'A Marcusean Alliance with Black Feminism', 
        CREATED: '2023-27-11', 
        MODIFIED: '2023-29-11', 
        AUTHORS: [('Yokum', 'Nicole')], 
        ABSTRACT: 'Among early Frankfurt School theorists, '
        + 'Herbert Marcuse would seem to be a prime candidate for '
        + 'an alliance with Black Feminist theory and praxis,\n'
        + 'if only because of his mentorship of radical Black thinker '
        'and activist Angela Davis.'}, 
    '10': {
        ID: '10', 
        TITLE: 'ARTICLE REDACTED', 
        CREATED: '', 
        MODIFIED: '', 
        AUTHORS: [('Wagner', 'Erich'), ('Cethirakath', 'Ingrid')], 
        ABSTRACT: ''}
}

BLANK_ARXIV = {
    '0': {
        ID: '0', 
        TITLE: '', 
        CREATED: '', 
        MODIFIED: '', 
        AUTHORS: [], 
        ABSTRACT: ''}
}
###############################################################################
# Helper function to use in your code later on.  Do not change this function.
###############################################################################
def clean_word(word: str) -> str:
    """Return word with all non-alphabetic characters removed and converted to 
    lowercase.
    
    Precondition: word contains no whitespace
    
    >>> clean_word('Hello!!!')
    'hello'
    >>> clean_word('12cat.dog?')
    'catdog'
    >>> clean_word("DON'T")
    'dont'
    """
    new_word = ''
    for ch in word:
        if ch.isalpha():
            new_word = new_word + ch.lower()
    return new_word


###############################################################################
# Task 1 - Working with ArxivType
###############################################################################
def created_in_year(id_to_article: ArxivType, identifier: str, year: int
                    ) -> bool:
    """Return True iff id_to_article contains an article with ID identifier
    that was created in year year.
    
    >>> created_in_year(EXAMPLE_ARXIV, '108', 2023)
    True
    >>> created_in_year(EXAMPLE_ARXIV, '5090', 2022)
    False
    >>> created_in_year(EXAMPLE_ARXIV, '0', 2025)
    False
    """
    if identifier in id_to_article and id_to_article[identifier][CREATED]:
        return int(id_to_article[identifier][CREATED][:4]) == year
    return False

def contains_keyword(id_to_article: ArxivType, keyword: str) -> list[str]:
    """Return a list (sorted in lexicographic order)
    of the IDs of articles in id_to_article whose title, authors, or abstract 
    contain exactly keyword. Punctuation-insensitive and case-insensitive.
    
    >>> contains_keyword(EXAMPLE_ARXIV, 'e')
    ['0001', '108']
    >>> contains_keyword(EXAMPLE_ARXIV, 'stargaze')
    []
    >>> contains_keyword(EXAMPLE_ARXIV, 'foobar')
    []
    """
    matches = []
    id_to_words = {}
    
    for article in id_to_article.values():
        id_to_words[article[ID]] =\
            (article[TITLE].split() + article[ABSTRACT].split())
        for tup in article[AUTHORS]:
            for string in tup:
                id_to_words[article[ID]] += string.split()
        
    for key in id_to_words:
        if keyword in [clean_word(word) for word in id_to_words[key]]:
            matches.append(key)
                
    matches.sort()
    
    return matches
            
            
def average_author_count(id_to_article: ArxivType) -> float:
    """Return the average number of authors per article in id_to_article.
    
    >>> average_author_count(EXAMPLE_ARXIV)
    1.6
    >>> average_author_count(EXAMPLE_ARXIV_1)
    1.25
    >>> average_author_count({})
    0.0
    """
    count = 0.0
    for article in id_to_article.values():
        count += len(article[AUTHORS])
            
    if count:
        return count / len(id_to_article)
    return count
        
        
###############################################################################
# Task 2 - Reading in the arxiv metadata
###############################################################################

def read_arxiv_file(f: TextIO) -> ArxivType:
    """Return an ArxivType dictionary containing the arxiv metadata in f.

    Note: example calls for functions that take open files are not necessary."""

    # TODO write the body of the function here
    
    # Read the file into a nested list whose inner lists each contain 
    # the data of one article respectively.

    contents = []
    article = []
    
    for line in f:
        if line.strip() != 'END':
            article.append(line)
        else:
            contents.append(article)
            article = []

    # Mutate contents so that all data occurs as inner ArticleType dicts.
    
    articletype_contents(contents)
    
    # Initialise, populate, then return the final ArxivType dict.
    
    id_to_article = {}
    
    for article in contents:
        id_to_article[article[ID]] = article
        
    return id_to_article

# TODO write any helper functions you need for Task 2 here

def articletype_contents(contents: list[list]) -> None:
    """
    Helper function for read_arxiv_file. Mutates contents by replacing each
    inner list with an ArticleType dict containing the data of that inner list.
    
    Precondition: contents is a list of lists read from a structured file by
    read_arxiv_file.
       
    >>> example = [['5090\n', 
    "Increasing Students' Engagement to Reminder Emails\n", '\n', 
    '2022-08-02\n', 'Yanez,Fernando\n', 'Zavaleta-Bernuy,Angela\n', '\n', 
    'Our metric of interest is open email rates.\n']]
    >>> articletype_contents(example)
    >>> example[0] == EXAMPLE_ARXIV['5090']
    True
    >>> example_1 = [['42\n', '\n', '2023-05-04\n', '2023-05-05\n', '\n',
    'This is a strange article with no title\n', 'and no authors.\n', '\n', 
    'It also has a blank line in its abstract!\n']]
    >>> articletype_contents(example_1)
    >>> example_1[0] == EXAMPLE_ARXIV['42']
    True
    """
    nametype_authors(contents)
    collect_authors(contents)
    collect_abstracts(contents)
    clean_contents(contents)
        
    for a in range(len(contents)):
        articletype_instance = {ID: '', TITLE: '', CREATED: '',
                            MODIFIED: '', AUTHORS: [], ABSTRACT: ''}
        i = 0
        for key in articletype_instance:           
            articletype_instance[key] = contents[a][i]
            i += 1
        contents[a] = articletype_instance


def nametype_authors(contents: list[list]) -> None:
    """Helper function for articletype_contents. Reformat authors in 
    each inner list in contents so they appear as NameType tuples. 
    If there are no authors, there are no changes.
    
    Precondition: contents is a list of lists read from a structured file by
    read_arxiv_file.
 
    >>> example = [['5090\n', 
    "Increasing Students' Engagement to Reminder Emails\n", '\n',
    '2022-08-02\n', 'Yanez,Fernando\n', 'Zavaleta-Bernuy,Angela\n', '\n',
    'Our metric of interest is open email rates.\n']]
    >>> nametype_authors(example)
    >>> example[0][4:6] == EXAMPLE_ARXIV['5090'][AUTHORS]
    True
    >>> example_1 = [['03221\n', 
    'Stargazer: An Interactive Camera Robot for How-To Videos\n',
    '2023-03-01\n', '2023-03-06\n', 'Grossman,Tovi\n', '\n',
    'We present Stargazer, a novel approach for assisting with '
    + 'tutorial content creation.\n']]
    >>> nametype_authors(example_1)
    >>> [example_1[0][4]] == EXAMPLE_ARXIV['03221'][AUTHORS]
    True
    """
    for article in contents:
        i = 4
        while article[i] != '\n':
            article[i] = tuple((article[i].strip()).split(','))
            i += 1
            
            
def collect_authors(contents: list[list]) -> None:
    """Helper function for articletype_contents. Mutates contents by 
    collecting authors in each inner list into a single list collection 
    per inner list of authors. If there are no authors, 
    this collection is empty.
    
    Precondition: contents has been passed to nametype_authors.
    
    >>> example = [['0001\n', 'Cats and Dogs Can Co-Exist\n', '2023-08-20\n',
    '2023-10-02\n', ('Smith', 'Jacqueline E.'), ('Sharmin', 'Sadia'), '\n',
    'We show a formal proof that cats and dogs\n',
    'can peacefully co-exist!\n']]
    >>> collect_authors(example)
    >>> example[0][4] == EXAMPLE_ARXIV['0001'][AUTHORS]
        True
    >>> example_1 = [['42\n', '\n', '2023-05-04\n', '2023-05-05\n', '\n',
    'This is a strange article with no title\n', 'and no authors.\n', '\n',
    'It also has a blank line in its abstract!\n']]
    >>> collect_authors(example_1)
    >>> example_1[0][4] == EXAMPLE_ARXIV['42'][AUTHORS]
    True
    """
    for article in contents:
        i = 4
        authors = []
        while article[i] != '\n':
            authors.append(article[i])
            i += 1
        article.insert(4, authors)
            
    for i in range(len(contents)):
        contents[i] = [item for item in contents[i] if type(item) != tuple]


def collect_abstracts(contents: list[list]) -> None:
    """Helper function for articletype_contents. Mutates contents by 
    collecting the abstract in each inner list in contents into a single string.
    If the abstract is already a single string, or if there is no abstract, 
    contents appears unchanged.
    
    Precondition: contents has been passed to collect_authors.
    
    >>> example = [['0001\n', 'Cats and Dogs Can Co-Exist\n', '2023-08-20\n', 
    '2023-10-02\n', [('Smith', 'Jacqueline E.'), ('Sharmin', 'Sadia')], '\n',
    'We show a formal proof that cats and dogs\n', 
    'can peacefully co-exist!\n']]
    >>> collect_abstracts(example)
    >>> example[0][6].strip() == EXAMPLE_ARXIV['0001'][ABSTRACT]
    True
    >>> example_1 = [['03221\n', 
    'Stargazer: An Interactive Camera Robot for How-To Videos\n', 
    '2023-03-01\n', '2023-03-06\n', [('Grossman', 'Tovi')], '\n', 
    'We present Stargazer, a novel approach for assisting '
    + 'with tutorial content creation.\n']]
    >>> collect_abstracts(example_1)
    >>> example_1[0][6].strip() == EXAMPLE_ARXIV['03221'][ABSTRACT]
    True
    >>> example_2 = [['10\n', 'REDACTED ARTICLE\n', '\n', '\n', 
    [('Wagner', 'Erich'), ('Cethirakath', 'Ingrid')], '\n']]
    >>> collect_abstracts(example_2)
    >>> example_2[0][6] == EXAMPLE_ARXIV_1['10'][ABSTRACT]
    True
    """
    for article in contents:
        i = 6
        current_abstract = ''
        while i < len(article):
            current_abstract += article[i]
            article[i] = ()
            i += 1
        article.append(current_abstract)
        
    for i in range(len(contents)):
        contents[i] = [item for item in contents[i] if item != ()]
        

def clean_contents(contents: list[list]) -> None:
    """
    Helper function for articletype_contents. Mutates contents by stripping 
    leading and trailing whitespace and removing the newline delimiter 
    at index 5 in each inner list.
    
    Precondition: contents has been passed to collect_abstracts.
    
    >>> example = [['0001\n', 'Cats and Dogs Can Co-Exist\n', '2023-08-20\n', 
    '2023-10-02\n', [('Smith', 'Jacqueline E.'), ('Sharmin', 'Sadia')], '\n',
    'We show a formal proof that cats and dogs\ncan peacefully co-exist!\n']]
    >>> clean_contents(example)
    >>> (len(example[0]) == len(EXAMPLE_ARXIV['0001']) and
    example[0][5] == EXAMPLE_ARXIV['0001'][ABSTRACT])
    True
    >>> example_1 = [['42\n', '\n', '2023-05-04\n', '2023-05-05\n', [], '\n', 
    'This is a strange article with no title\nand no authors.\n\n'
    + 'It also has a blank line in its abstract!\n']]
    >>> clean_contents(example_1)
    >>> (len(example_1[0]) == len(EXAMPLE_ARXIV['42']) and
    example_1[0][5] == EXAMPLE_ARXIV['42'][ABSTRACT])
    True
    """
    for i in range(len(contents)):
        contents[i].pop(5)
        contents[i] = [item if type(item) == list else\
                    item.strip() for item in contents[i]]


###############################################################################
# Task 3 - Working with Authors and Coauthors
###############################################################################

def make_author_to_articles(id_to_article: ArxivType
                            ) -> dict[NameType, list[str]]:
    """Return a dict that maps each author name to a list (sorted in
    lexicographic order) of IDs of articles written by that author,
    based on the information in id_to_article.

    >>> make_author_to_articles(EXAMPLE_ARXIV) == EXAMPLE_BY_AUTHOR
    True
    >>> make_author_to_articles({})
    {}
    """
    # We have provided the docstring for this function as an example of how
    # to compare dictionaries in a docstring example

    # TODO write the body of the function here
    
    author_to_articles = {}
    articles = id_to_article.values()
    
    for article in articles:
        for author in article[AUTHORS]:
            author_to_articles[author] = []
            
    for author in author_to_articles:
        for article in articles:
            if author in article[AUTHORS]:
                author_to_articles[author].append(article[ID])
    
    for author in author_to_articles:
        author_to_articles[author].sort()
    
    return author_to_articles

# TODO write the rest of your Task 3 functions here

def get_coauthors(id_to_article: ArxivType, author: NameType
                  ) -> list[NameType]:
    """Return a list (sorted in lexicographic order) of 
    coauthors of author in id_to_article.
    
    >>> get_coauthors(EXAMPLE_ARXIV, ('Smith', 'Jacqueline E.'))
    [('Campbell', 'Jen'), ('Sharmin', 'Sadia'), ('Zavaleta-Bernuy', 'Angela')]
    >>> get_coauthors(EXAMPLE_ARXIV, ('Zavaleta-Bernuy', 'Angela'))
    [('Campbell', 'Jen'), ('Smith', 'Jacqueline E.'), ('Yanez', 'Fernando')]
    >>> get_coauthors(EXAMPLE_ARXIV_1, ('Genet', 'Emmeline F.'))
    []
    """
    coauthors = []
    common_articles = []
    authors_to_articles = make_author_to_articles(id_to_article)
    
    if author not in authors_to_articles:
        return coauthors
    
    common_articles += authors_to_articles[author]

    for identifier in common_articles:
        for key in authors_to_articles:
            if key != author and\
            identifier in authors_to_articles[key] and\
            key not in coauthors:
                coauthors.append(key)
    
    coauthors.sort()
    
    return coauthors


def get_most_published_authors(id_to_article: ArxivType) -> list[NameType]:
    """Return a list (sorted in lexicographic order) of authors with the 
    most published articles in id_to_article. There may be one or more
    most published authors.
    
    >>> get_most_published_authors(EXAMPLE_ARXIV)
    [('Smith', 'Jacqueline E.'), ('Zavaleta-Bernuy', 'Angela')]
    >>> get_most_published_authors(EXAMPLE_ARXIV_1)
    [('Cethirakath', 'Ingrid'), ('Genet', 'Emmeline F.'), 
    ('Maus', 'John'), ('Wagner', 'Erich'), ('Yokum', 'Nicole')]
    >>> get_most_published_authors(BLANK_ARXIV)
    []
    """
    authors_to_articles = make_author_to_articles(id_to_article)
    authors_to_counts = {}
    most_published_authors = []

    for author in authors_to_articles:
        authors_to_counts[author] = len(authors_to_articles[author])
    
    if not authors_to_counts:
        return most_published_authors
        
    maximum = max(authors_to_counts.values())
    
    for author in authors_to_counts:
        if authors_to_counts[author] == maximum:
            most_published_authors.append(author)
    
    most_published_authors.sort()
    
    return most_published_authors
        

def suggest_collaborators(id_to_article: ArxivType, author: NameType) ->\
    list[NameType]:
    """Return a list of suggested collaborators for
    author in id_to_article. Suggested collaborators are coauthors
    of coauthors of author (excluding pre-existing coauthors of author).
    
    >>> suggest_collaborators(EXAMPLE_ARXIV, ('Yanez', 'Fernando'))
    [('Campbell', 'Jen'), ('Smith', 'Jacqueline E.')]
    >>> suggest_collaborators(EXAMPLE_ARXIV, ('Grossman', 'Tovi'))
    []
    """
    suggested = []
    coauthors = get_coauthors(id_to_article, author)
    
    for coauthor in coauthors:
        suggested +=\
        [item for item in get_coauthors(id_to_article, coauthor) if\
         not (item in suggested or item in coauthors or item == author)]
    
    suggested.sort()
    
    return suggested
    

###############################################################################
# Task 4 - Prolific Authors
###############################################################################

# TODO write your Task 4 functions here

def has_prolific_authors(author_to_articles: dict[NameType, list[str]], 
    article: ArticleType, min_publications: int) -> bool:
    """Return True iff article has at least one author that is considered 
    prolific. A prolific author has at least min_publications articles 
    published in author_to_articles.
    
    >>> D = make_author_to_articles(EXAMPLE_ARXIV)
    >>> A = EXAMPLE_ARXIV['5090']
    >>> has_prolific_authors(D, A, 2)
    True
    >>> A = EXAMPLE_ARXIV['03221']
    >>> has_prolific_authors(D, A, 2)
    False
    """
    prolific = []
    
    for author in author_to_articles:
        if len(author_to_articles[author]) >= min_publications:
            prolific.append(author)
    
    for author in article[AUTHORS]:
        if author in prolific:
            return True
    
    return False


def keep_prolific_authors(id_to_article: ArxivType,
                          min_publications: int) -> None:
    """Update id_to_article so that it contains only articles published by
    authors with min_publications or more articles published. As long
    as at least one of the authors has min_publications, the article
    is kept.

    >>> arxiv_copy = copy.deepcopy(EXAMPLE_ARXIV)
    >>> keep_prolific_authors(arxiv_copy, 2)
    >>> len(arxiv_copy)
    3
    >>> '108' in arxiv_copy and '5090' in arxiv_copy and '0001' in arxiv_copy
    True
    >>> arxiv_copy = copy.deepcopy(EXAMPLE_ARXIV)
    >>> keep_prolific_authors(arxiv_copy, 3)
    >>> arxiv_copy
    {}
    """
    # We have provided you with this docstring as an example of how to use 
    # the function copy.deepcopy in docstring examples for functions that
    # modify an argument.

    # TODO write the body of the function here
    
    prolific = {}
    author_to_articles = make_author_to_articles(id_to_article)
    
    for key in id_to_article:
        if has_prolific_authors(author_to_articles, id_to_article[key],
           min_publications):
            prolific[key] = id_to_article[key]
    
    id_to_article.clear()
    
    id_to_article.update(prolific)
    
    
if __name__ == '__main__':
    pass  # do not delete or comment out this line

    # uncomment the lines below to run doctest on your code
    # note that doctest requires your docstring examples to be perfectly
    # formatted, and we will not be running doctest on your code
    # import doctest
    # doctest.testmod()

    # uncomment the lines below to work with the small data set
    # example_data = open('example_data.txt')
    # example_arxiv = read_arxiv_file(example_data)
    # example_data.close()
    # if example_arxiv == EXAMPLE_ARXIV:
        # print('The dict returned by read_arxiv_file matches EXAMPLE_ARXIV!')
        # print('This is a good sign, but do more of your own testing!')
    # else:
       # If you are getting this message, try setting a breakpoint on the line
       # that calls read_arxiv_file above and running the debugger
       # print('Not quite! You got:')
       # pprint.pprint(example_arxiv)
       # print()
       # print('If you are getting this message, then the dictionary produced')
       # print('by your read_arxiv_file function does not match the provided')
       # print('EXAMPLE_ARXIV. Scroll up to see the dictionary your function')
       # print('produced. You may want to write more testing code to help')
       # print('figure out why it does not match.')


    # uncomment the lines below to work with a larger data set
    # large_file = open('data.txt')
    # large_data = read_arxiv_file(large_file)
    # large_file.close()

    # auth_to_articles = make_author_to_articles(large_data)
    # most_published_authors = get_most_published_authors(large_data)
    # print(most_published_authors)
    # print(get_coauthors(large_data, ('Varanasi', 'Mahesh K.')))  # one
    # print(get_coauthors(large_data, ('Chablat', 'Damien')))  # many
