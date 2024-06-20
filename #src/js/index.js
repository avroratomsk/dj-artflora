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
      if (item.dataset.id == 'another') {
        document.getElementById('contact-human').classList.add('_show')
      } else {
        document.getElementById('contact-human').classList.remove('_show')
      }
    })
  })
}
// $.get("/cart/set_delivery/1/", function () { })
const pickupCheckbox = document.getElementById('pickup');
if (pickupCheckbox) {
  pickupCheckbox.addEventListener('change', function (e) {
    if (e.target.checked) {
      let sd = parseInt(document.getElementById('order-delivery').innerText);
      $.get("/cart/set_delivery/0/", function () {
        document.getElementById('id_delivery_address').style.display = 'none';
        document.getElementById('suggest').required = false;
        document.getElementById('suggest').value = '';
        let summ = document.getElementById('order-total').innerText;
        let total_sum = parseInt(summ) - sd;
        document.getElementById('order-total').innerText = total_sum;
        document.getElementById('order-delivery').innerText = 0;
      });

    } else {
      $.get("/cart/set_delivery/1/", function () {
        let sd = parseInt(document.getElementById('delivery-price').innerText);
        console.log(sd);
        document.getElementById('id_delivery_address').style.display = 'flex';
        document.getElementById('suggest').required = true;
        let summ = document.getElementById('order-total').innerText;
        let total_sum = parseInt(summ) + sd;
        document.getElementById('order-total').innerText = total_sum;
        document.getElementById('order-delivery').innerText = sd;
      });

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


window.addEventListener('DOMContentLoaded', function (e) {
  const param_mass = []
  var params = window.location.search.replace('?', '').split('&');
  params.forEach(item => {
    param_mass.push(item.split('=')[0]);
  });

  if (param_mass[0] != '') {
    param_mass.forEach(item => {
      let encode = decodeURI(item)
      console.log(item);
      console.log(encode);
      let checkbox = document.querySelector('[name=' + encode + ']')
      checkbox.checked = true;
    })
  } else {
    // console.log('Четко');
  }
})

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
        $('#mini-cart_noempty').html('<div class="mini-cart__empty"><p class="mini-cart__empty-text">Пусто</p><a href="/category/"class="mini-cart__empty-link">Перейти в каталог</a></div>')
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


// const address_field = document.getElementById('suggest');

// ymaps.ready(function () {
//   // Указывается идентификатор HTML-элемента.
//   var moscow_map = new ymaps.Map("map", {
//     center: [55.76, 37.64],
//     zoom: 10
//   });
// });

var deliveryArea;
var myMap;
ymaps.ready(init);

function init() {

  var city = $('#suggest').attr('data-city')
  var zones = $('#suggest').attr('data-zones')

  var suggestView = new ymaps.SuggestView(
    'suggest', {
    provider: {
      suggest: (function (request, options) {

        return ymaps.suggest(request, {
          boundedBy: myMap.getBounds()
        });

      })
    }
  }

  );
  if (zones == 'false') {
    $(document).on('click touchend', '.ymaps-2-1-79-suggest-item', function (e) {
      $('#finaladress').val($('#suggest').val())
    })
  } else {
    $(document).on('keyup', '#suggest', function (e) {
      $('#suggest').css('border-color', 'red');
      $('#finaladress').val('')
    })

    ymaps.geocode(city).then(function (res) {
      myMap = new ymaps.Map('map', {
        center: res.geoObjects.get(0).geometry.getCoordinates(),
        zoom: 9,
        controls: []

      });


      function getzones() {
        var flickerAPI = "/core/libs/data-1.json";
        $.getJSON(flickerAPI, {
          tags: "mount rainier",
          tagmode: "any",
          format: "json"
        })
          .done(function (data) {
            var count = 0
            $.each(data.deliverys, function (index, val) {
              freeArea = new ymaps.Polygon(
                [
                  val.coords
                ], {
                hintContent: val.hintContent,
                balloonContent: val.balloonContent,
                balloonContentHeader: val.balloonContentHeader,
                balloonContentBody: val.balloonContentBody,
                balloonContentFooter: val.balloonContentFooter
              }, {

                fillColor: val.fillColor,
                strokeColor: val.strokeColor,
                opacity: val.opacity
              });
              myMap.geoObjects.add(freeArea);
              count += 1
            })
          });
      };
      getzones()
      $(document).on('click touchend', '.ymaps-2-1-79-suggest-item', function (e) {
        geocode();
        getzones()
      })
      function showError(message) {
        $('#suggest').addClass('suggest-error')
        $('#addressError').text(message)
        $('#addressError').show()
      }
      function geocode() {
        // Забираем запрос из поля ввода.
        myMap.geoObjects.removeAll()
        var request = $('#suggest').val();
        // Геокодируем введённые данные.
        ymaps.geocode(request).then(function (res) {
          var obj = res.geoObjects.get(0),
            error, hint;

          if (obj) {
            // Об оценке точности ответа геокодера можно прочитать тут: https://tech.yandex.ru/maps/doc/geocoder/desc/reference/precision-docpage/
            switch (obj.properties.get('metaDataProperty.GeocoderMetaData.precision')) {
              case 'exact':
                break;
              case 'number':
              case 'near':
              case 'range':
                error = 'Уточните номер дома';
                hint = 'Уточните номер дома';
                break;
              case 'street':
                error = 'Уточните номер дома';
                hint = 'Уточните номер дома';
                break;
              case 'other':
              default:
                error = 'Уточните адрес';
                hint = 'Уточните адрес';
            }
          } else {
            error = 'Адрес не найден';
            hint = 'Уточните адрес';
          }

          // Если геокодер возвращает пустой массив или неточный результат, то показываем ошибку.
          if (error) {
            showError(error)

          } else {
            // showResult(obj);
            var deliveryText = ''
            myMap.geoObjects.each(function (item) {
              if (item.geometry.getType() == "Polygon") {
                if (item.geometry.contains(obj.geometry._coordinates)) {
                  var deliveryText = item.properties._data.hintContent
                  var deliveryPrice = item.properties._data.balloonContentFooter
                  var sd = parseInt(deliveryPrice);

                  $.get("/cart/delivery_summ/" + sd + "/", function () {
                    checkCoupon();
                  });


                  myGeoObject = new ymaps.GeoObject({
                    // Описание геометрии.
                    geometry: {
                      type: "Point",
                      coordinates: obj.geometry._coordinates
                    },
                    // Свойства.
                    properties: {
                      iconContent: 'Я тут',
                    }
                  }, {
                    // Опции.
                    // Иконка метки будет растягиваться под размер ее содержимого.
                    preset: 'islands#blackStretchyIcon',
                    // Метку можно перемещать.
                    draggable: false
                  })
                  $('#suggest').removeClass('suggest-error')
                  $('#addressError').text('')
                  $('#addressError').hide()
                  myMap.geoObjects.removeAll()
                  getzones()
                  myMap.geoObjects.add(item)
                  myMap.geoObjects.add(myGeoObject)
                  $('#finaladress').val($('#suggest').val())
                  myMap.setCenter(obj.geometry._coordinates);
                  myMap.setZoom(17); ы
                  $('#suggest').css('border-color', 'green');

                } else {
                  showError('Нет доставки')
                  $('#finaladress').val('')
                }
              }
            })
          }
        }, function (e) {
          console.log(e.geometry._coordinates)
        })

      }
    });
  }
}

/**
 * Реализация покупки в один клик
 */

const oneClickOrderBtn = document.querySelectorAll('.one-click-order');
if (oneClickOrderBtn) {
  oneClickOrderBtn.forEach(btn => {
    btn.addEventListener('click', function (e) {
      console.log("ТОвар");
    })
  })
}

async function applyCoupon() {
  const couponCode = document.getElementById('code').value;
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  promocodErrorText = document.getElementById('order-create__promocode-error');

  if (couponCode) {
    const response = await fetch('/coupons/apply-to/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({ couponCode })
    });

    const data = await response.json();
    console.log(data.status);
    if (data.status == 1) {

      promocodErrorText.style.display = "block"
      promocodErrorText.innerText = "Промокод применился"
      checkCoupon()

    } else if (data.status == 0) {
      promocodErrorText = document.getElementById('order-create__promocode-error');
      promocodErrorText.style.display = 'block';
      promocodErrorText.innerText = "Применен";
      // checkCoupon()
    } else {
      promocodErrorText = document.getElementById('order-create__promocode-error');
      promocodErrorText.style.display = 'block';
      promocodErrorText.innerText = "Купон не действителен";
    }
  }
}

async function checkCoupon() {
  console.log("Зашел сюда");
  promocodErrorText = document.getElementById('order-create__promocode-error');
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  const response = await fetch('/coupons/check-coupons/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
  });

  const data = await response.json();

  /*
   * Тут изменения которые должны быть визуально применены
   * смена стоимсоти скидки, и стоимость досткавки
   */

  let delivery = document.getElementById('order-delivery');
  let discount = document.getElementById('discount');
  let summ = parseInt(document.getElementById('order-sum').innerText);
  let total = document.getElementById('order-total');

  let priceWithShiping = summ + parseInt(data.delivery);

  let totalSum = priceWithShiping - ((priceWithShiping * data.coupon_sum) / 100);

  console.log(`Цена с доставкой - ${priceWithShiping, typeof (priceWithShiping)} - ${totalSum, typeof (totalSum)} - со скидкой - ${data.delivery, typeof (data.delivery)} - Доставка - ${data.coupon_sum, typeof (data.coupon_sum)} - Вот такая скидка`);

  delivery.innerText = data.delivery;
  discount.innerText = data.coupon_sum;
  console.log("Тут");

  total.innerText = totalSum

}


// checkCoupon()


document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('callback-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(form.action, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken
      },
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        form.reset();
        document.getElementById('callback').classList.remove('_open');
        document.getElementById('success').classList.add('_open');
      })
      .catch(error => {
        console.log(error);
        // document.getElementById('form-messages').innerHTML = '<p>Произошла ошибка: ' + error + '</p>';
      });
  });
});


