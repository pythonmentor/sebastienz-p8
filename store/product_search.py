from .models import Products, Categories


class ProductSearch:

    @classmethod
    def found_substitutes(cls, product_id):
        # find product in DB
        product = Products.objects.get(pk=product_id)
        # find all products (substitutes) which are in same categories as initial product
        substitutes_ids_list = []
        dic = {}
        # List all substitutes in all common categories with better nutrition grade
        for cat in product.categories.all():
            substitutes_ids_list.extend([prod.id for prod in Products.objects.
                                        filter(categories__name=cat).
                                        filter(nutrition_grade_fr__lt=product.nutrition_grade_fr)
                                        .order_by('nutrition_grade_fr')])
            # Put temporarily each unique substitutes ids from list in dic,
        # with number of common instance with other categories
        if len(substitutes_ids_list) > 0:
            for sub_id in substitutes_ids_list:
                if sub_id not in dic:
                    dic[sub_id] = substitutes_ids_list.count(sub_id)

        sorted_id_list = [key[0] for key in sorted(dic.items(), key=lambda x: x[1], reverse=True)]

        # return the best substitutes from dictionnary and return them in queryset
        # Define ordering to preserve list order
        SQL_clauses = ' '.join(['WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(sorted_id_list)])
        ordering = 'CASE %s END' % SQL_clauses
        return Products.objects.filter(id__in=sorted_id_list).extra(
            select={'ordering': ordering}, order_by=('ordering',))
