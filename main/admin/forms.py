from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from home.models import BaseSettings, HomeTemplate, Stock
from service.models import Service
from reviews.models import Reviews
from shop.models import Categories, Day, Product, Subsidiary

# class ProductForm(forms.ModelForm):
#   # description = forms.CharField(label="Полное описание товара", required=False, widget=CKEditorUploadingWidget())
#   class Meta:
#     model = Product
#     fields = (
#       "name", 
#       "short_description",
#       "description",
#       "meta_h1",
#       "meta_title",
#       "meta_description",
#       "meta_keywords",
#       "slug",
#       "price",
#       "discount",
#       "quantity",
#       "category",
#       "day",
#       "subsidiary",
#       "weight",
#       )
class GlobalSettingsForm(forms.ModelForm):
  """ Form, глобальные и общие настройки сайта(лого, телефон, email)"""
  # description = forms.CharField(label='Полное описание товара', required=False, widget=CKEditorUploadingWidget())
  class Meta:
    model = BaseSettings
    fields = [
        'logo',
        'phone_one',
        'phone_two',
        'time_work',
        'email',
        'address_one',
        'address_two',
        'meta_h1',
        'meta_title',
        'meta_description',
        'meta_keywords',
    ]
    labels = {
        'logo': 'Логотип',
        'phone_one': 'Номер телефона Пролетарская',
        'phone_two': 'Номер телефона Ракетная',
        'time_work': 'Режим работы',
        'email': 'Email',
        'address_one': 'Адрес Пролетарская',
        'address_two': 'Адрес Ракетная',
        'meta_h1':'Заголвок первого уровня',
        'meta_title':'Meta title',
        'meta_description':'Мета description',
        'meta_keywords':'Meta keywords',
    }
    widgets = {
        'phone_one': forms.TextInput(attrs={
            'class': 'form__controls'
        }),
        'phone_one': forms.TextInput(attrs={
            'class': 'form__controls'
        }),
        'phone_two': forms.TextInput(attrs={
            'class': 'form__controls'
        }),
        'time_work': forms.TextInput(attrs={
            'class': 'form__controls'
        }),
        'email': forms.EmailInput(attrs={
            'class': 'form__controls'
        }),
        'address_one': forms.TextInput(attrs={
            'class': 'form__controls'
        }),
        'address_two': forms.TextInput(attrs={
            'class': 'form__controls'
        }),
        'meta_h1': forms.TextInput(attrs={
            'class': 'form__controls'
        }),
        'meta_title': forms.TextInput(attrs={
            'class': 'form__controls'
        }),
        'meta_description': forms.TextInput(attrs={
            'class': 'form__controls'
        }),
        'meta_keywords': forms.TextInput(attrs={
            'class': 'form__controls'
        })
    }
    