/**
 * Добавление товара в избранное
 */

const favoriteButton = document.querySelectorAll('.add-to-favorit');

const countFavorite = (csrfToken) => {
  fetch('/favorites/check/', {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken
    },
    body: JSON.stringify({})
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('Error hueror')
      }

      return response.json()
    })
    .then(data => {
      const countFavorite = document.getElementById('count');
      console.log(countFavorite);
      if (!countFavorite) {
        let favoriteElem = document.getElementById('favorites');
        favoriteElem.insertAdjacentHTML('afterbegin', '<span class="favorite_count" id="count">' + data.count + '</span>');
      } else {
        countFavorite.innerText = data.count;
      }
    })
    .catch(error => {
      console.log("Error", error);
    })
}

const toggleFavorites = (e) => {
  let btn = e.target.closest('.add-to-favorit');
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  if (btn) {
    let dataId = btn.dataset.id;
    console.log(dataId);
    fetch('/favorites/favorites-toggle/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({ "dataId": dataId })
    })
      .then(response => {
        if (!response.ok) {
          throw new Error("Error");
        }

        return response.json()
      })
      .then(data => {

        if (data.status == "added") {
          btn.classList.add('_active');
          countFavorite(csrfToken);
        } else {
          btn.classList.remove('_active');
          countFavorite(csrfToken);
        }
      })
      .catch(error => {
        console.log("Error", error);
      })
  }
}

if (favoriteButton) {
  favoriteButton.forEach(btn => {
    btn.addEventListener('click', toggleFavorites)
  })
}


/**
 * Scroll filter
 */

// const scrollElem = document.getElementById('filter-category');

// if(scrollElem){
//   scrollElem.addEventListener('scroll', (e) => {
//     e.target
//   })
// }





