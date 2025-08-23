from django import forms
from .models import Category,Listing,Bid,Comment

class CategoriesForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            "name": "Category",
        }
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full border border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": "Enter product Category"})}
        def clean_name(self):
            name = self.cleaned_data['name']
        # Just return the name without checking uniqueness
            return name



class ListingsForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'
        exclude = ['winner', 'active', 'user', 'category']
        labels = {
            "img": "Image",   # <-- custom label
            "desc": "Description",  # optional nicer name
        }
        widgets = {
            "item_no": forms.TextInput(attrs={
                "class": "w-full border border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": "Enter product item no"}),
            "title": forms.TextInput(attrs={
                "class": "w-full border border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": "Enter product title"
            }),
            "desc": forms.Textarea(attrs={
                "class": "w-full border border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "rows": 4,
                "placeholder": "Write a short description..."
            }),
            
            "img": forms.URLInput(attrs={
                "class": "w-full border border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500",
                 "placeholder": "Enter image URL"
            }),

        }

        
class BidsForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = '__all__'
        exclude = ['listing','bidder','cur_bid']
        widgets = {
            "start_bid": forms.NumberInput(attrs={
                "class": "w-full border border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": "Enter starting bid"
            })}


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
        "comment": forms.Textarea(attrs={
                "class": "w-full border border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "rows": 4,
                "placeholder": "Write a Comment..."
            })}
 