# hanzi-trees
A set of tools for in-depth search and analysis of Chinese characters based on their internal structure

This website presents a set of tools for working with Chinese characters based on the classification of some 10,000 Chinese characters done by my father Boris Klimenko. The classification is built on analysis of the internal structure of each character and break-up of complex characters into two immediate components. Many characters are then grouped together on the basis of having the same common component. The latter is labeled as a root, while all characters derived from the root comprise its tree. This method of character classification and its results are presented in more detail on the About page of the website.

The tools include the following:
* Search by character
* Character search by structure elements
* Tree search by root structure
* Character search by meaning

What I learned:
* MySQL (ended up using SQLite due to unexpected issues with character rendering when using MySQL)
* Watch out for capability of different SQLAlchemy versions to render CJK Ext B (rare/archaic characters) properly
* Make a virtual keyboard of Chinese radicals with JavaScript


