from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category
from .forms import PostForm, CategoryForm


# Zobrazení seznamu všech příspěvků
# Umožňuje filtrování podle kategorií pomocí GET parametru
# Řazeno od nejnovějších podle data vytvoření
def post_list(request):
	# Načtení všech příspěvků seřazených podle data vytvoření (sestupně)
	posts = Post.objects.all().order_by("-created_at")
	# Načtení všech kategorií pro filtrování
	categories = Category.objects.all()
	# Získání kategorie z URL parametru pro filtrování
	category_filter = request.GET.get("category")

	# Pokud je vybrána kategorie, filtrujeme příspěvky
	if category_filter:
		posts = posts.filter(categories__id=category_filter)

	# Renderování šablony s příspěvky a kategoriemi
	return render(request, "blog/post_list.html", {
		"posts": posts,
		"categories": categories,
	})

# Detail konkrétního příspěvku podle jeho ID
# Pokud příspěvek neexistuje, vrátí 404 (HTTP status kód pro "Stránka nenalezena")
# 404 je standardní HTTP odpověď, která říká uživateli že požadovaný obsah nebyl nalezen
# Například když uživatel zadá ID příspěvku který neexistuje nebo byl smazán
def post_detail(request, pk):
	# Načtení příspěvku nebo 404 pokud neexistuje
	# get_object_or_404 se pokusí najít příspěvek s daným ID
	# Pokud příspěvek nenajde, automaticky vyvolá HTTP 404 odpověď
	# Tím se zobrazí uživateli přívětivá chybová stránka místo systémové chyby
	post = get_object_or_404(Post, pk=pk)
	return render(request, "blog/post_detail.html", {"post": post})

# Vytvoření nového příspěvku
# Zpracovává jak GET (zobrazení formuláře) tak POST (uložení dat)
# Po úspěšném vytvoření přesměruje na seznam příspěvků
def post_create(request):
	if request.method == "POST":
		# Vytvoření formuláře s daty z POST requestu
		form = PostForm(request.POST)
		if form.is_valid():
			# Uložení dat z formuláře
			form.save()
			# Přesměrování na seznam příspěvků
			return redirect("blog:post_list")
	else:
		# Vytvoření prázdného formuláře pro GET request
		form = PostForm()
	return render(request, "blog/post_form.html", {"form": form})

# Úprava existujícího příspěvku
# Po úspěšné editaci přesměruje zpět na editační formulář
# Pokud příspěvek neexistuje, vrátí 404
def post_edit(request, pk):
	# Načtení existujícího příspěvku nebo 404
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		# Vytvoření formuláře s daty z POST requestu a existujícím příspěvkem
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			# Uložení upravených dat
			form.save()
			# Přesměrování zpět na editaci
			return redirect("blog:post_edit", pk=post.pk)
	else:
		# Předvyplnění formuláře daty z existujícího příspěvku
		form = PostForm(instance=post)
	return render(request, "blog/post_form.html", {
		"form": form,
		"post": post,
	})

# Smazání příspěvku a přesměrování na seznam
# Pokud příspěvek neexistuje, vrátí 404
def post_delete(request, pk):
	# Načtení a smazání příspěvku
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	# Přesměrování na seznam příspěvků
	return redirect("blog:post_list")


def category_list(request):
	# Načtení všech kategorií
	categories = Category.objects.all()
	return render(request, "blog/category_list.html", {
		"categories": categories,
	})

# Detail kategorie podle jména
# Pokud kategorie neexistuje, vrátí 404
def category_detail(request, pk):
	# Načtení kategorie podle jména nebo 404
	category = get_object_or_404(Category, name=pk)
	return render(request, "blog/category_detail.html", {"category": category})

# Vytvoření nové kategorie
# Po vytvoření přesměruje na editaci této kategorie
# Zobrazuje také seznam všech existujících kategorií
def category_create(request):
	if request.method == "POST":
		# Zpracování dat z formuláře
		form = CategoryForm(request.POST)
		if form.is_valid():
			# Uložení nové kategorie
			category = form.save()
			# Přesměrování na editaci nově vytvořené kategorie
			return redirect("blog:category_edit", category.id)
	else:
		# Prázdný formulář pro novou kategorii
		form = CategoryForm()

	# Načtení všech kategorií pro zobrazení v šabloně
	categories = Category.objects.all()
	return render(request, "blog/category_form.html", {
		"form": form,
		"categories": categories,
	})

# Úprava existující kategorie podle ID
# Po úspěšné editaci zůstává na stejné stránce
# Pokud kategorie neexistuje, vrátí 404
def category_edit(request, pk):
	# Načtení kategorie podle ID
	category = get_object_or_404(Category, pk=pk)
	print(category)  # Debug výpis pro kontrolu načtené kategorie
	if request.method == "POST":
		# Formulář s daty z POST a existující kategorií
		form = CategoryForm(request.POST, instance=category)
		if form.is_valid():
			# Uložení změn
			form.save()
			# Přesměrování zpět na editaci
			return redirect("blog:category_edit", pk=category.id)
	else:
		# Předvyplnění formuláře daty existující kategorie
		form = CategoryForm(instance=category)
	return render(request, "blog/category_form.html", {
		"form": form,
		"category": category,
	})

# Smazání kategorie a přesměrování na seznam kategorií
# Pokud kategorie neexistuje, vrátí 404
def category_delete(request, pk):
	# Načtení a smazání kategorie
	category = get_object_or_404(Category, pk=pk)
	category.delete()
	# Přesměrování na seznam kategorií
	return redirect("blog:category_list")
