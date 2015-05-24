ComeBebeSP
==========

This project targets São Paulo restaurants for a food-gathering effort by a
partner NGO. It can, of course, be useful for any other project. Requests for
more sites will be considered, please open an Issue.


Installing and running Scrapy
-----------------------------

This project uses the pre-release Scrapy 1.0 Release Candidate. Installing it
on a Python development environment (with lxml, libxslt and libssl as per
[scrapy docs][install scrapy]) should be easy from a checkout of this project:

    pip install -r requirements.txt

It also needs `scrapylib` and `purl`, declared in requirements.txt.


Running the crawlers
--------------------

From a checkout of the project, run:

    scrapy crawl vejasp -t csv -o vejasp.csv

If you're fixing or improving the project and need to run the crawls several
times, you will benefit from using the built-in http cache: 

    scrapy crawl --set=HTTPCACHE_ENABLED=1 vejasp -t csv -o vejasp.csv

Of course, you can substitute `vejasp` for any of the other spiders. Right now
we got these:

- `vejasp` => crawls http://vejasp.abril.com.br
- `baresp` => crawls http://baressp.com.br

Keep in mind Scrapy supports not only CSV but also JSON, XML and others (see
[exporters docs][scrapy exporters]).

[install scrapy]: http://doc.scrapy.org/en/1.0/intro/install.html#installing-scrapy
[scrapy exporters]: http://doc.scrapy.org/en/1.0/topics/exporters.html
