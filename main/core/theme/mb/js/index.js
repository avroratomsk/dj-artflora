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

orderBtn.forEach(btn => {
  btn.addEventListener('click', function (e) {
    // e.preventDefault();
  })
})


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
}

function closeMiniCart(e) {
  document.querySelector('#mini-cart').classList.remove('_show-mini-cart');
  bodyUnLock();
}

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

/**
 * Работа с добавление в корзину без перезагрузки страницы
 */

let addToCartButton = document.querySelectorAll('.add-to-cart');

// if (addToCartButton) {
//   addToCartButton.forEach(btn => [
//     btn.addEventListener('click', addToCart)
//   ])
// }

// function addToCart(e) {
//   e.preventDefault();
//   // let miniCartCount = parseInt(document.querySelector('#mini-cart-count').textContent) || 0;
//   let productId = this.getAttribute('data-product-id');
//   console.log(productId);
//   let productLink = this.getAttribute('href');
//   console.log(productLink);
//   let csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
//   console.log(csrfToken);

//   fetch('/cart/', {
//     method: 'POST',
//     headers: {
//       // "Accept": "application/json",
//       'Content-Type': 'application/json',
//       "X-CSRFToken": csrfToken
//     },
//     body: JSON.stringify(productId)
//   })
//     .then(response => response.json())
//     .then(data => { console.log(data) })
//     .catch(error => {
//       console.error('Ошибка при отправке данных:', error);
//     })

// fetch('/cart/cart_add/', {
//   method: 'POST',
//   headers: {
//     "Accept": "application/json",
//     'Content-Type': 'application/json',
//     'X-CSRFToken': csrfToken
//   },
//   body: JSON.stringify({ product_id: productId })
// })
//   .then(response => {
//     if (!response.ok) {
//       throw new Error('Network response was not ok');
//     }
//     const contentType = response.headers.get('content-type');
//     if (contentType && contentType.includes('application/json')) {
//       return response.json();
//     } else {
//       throw new Error('Unexpected response type');
//     }
//   })
//   .then(data => {
//     console.log(data);
//     // miniCartCount++;
//     let cartItemsContainer = document.querySelector('#cart-item');
//     cartItemsContainer.innerHTML = data.cart_items_html;
//     // document.querySelector('#mini-cart-count').textContent = miniCartCount; // Обновляем счетчик товаров в мини-корзине
//   })
//   .catch(error => {
//     console.error('Ошибка:', error);
//   });
// }

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
    if (!pickupCheckbox.checked) {
      document.getElementById('address-delivery').classList.add('_hidden');
    } else {
      document.getElementById('address-delivery').classList.remove('_hidden');
    }
  })
}

/**
 * Покупка в один клик
 */

const oneClickBtn = document.querySelectorAll('.card__click');
if (oneClickBtn) {
  oneClickBtn.forEach(btn => {
    btn.addEventListener('click', buyOneСlick)
  })
}

function buyOneСlick(e) {
  let parent = this.closest('.card');
  let img = parent.querySelector('.product-click-image').src;
  let name = parent.querySelector('.card__title-h3').innerText;
  let price = parent.querySelector('.card__price').innerText;
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

