from django import forms
from home.models import BaseSettings, HomeTemplate, Messanger, SliderHome, Stock
from coupons.models import Coupon
from service.models import Service
from reviews.models import Reviews
from shop.models import Category, CharGroup, CharName, Product, ProductChar, ProductImage, ShopSettings
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# from ckeditor.widgets import CKEditorWidget
class UploadFileForm(forms.Form):
    file = forms.FileField()


class GlobalSettingsForm(forms.ModelForm):
  """ Form, глобальные и общие настройки сайта(лого, телефон, email)"""
  # description = forms.CharField(label='Полное описание товара', required=False, widget=CKEditorUploadingWidget())
  class Meta:
    model = BaseSettings
    fields = [
        'logo',
        'phone',
        'time_work',
        'email',
        'address',
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
        'phone': forms.TextInput(attrs={
            'class': 'form__controls'
        }),
        'time_work': forms.TextInput(attrs={
            'class': 'form__controls'
        }),
        'email': forms.EmailInput(attrs={
            'class': 'form__controls'
        }),
        'address': forms.TextInput(attrs={
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
    description = forms.CharField(label='Полное описание товара', required=False, widget=CKEditorUploadingWidget())
    # description = RichTextUploadingField()
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form__controls',
                "id":"name"
                # 'placeholder': 'Название товара',
                
            }), 
            # 'description': forms.Textarea(attrs={
            #     'class': 'form__controls',
            #     # 'placeholder': 'Короткое описание товара',
            # }),
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
            'sale_price': forms.NumberInput(attrs={
                'class': 'form__controls',
                # 'placeholder': 'Цена (с учетом скидки)',
            }),
            'quantity_purchase': forms.NumberInput(attrs={
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
            'category': forms.CheckboxSelectMultiple,
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
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage

        fields = [
            'parent',
            'src'
        ]
        labels = {
            'src': 'Выбрать изображение'
        }
        widgets = {
            'parent': forms.Select(attrs={
                'class': 'form__controls', 
            })
        }

class ProductCharForm(forms.ModelForm):
    class Meta:
        model = ProductChar
        fields = [
            'char_name',
            'char_value',
        ]
        labels = {
            'char_name': 'Название характеристики',
            'char_value': 'Значение',
        }
        widgets = {
            'char_name': forms.Select(attrs={
                'class': 'form__controls',
                'placeholder': 'Название характеристики',
                'id': 'id_char_name',
               
            }),
            'char_value': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
                'id': 'id_char_value'
            }),
        }

class CharGroupForm(forms.ModelForm):
    class Meta:
        model = CharGroup
        fields = [
            'name',
        ]
        labels = {
            'name': 'Название группы характеристик',
           
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form__controls',
            }),
        }

class CharNameForm(forms.ModelForm):
  class Meta:
    model = CharName
    fields = [
        'group',
        'text_name',
        'filter_add',
        'filter_name',
        'sort_order'
        
    ]
    labels = {
        'group': 'Группа опций',
        'text_name': 'Название опции',
        'filter_add': "Добавить в фильтрацию",
        'filter_name': "Название фильтрации на английском",
        'sort_order': "Сортировка"
    }
    widgets = {
        'group': forms.Select(attrs={
          'class': 'form__controls'
        }),
        'text_name': forms.TextInput(attrs={
            'class': 'form__controls',
            'id': 'char_name'
        }),
        'filter_add': forms.CheckboxInput(attrs={
            'class': 'form__controls-checkbox',
        }),
        'filter_name': forms.TextInput(attrs={
            'class': 'form__controls',
        }),
        'sort_order': forms.TextInput(attrs={
            'class': 'form__controls',
        }),
    }

