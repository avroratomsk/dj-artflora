// import "./import/modules";
// import "./import/components";
// import "./import/inputMask";
// import "./import/script";

// new VenoBox({
//   selector: ".index-gallery__item"
// });

console.log("Работает");

/**
 * Функция отктия и закрытия строку поиска  и фильтрацию по убыванию/возрастанию
 * 
 * Оптимизировать код
 */

const openSearchBtn = document.getElementById('open-search');
if (openSearchBtn) {
  openSearchBtn.addEventListener('click', function (e) {
    this.classList.toggle('_active');
    document.getElementById('single-search').classList.toggle('_active');

    if (!this.classList.contains('_active')) {
      this.innerHTML = '<i class="fa-solid fa-magnifying-glass"></i>';
    } else {
      this.innerHTML = '<i class="fa-solid fa-xmark"></i>';
    }
  })
}

const openFilterBtn = document.getElementById('open-filter');
if (openFilterBtn) {
  openFilterBtn.addEventListener('click', function (e) {
    this.classList.toggle('_active');
    document.getElementById('filter-sort').classList.toggle('_active');

    if (!this.classList.contains('_active')) {
      this.innerHTML = '<i class="fa-solid fa-sliders"></i>';
    } else {
      this.innerHTML = '<i class="fa-solid fa-xmark"></i>';
    }
  })
}

/**
 * Фильтр по цене 
 * 
 * Разобраться в скрипке 
 */

const rangeInput = document.querySelectorAll(".price-input__range input");
const priceInputField = document.querySelectorAll(".price-input__field input");
const progress = document.querySelector('#prodgress');
const priceGap = 1000;


if (rangeInput) {
  rangeInput.forEach(input => {
    input.addEventListener('input', (e) => {
      const minValue = parseInt(rangeInput[0].value);
      const maxValue = parseInt(rangeInput[1].value);

      if (maxValue - minValue < priceGap) {
        if (e.target.className === "price-input__range-min") {
          rangeInput[0].value = maxValue - priceGap;
        } else {
          rangeInput[1].value = minValue + priceGap;
        }
      } else {
        priceInputField[0].value = minValue;
        priceInputField[1].value = maxValue;
        progress.style.left = (minValue / rangeInput[0].max) * 100 + "%";
        progress.style.right = 100 - (maxValue / rangeInput[1].max) * 100 + "%";
      }


    })

  })
}


/**
 * Рейтинг в виде звездочек
 */

const ratingItemList = document.querySelectorAll('.form__star');
const inputSaveRating = document.querySelector('#form-reviews__rating');
if (ratingItemList) {
  const ratingItemArray = Array.prototype.slice.call(ratingItemList);

  ratingItemArray.forEach(item => {
    item.addEventListener('click', function (e) {
      const { rating } = item.dataset;
      item.parentNode.dataset.ratingTotal = rating;
      // inputSaveRating.value = rating;
    })
  })
}

/**
 * Просмотр полного описания продукта
 */

const btnViewProduct = document.querySelectorAll('.product-desc');
if (btnViewProduct) {
  btnViewProduct.forEach(btn => btn.addEventListener('click', viewProduct));
}

function viewProduct(e) {
  let parentNodeHtml = this.closest('.card-product').querySelector('.card-product__info').innerHTML;
  let popupView = document.querySelector('.popup-view .popup__grid');
  console.log(popupView);

  if (popupView) {
    popupView.innerHTML = parentNodeHtml;
  }
}

const orderBtn = document.querySelectorAll('.filter-sort__value');

let popupBtn = document.querySelectorAll('[data-popup]')

if (popupBtn) {
  popupBtn.forEach(btn => {
    btn.addEventListener('click', openPopup);
  })
}

function openPopup(e) {
  document.getElementById(this.dataset.popup).classList.add('_open');
  bodyLock();
}


// Создание правильной ссылка номера телефона
const regNum = document.querySelectorAll('.reg-num');
if (regNum) {
  regNum.forEach(num => {
    phoneNumber = num.href.replace('tel:', '');
    newNumber = clearSimvol(phoneNumber.replace('8', "+7"));
    num.href = newNumber
  });
}
function clearSimvol(str) {
  return str.replace(/[\s.,%,),(,-]/g, '');
}