class ProductForm(forms.ModelForm):
    """ Form, отвечает за создание товара и редактирование товара"""
    # description = forms.CharField(label='Полное описание товара', required=False, widget=CKEditorUploadingWidget())
    
    class Meta:
        model = Product
        fields = [
            'name',
            'slug',
            'short_description',
            'description',
            'meta_h1',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'image',
            'price',
            'discount',
            'quantity',
            'category',
            'day',
            'subsidiary',
            'image',
            'weight',
            'calories',
            'proteins',
            'fats',
            'carbonhydrates',
            'status',
        ]
        labels = {
            'name': 'Название блюда',
            'slug':'URL',
            'short_description':'Короткое описание',
            'description':'Полное описание',
            'meta_h1':'Заголвок первого уровня',
            'meta_title':'Meta title',
            'meta_description':'Мета description',
            'meta_keywords':'Meta keywords',
            'image':'Изображение',
            'price':'Цена',
            'discount':'Скидка в (%)',
            'quantity':'Количество',
            'category':'Категория',
            'day':'В какой день готовят',
            'subsidiary':'В каком из филлиалов',
            'image': 'Превью изображения',
            'weight':'Грамовка',
            'calories': 'Каллорийность',
            'proteins': 'Белки',
            'fats': 'Жиры',
            'carbonhydrates': 'Углеводы',
            'status': 'Статус публикации'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form__controls',
                "id":"name"
                # 'placeholder': 'Название товара',
                
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form__controls',
                # 'placeholder': 'Короткое описание товара',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form__controls',
                # 'placeholder': 'Короткое описание товара',
            }),
            'meta_h1': forms.TextInput(attrs={
                'class': 'form__controls',
                # 'placeholder': 'h1',
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'form__controls',
                # 'placeholder': 'Мета заголовок',
            }),
            'meta_description': forms.TextInput(attrs={
                'class': 'form__controls',
                # 'placeholder': 'Мета описание',
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'form__controls',
                # 'placeholder': 'Ключевые слова',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form__controls',
                # 'placeholder': 'Цена (с учетом скидки)',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form__controls',
                # 'placeholder': 'Количество',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form__controls',
                "id": "slug"
                # 'placeholder': 'SEO URL',
            }),
            'category': forms.Select(attrs={
                'class': 'form__controls', 
                # 'placeholder': 'Категория',
            }),
            # 'day': forms.Select(attrs={
            #     'class': 'form__controls',
            #     # 'placeholder': 'День приготовления',
            # }),
            # 'subsidiary': forms.Select(attrs={
            #     'class': 'form__controls',
            #     'placeholder': 'Филлиал',
            #     'multiply': True
            # }),
            'weight': forms.TextInput(attrs={
                'class': 'form__controls',
                # 'placeholder': 'Грамовка',
            }),
            'discount': forms.TextInput(attrs={
                'class': 'form__controls',
                # 'placeholder': 'Скидка',
            }),
            'image': forms.FileInput(attrs={
                'class': 'submit-file',
                'accept': 'image/*'
            }),
            'calories': forms.TextInput(attrs={
                'class': "form__controls",
                # 'placeholder': 'Колорийность'
            }),
            'proteins': forms.TextInput(attrs={
                'class': "form__controls",
                # 'placeholder': 'Белки'
            }),
            'fats': forms.TextInput(attrs={
                'class': "form__controls",
                # 'placeholder': 'Жиры'
            }),
            'carbonhydrates': forms.TextInput(attrs={
                'class': "form__controls",
                # 'placeholder': 'Углеводы'
            }),
            # 'status': forms.CheckboxInput(attrs={
            #     'class': "form__controls-checkbox",
            #     'placeholder': 'Белки'
            # })
        }
   
class CategoryForm(forms.ModelForm):
  """ Form, отвечает за создание категорий и редактирование категорий"""
  class Meta:
    model = Categories
    fields = [
      "name",
      "slug",
      "image",
      "meta_h1",
      "meta_title",
      "meta_description",
      "meta_keywords"
    ]
    labels = {
      "name": "Назване категории",
      "slug": "URL",
      "image": "Изображение",
      "meta_h1": "Заголовок H1",
      "meta_title": "Meta заголовок",
      "meta_description": "Meta описание",
      "meta_keyword": "Meta keywords",
    }
    widgets = {
      "name": forms.TextInput(attrs={
          "class": "form__controls",
          "id":"name"
          # "placeholder": "Название  категории"
      }),
      "slug": forms.TextInput(attrs={
        "class":"form__controls",
        "id": "slug"
        # "placeholder": "Название категори"
      }),
      'image': forms.FileInput(attrs={
          'class': 'submit-file',
          'accept': 'image/*'
      }),
      "meta_h1": forms.TextInput(attrs={
        "class":"form__controls",
        # "placeholder": "Заголовок H1"
      }),
      "meta_title": forms.TextInput(attrs={
        "class":"form__controls meta_field",
        "id": "meta_title"
        # "placeholder": "Meta заголовок"
      }),
      "meta_description": forms.Textarea(attrs={
        "class":"form__controls meta_field",
        # "placeholder": "Meta Описание",
        "rows": "5"
      }),
      "meta_keywords": forms.TextInput(attrs={
        "class":"form__controls",
        # "placeholder": "Meta keywords"
      }),  
    }
    
