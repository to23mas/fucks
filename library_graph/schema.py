import graphene

from graphene_django import DjangoObjectType
from library_rest.models import Book 

# Definice typu Book pro GraphQL
# - DjangoObjectType: převádí Django model na GraphQL typ
# - fields: specifikuje, která pole modelu budou dostupná v GraphQL
class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'isbn', 'pages', 'published_date', 'created_at', 'updated_at')

# Definice GraphQL dotazů (queries)
# - all_books: vrací seznam všech knih
# - book: vrací jednu knihu podle ID
class Query(graphene.ObjectType):
    all_books = graphene.List(BookType)
    book = graphene.Field(BookType, id=graphene.Int())

    # Resolver pro získání všech knih
    def resolve_all_books(self, info):
        return Book.objects.all()

    # Resolver pro získání jedné knihy podle ID
    def resolve_book(self, info, id):
        return Book.objects.get(pk=id)

# Mutace pro vytvoření nové knihy
# - Arguments: definuje povinné parametry pro vytvoření knihy
# - book: vrací vytvořenou knihu
class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)
        isbn = graphene.String(required=True)
        pages = graphene.Int(required=True)
        published_date = graphene.String(required=True)

    book = graphene.Field(BookType)

    # Metoda pro vytvoření nové knihy
    def mutate(self, info, title, author, isbn, pages, published_date):
        book = Book.objects.create(
            title=title,
            author=author,
            isbn=isbn,
            pages=pages,
            published_date=published_date
        )
        return CreateBook(book=book)

# Mutace pro aktualizaci existující knihy
# - Arguments: definuje ID knihy a volitelné parametry pro aktualizaci
# - book: vrací aktualizovanou knihu
class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        author = graphene.String()
        isbn = graphene.String()
        pages = graphene.Int()
        published_date = graphene.String()

    book = graphene.Field(BookType)

    # Metoda pro aktualizaci knihy
    # - **kwargs: umožňuje aktualizovat pouze zadaná pole
    def mutate(self, info, id, **kwargs):
        book = Book.objects.get(pk=id)
        for key, value in kwargs.items():
            if value is not None:
                setattr(book, key, value)
        book.save()
        return UpdateBook(book=book)

# Mutace pro smazání knihy
# - Arguments: definuje ID knihy ke smazání
# - success: vrací boolean indikující úspěch operace
class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    # Metoda pro smazání knihy
    # - try/except: ošetření případu, kdy kniha neexistuje
    def mutate(self, info, id):
        try:
            Book.objects.get(pk=id).delete()
            return DeleteBook(success=True)
        except Book.DoesNotExist:
            return DeleteBook(success=False)

# Registrace všech mutací
class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()

# Vytvoření GraphQL schématu
# - query: registrace dotazů
# - mutation: registrace mutací
schema = graphene.Schema(query=Query, mutation=Mutation) 
