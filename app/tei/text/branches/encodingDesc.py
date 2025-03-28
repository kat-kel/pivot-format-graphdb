from lxml import etree
from app.models.data import GenreModel
from app.models.data import TextDataModel
from app.constants import XML_ID
from app.tei.text import TextTree


class GenreTaxonomy:
    """Class to manage metadata for 'taxonomy/category[@xml:id="genre"]' node \
        in 'teiHeader/encodingDesc/classDecl/taxonomy' branch."""

    @staticmethod
    def sort_genres(genre: GenreModel) -> list[GenreModel]:
        """Unnest the potentially nested genealogy of the text's genre and return a \
            flat list of genres ordered by seniority, with the eldest parent first.

        Args:
            genre (GenreModel): Genre data model.

        Returns:
            list[GenreModel]: List of genre data models; first is the eldest parent.
        """

        reverse_genre_genealogy = [genre]

        def has_parent(genre: GenreModel) -> bool:
            if genre.parent_genre:
                return True
            else:
                return False

        # Recursively go through the genre's parents
        current_genre = genre
        while has_parent(current_genre):
            current_genre = current_genre.parent_genre
            reverse_genre_genealogy.append(current_genre)

        return list(reversed(reverse_genre_genealogy))

    @staticmethod
    def make_genre_category(genre: GenreModel) -> etree.Element:
        """Build a new 'category' branch for a genre entity.

        <category xml:id="genre_ID">
          <catDesc>Genre name</catDesc>
        </category>

        Args:
            genre (GenreModel): Data model for a genre.

        Returns:
            etree.Element: Small branch of a new 'category' element.
        """

        category_node = etree.Element("category")
        category_node.set(XML_ID, genre.xml_id)
        catDesc_node = etree.SubElement(category_node, "catDesc")
        catDesc_node.text = genre.preferred_name
        return category_node

    @classmethod
    def build_category_tree(cls, genre: GenreModel) -> etree.Element:
        """Build a potentially nested tree of genre 'category' branches.

        <category xml:id="genre_1">
            <catDesc>---Parent genre---</catDesc>
            <category xml:id"genre_2">
                <catDesc>---Child genre---</catDesc>
            </category>
        </category>

        Args:
            genre (GenreModel): Text's genre, which might have parents.

        Returns:
            etree.Element: Small tree of 'category' and its decsending nodes.
        """

        genre_genealogy = cls.sort_genres(genre=genre)

        # Create the most senior node
        parent_genre = genre_genealogy[0]
        base_node = cls.make_genre_category(genre=parent_genre)

        # If the genre has children, insert them
        if len(genre_genealogy) > 1:
            parent_node = base_node
            for genre in genre_genealogy[1:]:
                node = cls.make_genre_category(genre=genre)
                parent_node.append(node)
                parent_node = node

        return base_node

    @classmethod
    def insert_nodes(cls, genre: GenreModel | None, tree: TextTree) -> None:
        """If the text has a genre, insert the genre's 'category' tree into the branch \
            of the encodingDesc.

        Args:
            genre (GenreModel | None): Text's genre, which might have parents.
            tree (TextTree): Tree parser for the text's TEI document.
        """

        if genre:
            genre_nodes = cls.build_category_tree(genre=genre)
            parent_node = tree.encodingDesc.genre_taxonomy
            parent_node.append(genre_nodes)


class EncodingDesc:
    """Class to manage construction of nodes in 'teiHeader/encodingDesc' branch."""

    @classmethod
    def insert_data(cls, text: TextDataModel | None, tree: TextTree) -> None:
        """Transform the text data model's metadata into the elements in the \
            'teiHeader/encodingDesc' branch and insert them into the tree.

        Args:
            text (TextDataModel): Text data model.
            tree (TextTree): Tree parser for the text's TEI document.
        """

        # Add genre categories to the taxonomy branch
        GenreTaxonomy.insert_nodes(genre=text.genre, tree=tree)