class DayForm(forms.ModelForm):
  """ Form, отвечает за создание дней и редактирование дней"""
  class Meta:
    model = Day
    fields = [
      "name",
      "slug"
    ]
    labels = {
      "name": "Назване категории",
      "slug": "URL",
    }
    widgets = {
      "name": forms.TextInput(attrs={
          "class": "form__controls",
          "id":"name"
          # "placeholder": "Название  категории"
      }),
      "slug": forms.TextInput(attrs={
        "class":"form__controls",
        "id": "slug"
        # "placeholder": "Название категори"
      })
    }
    
class FillialForm(forms.ModelForm):
  """ Form, отвечает за добавление филлиала и редактирование филлиала"""
  class Meta:
    model = Subsidiary
    fields = [
      "name",
      "address_fillial",
      "image",
      "slug"
    ]
    labels = {
      "name": "Название филлиала",
      "address_fillial": "Адрес филлиала",
      "image": "Фотография зала",
      "slug": "URL",
    }
    widgets = {
      "name": forms.TextInput(attrs={
          "class": "form__controls",
          "id":"name"
      }),
      "address_fillial": forms.TextInput(attrs={
          "class": "form__controls",
          "id":"name",
          "placeholder": "г.Томск, ул.Ленина 111"
      }),
      "slug": forms.TextInput(attrs={
        "class":"form__controls",
        "id": "slug"
      })
    }
    
class HomeTemplateForm(forms.ModelForm):
  """ Form, редактирование главной страницы"""
  # description = forms.CharField(label='Полное описание товара', required=False, widget=CKEditorUploadingWidget())
  
  class Meta:
      model = HomeTemplate
      fields = [
          'banner',
          'meta_h1',
          'untitle',
          'meta_title',
          'meta_description',
          'meta_keywords',
          'about_text',
          'about_image'
      ]
      labels = {
          'banner': 'Изображение банера',
          'meta_h1':'Заголвок первого уровня',
          'meta_title':'Meta title',
          'untitle': 'Надзаголовок',
          'meta_description':'Мета description',
          'meta_keywords':'Meta keywords',
          'about_text':'Текст о нас',
          'about_image':'Изображение о нас'
      }
      widgets = {
          'name': forms.TextInput(attrs={
              'class': 'form__controls'
          }),
          'meta_h1': forms.TextInput(attrs={
              'class': 'form__controls',
          }),
          'untitle': forms.TextInput(attrs={
              'class': 'form__controls',
          }),
          'meta_title': forms.TextInput(attrs={
              'class': 'form__controls',
              # 'placeholder': 'Мета заголовок',
          }),
          'meta_description': forms.TextInput(attrs={
              'class': 'form__controls',
              # 'placeholder': 'Мета описание',
          }),
          'meta_keywords': forms.TextInput(attrs={
              'class': 'form__controls',
          }),
          'about_text': forms.TextInput(attrs={
              'class': 'form__controls',
          }),
      }
           
class ReviewsForm(forms.ModelForm):
  """ Form, добавление и редактирование отзыва"""
  # description = forms.CharField(label='Полное описание товара', required=False, widget=CKEditorUploadingWidget())
  
  class Meta:
    model = Reviews
    fields = [
        'avatar',
        'name',
        'slug',
        'date',
        'text',
        'status',
        'meta_h1',
        'meta_title',
        'meta_description',
        'meta_keywords',
    ]
    labels = {
        'avatar': 'Фотография пользователя',
        'name':'ФИО пользователя',
        'slug': 'URL',
        'date':'Дата коментария',
        'text':'Текст коментария',
        'status':'Статус публикации',
        'meta_h1':'Заголвок первого уровня',
        'meta_title':'Meta title',
        'untitle': 'Надзаголовок',
        'meta_description':'Мета description',
        'meta_keywords':'Meta keywords',
    }
    widgets = {
      'name': forms.TextInput(attrs={
        'class': 'form__controls',
        'id': 'name'
      }),
      'slug': forms.TextInput(attrs={
        'class':'form__controls',
        "id": "slug"
      }),
      'date': forms.DateInput(attrs={
        'class':'form__controls',
      }),
      'text': forms.Textarea(attrs={
        'class': 'form__controls',
        'rows': 5,
      }),
      'status': forms.CheckboxInput(attrs={
        'class': 'form__controls-checkbox',
      }),
      'meta_h1': forms.TextInput(attrs={
        'class': 'form__controls',
      }),
      'meta_title': forms.TextInput(attrs={
        'class': 'form__controls',
      }),
      'meta_description': forms.Textarea(attrs={
        'class': 'form-controls',
        'rows': 5,
      }),
      'meta_keywords': forms.TextInput(attrs={
        'class': 'form__controls'
      })
    }
    
