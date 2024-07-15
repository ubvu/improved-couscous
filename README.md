# improved-couscous
dashboard for UNL

This has been built from a simple query: 

https://api.openalex.org/works?page=1&filter=authorships.institutions.lineage:i865915315,publication_year:2022,type:types/article,is_retracted:false 


list with all universities, but without academic hospitals or other institutions:

https://api.openalex.org/works?page=1&filter=authorships.institutions.lineage:i865915315|i887064364|i121797337|i98358874|i913958620|i193700539|i83019370|i34352273|i145872427|i913481162|i193662353|i94624287|i169381384,publication_year:2022,type:types/article,is_retracted:false 

add your own email address in the scope_file to get on the nice list.