/**
 * Функции отвечающие за открытие и закрытие мини-корзины
 */
window.addEventListener('DOMContentLoaded', function (e) {
  const showCart = document.getElementById('show-cart');
  if (showCart) {
    showCart.addEventListener('click', showMiniCart);
  }

  function showMiniCart(e) {
    console.log(this);
    document.querySelector('#mini-cart').classList.add('_show-mini-cart');
    bodyLock();
  }

  const closeCart = document.getElementById('close-cart');
  if (closeCart) {
    closeCart.addEventListener('click', closeMiniCart);
    bodyUnLock();
  }

  function closeMiniCart(e) {
    document.querySelector('#mini-cart').classList.remove('_show-mini-cart');
    bodyUnLock();
  }
})


/**
 * Вспомогательные общие функции
 */

function bodyLock(e) {
  let widthScrollBar = window.innerWidth - document.documentElement.clientWidth;
  document.documentElement.style.marginRight = widthScrollBar + 'px';
  document.documentElement.classList.add('_lock');
}

function bodyUnLock(e) {
  document.documentElement.style.marginRight = '0px';
  document.documentElement.classList.remove('_lock');
}


const whoGetRadio = document.querySelectorAll('.who-get');
if (whoGetRadio) {
  whoGetRadio.forEach(item => {
    item.addEventListener('change', function (e) {
      console.log(this);
      if (item.dataset.id == 'another') {
        document.getElementById('contact-human').classList.add('_show')
      } else {
        document.getElementById('contact-human').classList.remove('_show')
      }
    })
  })
}

const pickupCheckbox = document.getElementById('pickup');
if (pickupCheckbox) {
  pickupCheckbox.addEventListener('change', function (e) {
    if (pickupCheckbox.checked) {
      document.getElementById('id_delivery_address').classList.add('_hidden');
    } else {
      document.getElementById('id_delivery_address').classList.remove('_hidden');
    }
  })
}

const burgerBtn = document.getElementById('burger')
if (burger) {
  burger.addEventListener('click', function (e) {
    document.querySelector('.hidden-menu').classList.add('_show');
    bodyLock();
  })
}

const closeMenuBtn = document.getElementById('close-menu')
if (closeMenuBtn) {
  closeMenuBtn.addEventListener('click', function (e) {
    document.querySelector('.hidden-menu').classList.remove('_show');
    bodyUnLock();
  })
}

const filterBtn = document.getElementById('filter-btn')
if (filterBtn) {
  filterBtn.addEventListener('click', function (e) {
    document.querySelector('.filter-mobile').classList.add('_show');
    bodyLock();
  })
}

const closeFilterBtn = document.getElementById('close-filter')
if (closeFilterBtn) {
  closeFilterBtn.addEventListener('click', function (e) {
    document.querySelector('.filter-mobile').classList.remove('_show');
    bodyUnLock();
  })
}


/**
 * Покупка в один клик
 */

const oneClickBtn = document.querySelectorAll('.add-one-click');
if (oneClickBtn) {
  oneClickBtn.forEach(btn => {
    btn.addEventListener('click', buyOneСlick)
  })
}

function buyOneСlick(e) {
  let parent = this.closest('.card-section');
  console.log(parent);
  let img = parent.querySelector('.product-click-image').src;
  let name = parent.querySelector('.card-section__name').innerText;
  let price = parent.querySelector('.card-section__price').innerText;
  popup = document.getElementById('popup-one-click');
  popup.classList.add('_open');

  document.querySelector('.popup__product-img').src = img;
  document.querySelector('.popup__product-name').innerText = name;
  document.querySelector('.product__price-text').innerText = price;

  bodyLock();
}

const closeBtn = document.querySelectorAll('.close-btn');
if (closeBtn) {
  closeBtn.forEach(btn => {
    btn.addEventListener('click', function (e) {
      let parent = this.closest('.popup');
      parent.classList.remove('_open');
      bodyUnLock();
    })
  })
}