class StockForm(forms.ModelForm):
  """ Form, добавление и редактирование акций"""
  # description = forms.CharField(label='Полное описание товара', required=False, widget=CKEditorUploadingWidget())
  
  class Meta:
    model = Stock
    fields = [
        'title',
        'slug',
        'description',
        'validity',
        'status',
        'image',
        'meta_title',
        'meta_description',
        'meta_keywords',
    ]
    labels = {
        'title':'Название акции',
        'slug': 'URL',
        'validity':'Срок действия акции',
        'description':'Текст коментария',
        'status':'Статус публикации',
        'image': 'Изображение акции',
        'meta_title':'Meta title',
        'untitle': 'Надзаголовок',
        'meta_description':'Мета description',
        'meta_keywords':'Meta keywords',
    }
    widgets = {
      'title': forms.TextInput(attrs={
        'class': 'form__controls',
        'id': 'name'
      }),
      'slug': forms.TextInput(attrs={
        'class':'form__controls',
        "id": "slug"
      }),
      'validity': forms.DateInput(attrs={
        'class':'form__controls',
      }),
      'description': forms.Textarea(attrs={
        'class': 'form__controls',
        'rows': 5,
      }),
      'status': forms.CheckboxInput(attrs={
        'class': 'form__controls-checkbox',
      }),
      'meta_title': forms.TextInput(attrs={
        'class': 'form__controls',
      }),
      'meta_description': forms.Textarea(attrs={
        'class': 'form-controls',
        'rows': 5,
      }),
      'meta_keywords': forms.TextInput(attrs={
        'class': 'form__controls'
      })
    }
    
    
class ServiceForm(forms.ModelForm):
  """ Form, добавление и редактирование услуг"""
  # description = forms.CharField(label='Полное описание товара', required=False, widget=CKEditorUploadingWidget())
  
  class Meta:
    model = Service
    fields = [
        'name',
        'slug',
        'subtitle',
        'status',
        'image',
        'meta_title',
        'meta_description',
        'meta_keywords',
    ]
    labels = {
        'name':'Название',
        'slug': 'URL',
        'subtitle':'Текст под заголовком',
        'status':'Статус публикации',
        'image': 'Изображение акции',
        'meta_title':'Meta title',
        'untitle': 'Надзаголовок',
        'meta_description':'Мета description',
        'meta_keywords':'Meta keywords',
    }
    widgets = {
      'name': forms.TextInput(attrs={
        'class': 'form__controls',
        'id': 'name'
      }),
      'slug': forms.TextInput(attrs={
        'class':'form__controls',
        "id": "slug"
      }),
      'subtitle': forms.DateInput(attrs={
        'class':'form__controls',
      }),
      'status': forms.CheckboxInput(attrs={
        'class': 'form__controls-checkbox',
      }),
      'meta_title': forms.TextInput(attrs={
        'class': 'form__controls',
      }),
      'meta_description': forms.Textarea(attrs={
        'class': 'form-controls',
        'rows': 5,
      }),
      'meta_keywords': forms.TextInput(attrs={
        'class': 'form__controls'
      })
    }