class CategoryForm(forms.ModelForm):
  """ Form, отвечает за создание категорий и редактирование категорий"""
  class Meta:
    model = Category
    fields = "__all__"
    labels = {
      "name": "Назване категории",
      "slug": "URL",
      "image": "Изображение",
      "parent": "Родительсткая категория",
      "header_show": "Отображать в шапке ?",
      "meta_h1": "Заголовок H1",
      "meta_title": "Meta заголовок",
      "meta_description": "Meta описание",
      "meta_keyword": "Meta keywords",
      "menu_add": "Добавить в меню",
      "first_block_home": "Вывести на главную страницу",
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
      'parent': forms.Select(attrs={
          'class': 'form__controls'
      }),
      'description': forms.Textarea(attrs={
          'class': 'form__controls'
      }),
      'header_show': forms.CheckboxInput(attrs={
        'class': 'form__controls-checkbox',
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
      "menu_add": forms.CheckboxInput(attrs={
        "class":"form__controls-checkbox",
        # "placeholder": "Meta keywords"
      }),  
      "first_block_home": forms.CheckboxInput(attrs={
        "class":"form__controls-checkbox",
        # "placeholder": "Meta keywords"
      }),  
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
      
class SliderForm(forms.ModelForm):
  """ Form, редактирование слайдера главной страницы """
  # description = forms.CharField(label='Полное описание товара', required=False, widget=CKEditorUploadingWidget())
  
  class Meta:
      model = SliderHome
      fields = [
          'title',
          'description',
          'link',
          'image',
      ]
      labels = {
          'title': 'Заголовок',
          'description':'Описание',
          'link': 'Ссылка на страницу',
          'image':'Изображение',
      }
      widgets = {
          'title': forms.TextInput(attrs={
              'class': 'form__controls'
          }),
          'description': forms.Textarea(attrs={
              'class': 'form__controls',
          }),
          'link': forms.TextInput(attrs={
              'class': 'form__controls',
          })
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
    
class ShopSettingsForm(forms.ModelForm):
    """ Form, отвечает за создание товара и редактирование товара"""
    # description = forms.CharField(label='Описание производителя', required=False, widget=CKEditorUploadingWidget)
    # description = forms.CharField(widget=TinyMCE())
    class Meta:
        model = ShopSettings
        fields = [
            'meta_h1',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'delivery',
        ]
        labels = {
            'meta_h1':'Заголвок первого уровня',
            'meta_title':'Meta title',
            'meta_description':'Мета description',
            'meta_keywords':'Meta keywords',
            'delivery':'Стоимость доставки',
        }
        widgets = {
            'meta_h1': forms.TextInput(attrs={
                'class': 'form__controls',
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'form__controls',
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'form__controls',
                "id": "meta_description"
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'form__controls',
            }),
            'delivery': forms.NumberInput(attrs={
                'class': 'form__controls',
            }),
        }
              
class MessangerForm(forms.ModelForm):
    """ Form, отвечает за создание товара и редактирование товара"""
    # description = forms.CharField(label='Описание производителя', required=False, widget=CKEditorUploadingWidget)
    # description = forms.CharField(widget=TinyMCE())
    class Meta:
        model = Messanger
        fields = "__all__"
        widgets = {
            # 'meta_h1': forms.TextInput(attrs={
            #     'class': 'form__controls',
            # }),
            # 'meta_title': forms.TextInput(attrs={
            #     'class': 'form__controls',
            # }),
            # 'meta_description': forms.Textarea(attrs={
            #     'class': 'form__controls',
            #     "id": "meta_description"
            # }),
            # 'meta_keywords': forms.TextInput(attrs={
            #     'class': 'form__controls',
            # }),
            # 'delivery': forms.NumberInput(attrs={
            #     'class': 'form__controls',
            # }),
        }
             
class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = "__all__"
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form__controls',
                'placeholder': 'Код купона',
            }),
            'valid_from': forms.DateInput(attrs={
                'class': 'input',
                'type': 'date',
                
            }),
            'valid_to': forms.DateInput(attrs={
                'class': 'input',
                'type': 'date',
                
            }),
            'discount': forms.NumberInput(attrs={
                'class': 'form__controls',
                'placeholder': 'Скидка',
            }),
        }