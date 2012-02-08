# Case Conductor is a Test Case Management system.
# Copyright (C) 2011-2012 Mozilla
#
# This file is part of Case Conductor.
#
# Case Conductor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Case Conductor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Case Conductor.  If not, see <http://www.gnu.org/licenses/>.
"""
Manage views for cases.

"""
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

from .... import model

from ...lists import decorators as lists
from ...utils.ajax import ajax

from ..finders import ManageFinder

from .filters import ProductFilterSet
from . import forms



@login_required
@lists.actions(
    model.Product,
    ["delete", "clone"],
    permission="core.manage_products")
@lists.finder(ManageFinder)
@lists.filter("products", filterset_class=ProductFilterSet)
@lists.sort("products")
@ajax("manage/product/_products_list.html")
def products_list(request):
    """List products."""
    return TemplateResponse(
        request,
        "manage/product/products.html",
        {
            "products": model.Product.objects.all(),
            }
        )



@login_required
def product_details(request, product_id):
    """Get details snippet for a product."""
    product = get_object_or_404(model.Product, pk=product_id)
    return TemplateResponse(
        request,
        "manage/product/_product_details.html",
        {
            "product": product
            }
        )



@permission_required("core.manage_products")
def product_add(request):
    """Add a single case."""
    if request.method == "POST":
        form = forms.ProductForm(request.POST, user=request.user)
        if form.is_valid():
            product = form.save()
            messages.success(
                request, "Product '{0}' added.".format(
                    product.name)
                )
            return redirect("manage_products")
    else:
        form = forms.ProductForm(user=request.user)
    return TemplateResponse(
        request,
        "manage/product/add_product.html",
        {
            "form": form
            }
        )



@permission_required("core.manage_products")
def product_edit(request, product_id):
    """Edit a product."""
    product = get_object_or_404(model.Product, pk=product_id)
    if request.method == "POST":
        form = forms.ProductForm(
            request.POST, instance=product, user=request.user)
        if form.is_valid():
            cv = form.save()
            messages.success(request, "Saved '{0}'.".format(cv.name))
            return redirect("manage_products")
    else:
        form = forms.ProductForm(instance=product, user=request.user)
    return TemplateResponse(
        request,
        "manage/product/edit_product.html",
        {
            "form": form,
            "product": product,
            }
        )
