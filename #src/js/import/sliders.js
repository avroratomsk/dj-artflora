/*
Документация по работе в шаблоне: 
Документация слайдера: https://swiperjs.com/
Сниппет(HTML): swiper
*/

// Подключаем слайдер Swiper из node_modules
// При необходимости подключаем дополнительные модули слайдера, указывая их в {} через запятую
// Пример: { Navigation, Autoplay }
import Swiper from "swiper";
import { Autoplay, EffectFade, Navigation, Pagination, Thumbs } from "swiper/modules";
/*
Основниые модули слайдера:
Navigation, Pagination, Autoplay, \
EffectFade, Lazy, Manipulation
Подробнее смотри https://swiperjs.com/
*/

// Стили Swiper
// Базовые стили
import "../../scss/base/swiper.scss";
// Полный набор стилей из scss/libs/swiper.scss
import "../../scss/libs/swiper.scss";
// Полный набор стилей из node_modules
// import 'swiper/css';

// Инициализация слайдеров
function initSliders() {
  // Перечень слайдеров
  // Проверяем, есть ли слайдер на стронице

  if (document.querySelector(".index-slider__slider")) {
    // Указываем скласс нужного слайдера
    // Создаем слайдер
    new Swiper(".index-slider__slider", {
      // Указываем скласс нужного слайдера
      // Подключаем модули слайдера
      // для конкретного случая
      modules: [Navigation, Pagination, Autoplay],
      observer: true,
      observeParents: true,
      slidesPerView: 1,
      spaceBetween: 5,
      autoHeight: true,
      speed: 800,

      //touchRatio: 0,
      //simulateTouch: false,
      loop: true,
      //preloadImages: false,
      //lazy: true,

      // Эффекты
      // effect: 'fade',
      autoplay: {
        delay: 10000,
        disableOnInteraction: false,
      },

      // Пагинация
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
        dynamicBullets: false,
      },

      // Скроллбар
      /*
      scrollbar: {
        el: '.swiper-scrollbar',
        draggable: true,
      },
      */

      // Кнопки "влево/вправо"
      navigation: {
        prevEl: ".index-button-prev",
        nextEl: ".index-button-next",
      },

      // navigation: {
      //   prevEl: '.swiper-button-prev',
      //   nextEl: '.swiper-button-next',
      // },

      // Брейкпоинты
      // breakpoints: {
      // 	320: {
      // 		slidesPerView: 1,
      // 		spaceBetween: 20,
      // 		autoHeight: true,
      // 	},
      // 	485: {
      // 		slidesPerView: 2,
      // 		spaceBetween: 20,
      // 	},
      // 	992: {
      // 		slidesPerView: 3,
      // 		spaceBetween: 20,
      // 	},
      // 	1268: {
      // 		slidesPerView: 3,
      // 		spaceBetween: 30,
      // 	},
      // },
      // События
      on: {},
    });
  }

  if (document.querySelector(".reviews__slider")) {
    // Указываем скласс нужного слайдера
    // Создаем слайдер
    new Swiper(".reviews__slider", {
      // Указываем скласс нужного слайдера
      // Подключаем модули слайдера
      // для конкретного случая
      modules: [Navigation, Pagination, Autoplay],
      observer: true,
      observeParents: true,
      slidesPerView: 3,
      spaceBetween: 35,
      autoHeight: true,
      centeredSlides: true,
      speed: 800,

      //touchRatio: 0,
      //simulateTouch: false,
      loop: true,
      //preloadImages: false,
      //lazy: true,

      // Эффекты
      // effect: 'fade',
      autoplay: {
        delay: 10000,
        disableOnInteraction: false,
      },

      // Пагинация
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
        dynamicBullets: true,
      },

      // Скроллбар
      /*
      scrollbar: {
        el: '.swiper-scrollbar',
        draggable: true,
      },
      */

      // Кнопки "влево/вправо"
      navigation: {
        prevEl: ".reviews__controls-prev",
        nextEl: ".reviews__controls-next",
      },

      // navigation: {
      //   prevEl: '.swiper-button-prev',
      //   nextEl: '.swiper-button-next',
      // },

      // Брейкпоинты
      // breakpoints: {
      // 	320: {
      // 		slidesPerView: 1,
      // 		spaceBetween: 20,
      // 		autoHeight: true,
      // 	},
      // 	485: {
      // 		slidesPerView: 2,
      // 		spaceBetween: 20,
      // 	},
      // 	992: {
      // 		slidesPerView: 3,
      // 		spaceBetween: 20,
      // 	},
      // 	1268: {
      // 		slidesPerView: 3,
      // 		spaceBetween: 30,
      // 	},
      // },
      // События
      on: {},
    });
  }

  if (document.querySelector(".days__slider")) {
    // Указываем скласс нужного слайдера
    // Создаем слайдер
    new Swiper(".days__slider", {
      // Указываем скласс нужного слайдера
      // Подключаем модули слайдера
      // для конкретного случая
      modules: [Navigation, Pagination, Autoplay],
      observer: true,
      observeParents: true,
      slidesPerView: 7,
      spaceBetween: 35,
      autoHeight: true,
      centeredSlides: true,
      speed: 800,

      //touchRatio: 0,
      //simulateTouch: false,
      loop: true,
      //preloadImages: false,
      //lazy: true,

      // Эффекты
      // effect: 'fade',
      autoplay: {
        delay: 10000,
        disableOnInteraction: false,
      },

      // Пагинация
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
        dynamicBullets: true,
      },

      // Скроллбар
      /*
      scrollbar: {
        el: '.swiper-scrollbar',
        draggable: true,
      },
      */

      // Кнопки "влево/вправо"
      navigation: {
        prevEl: ".reviews__controls-prev",
        nextEl: ".reviews__controls-next",
      },

      // navigation: {
      //   prevEl: '.swiper-button-prev',
      //   nextEl: '.swiper-button-next',
      // },

      // Брейкпоинты
      // breakpoints: {
      // 	320: {
      // 		slidesPerView: 1,
      // 		spaceBetween: 20,
      // 		autoHeight: true,
      // 	},
      // 	485: {
      // 		slidesPerView: 2,
      // 		spaceBetween: 20,
      // 	},
      // 	992: {
      // 		slidesPerView: 3,
      // 		spaceBetween: 20,
      // 	},
      // 	1268: {
      // 		slidesPerView: 3,
      // 		spaceBetween: 30,
      // 	},
      // },
      // События
      on: {},
    });
  }
}

// Скролл на базе слайдера (по классу swiper_scroll для оболочки слайдера)
function initSlidersScroll() {
  let sliderScrollItems = document.querySelectorAll(".swiper_scroll");
  if (sliderScrollItems.length > 0) {
    for (let index = 0; index < sliderScrollItems.length; index++) {
      const sliderScrollItem = sliderScrollItems[index];
      const sliderScrollBar = sliderScrollItem.querySelector(".swiper-scrollbar");
      const sliderScroll = new Swiper(sliderScrollItem, {
        observer: true,
        observeParents: true,
        direction: "vertical",
        slidesPerView: "auto",
        freeMode: {
          enabled: true,
        },
        scrollbar: {
          el: sliderScrollBar,
          draggable: true,
          snapOnRelease: false,
        },
        mousewheel: {
          releaseOnEdges: true,
        },
      });
      sliderScroll.scrollbar.updateSize();
    }
  }
}

window.addEventListener("load", function (e) {
  // Запуск инициализации слайдеров
  initSliders();
  // Запуск инициализации скролла на базе слайдера (по классу swiper_scroll)
  //initSlidersScroll();
});