// Ловим собыитие клика по кнопке добавить в корзину
$(document).on("click", ".add-to-cart", function (e) {
  // Блокируем его базовое действие
  e.preventDefault();

  // Берем элемент счетчика в значке корзины и берем оттуда значение
  var goodsInCartCount = $("#mini-cart-count");
  var cartCount = parseInt(goodsInCartCount.text() || 0);

  // Получаем id товара из атрибута data-product-id
  var product_id = $(this).data("product-id");

  // Из атрибута href берем ссылку на контроллер django
  var add_to_cart_url = $(this).attr("href");
  console.log(add_to_cart_url);

  // делаем post запрос через ajax не перезагружая страницу
  $.ajax({
    type: "POST",
    url: add_to_cart_url,
    data: {
      product_id: product_id,
      csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
    },
    success: function (data) {
      //alert(data.message);
      $("#notification-modal .success__body").text(data.message);
      $("#notification-modal").addClass("show");

      // Закрытие модального окна после 5 секунд
      setTimeout(function () {
        $("#notification-modal").removeClass("show");
      }, 5000);


      // Увеличиваем количество товаров в корзине (отрисовка в шаблоне)
      cartCount++;
      goodsInCartCount.text(cartCount);

      $('#show-cart').append('<span class="cart_count">' + cartCount + '</span>')

      if (cartCount > 0) {
        $('#mini-cart_noempty').html('<h4 class="mini-cart__title">Корзина<span>(</span><strong id="mini-cart-count">' + cartCount + '</strong><span>)</span></h4><div class="mini-cart__inner" id="cart-item">{% include "components/cart-item.html" %}</div><div class="mini-cart__links"><a href="/orders/create/" class="mini-cart__link">Оформить заказ</a></div>')
      }

      // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
      var cartItemsContainer = $("#cart-item");
      cartItemsContainer.html(data.cart_items_html);
    },

    error: function (data) {
      console.log("Ошибка при добавлении товара в корзину");
    },
  });
});

$(document).on("click", ".remove-from-cart", function (e) {
  // Блокируем его базовое действие
  e.preventDefault();

  // Берем элемент счетчика в значке корзины и берем оттуда значение
  var goodsInCartCount = $("#mini-cart-count");
  var cartCount = parseInt(goodsInCartCount.text() || 0);

  // Получаем id корзины из атрибута data-cart-id
  var cart_id = $(this).data("cart-id");
  // Из атрибута href берем ссылку на контроллер django
  var remove_from_cart = $(this).attr("href");
  console.log(remove_from_cart);
  console.log($("[name=csrfmiddlewaretoken]").val());
  // делаем post запрос через ajax не перезагружая страницу
  $.ajax({
    type: "POST",
    url: remove_from_cart,
    data: {
      cart_id: cart_id,
      csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
    },
    success: function (data) {
      // Уменьшаем количество товаров в корзине (отрисовка)
      cartCount -= data.quantity_deleted;
      goodsInCartCount.text(cartCount);
      $("#show-cart span").text(cartCount);
      if (cartCount == 0) {
        // $('#show-cart .no-empty').remove();
        $('#mini-cart_noempty').html('<div class="mini-cart__empty"><p class="mini-cart__empty-text">Пусто</p><a href="{% url "category" %}"class="mini-cart__empty-link">Перейти в каталог</a></div>')
        // $('#mini-cart .mini-cart__links').remove()
      }
      // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
      var cartItemsContainer = $("#cart-item");
      cartItemsContainer.html(data.cart_items_html);
    },

    error: function (data) {
      console.log("Ошибка при добавлении товара в корзину");
    },
  });
});

const submenuShowBtn = document.querySelectorAll('.submenu-show');

if (submenuShowBtn) {
  submenuShowBtn.forEach(btn => {
    btn.addEventListener('click', showSubMenu);
  })
}

function showSubMenu(e) {
  let submenu = this.closest('.hidden-menu__item').querySelector('.hidden-submenu');
  submenu.classList.toggle('_show');
}

function hideTagOnResolution() {
  if (window.innerWidth <= 1024) {
    var tagsToHide = document.querySelectorAll('.header__inner-pc');
    tagsToHide.forEach(function (tag) {
      tag.remove(); // Удалить тег из DOM
    });
  }
}

// Вызов функции при загрузке страницы и при изменении размера окна
hideTagOnResolution();
window.addEventListener('resize', hideTagOnResolution);


