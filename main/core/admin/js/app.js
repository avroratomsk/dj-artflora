/**
 * Добавление класса активности вкладкам sidebar
 */
// const sideBarItem = document.querySelectorAll('.sidebar__item');
// if (sideBarItem) {
//   sideBarItem.forEach(item => {
//     item.addEventListener('click', function (e) {
//       this.classList.toggle('_active');
//     })
//   })
// }

// const { locale } = require("yargs");

/**
 * Переключение вкладок на страницах продуктов, категорий
 */

let imageAdd = document.querySelector(".product-block__plus");

imageAdd?.addEventListener("click", () => {
    let image = "<div class=\"product-block__inner\"><p><label for=\"id_src\">Выбрать изображение:</label><input type=\"file\" multiple=\"multiple\" name=\"src\" accept=\"image/*\" required=\"\" id=\"id_src\"></p><div class=\"product-block__minus\"><svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 448 512\"><path d=\"M416 208H32c-17.67 0-32 14.33-32 32v32c0 17.67 14.33 32 32 32h384c17.67 0 32-14.33 32-32v-32c0-17.67-14.33-32-32-32z\"></path></svg></div></div>";
    document.querySelector(".product-block__paste").innerHTML += image;
});


// $(document).on("click", ".product-block__minus", function () {
//     $(this).parent(".product-block__inner").remove();
// });

const tabButton = document.querySelectorAll("[data-name]");
const pageEditButton = document.querySelectorAll(".page-content");
if (tabButton) {
    tabButton.forEach(btn => {
        btn.addEventListener("click", function (e) {
            tabButton.forEach(item => item.classList.remove("_active"));
            pageEditButton.forEach(item => item.classList.remove("_show"));


            let bodyTabBody = document.getElementById(this.dataset.name);

            btn.classList.add("_active");
            bodyTabBody.classList.add("_show");
        });
    });
}


/**
 * Принимает на вход строку и конвертирует ее в английский язык
 */
function makeSlug(str) {
    var from = "а б в г д е ё ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я ā ą ä á à â å č ć ē ę ě é è ê æ ģ ğ ö ó ø ǿ ô ő ḿ ŉ ń ṕ ŕ ş ü ß ř ł đ þ ĥ ḧ ī ï í î ĵ ķ ł ņ ń ň ř š ś ť ů ú û ứ ù ü ű ū ý ÿ ž ź ż ç є ґ".split(" ");
    var to = "a b v g d e e zh z i y k l m n o p r s t u f h ts ch sh shch # y # e yu ya a a ae a a a a c c e e e e e e e g g oe o o o o o m n n p r s ue ss r l d th h h i i i i j k l n n n r s s t u u u u u u u u y y z z z c ye g".split(" ");

    str = str.toLowerCase();

    // remove simple HTML tags
    str = str.replace(/(<[a-z0-9\-]{1,15}[\s]*>)/gi, "");
    str = str.replace(/(<\/[a-z0-9\-]{1,15}[\s]*>)/gi, "");
    str = str.replace(/(<[a-z0-9\-]{1,15}[\s]*\/>)/gi, "");

    str = str.replace(/^\s+|\s+$/gm, ""); // trim spaces

    for (i = 0; i < from.length; ++i)
        str = str.split(from[i]).join(to[i]);

    // Replace different kind of spaces with dashes
    var spaces = [/(&nbsp;|&#160;|&#32;)/gi, /(&mdash;|&ndash;|&#8209;)/gi,
        /[(_|=|\\|\,|\.|!)]+/gi, /\s/gi];

    for (i = 0; i < from.length; ++i)
        str = str.replace(spaces[i], "-");
    str = str.replace(/-{2,}/g, "-");

    // remove special chars like &amp;
    str = str.replace(/&[a-z]{2,7};/gi, "");
    str = str.replace(/&#[0-9]{1,6};/gi, "");
    str = str.replace(/&#x[0-9a-f]{1,6};/gi, "");

    str = str.replace(/[^a-z0-9\-]+/gmi, ""); // remove all other stuff
    str = str.replace(/^\-+|\-+$/gm, ""); // trim edges

    return str;
}

/**
 * Получаем имя/названия и конвертируем его в английский язык
 */
const nameField = document.getElementById("name");
if (nameField) {
    nameField.addEventListener("input", function (e) {
        document.getElementById("slug").value = makeSlug(this.value);
    });
}

/**
 * Подсчет и отображение количества символов в meta-полях
 */
// const metaFields = document.querySelectorAll('.meta_field');
// if (metaFields) {
//   metaFields.forEach(item => {
//     let parentItem = item.closest('.form__group').querySelector('.meta-lenght');
//     console.log(item);
//     if (item.value <= 0) {
//       parentItem.innerText = 0;
//     } else {
//       parentItem.innerText = item.value.length;
//     }
//     item.addEventListener('input', function (e) {
//       parentItem.innerText = item.value.length;
//     })
//   })
// }

const dropdownButtons = document.querySelectorAll(".dropdownButton");

if (dropdownButtons) {
    dropdownButtons.forEach(btn => {
        btn.addEventListener("click", function (e) {
            console.log(e.target);
            let dropdownContent = this.querySelector(".dropdownContent");
            if (dropdownContent.classList.contains("hidden")) {
                dropdownContent.classList.remove("hidden");
                dropdownContent.style.maxHeight = dropdownContent.scrollHeight + "px";
            } else {
                dropdownContent.style.maxHeight = 0;
                // setTimeout(function () {
                dropdownContent.classList.add("hidden");
                // }, 500); // transition duration
            }
        });
    });
}

document.addEventListener("click", function (event) {
    if (event.target.classList.contains("form__plus")) {
        const blockPasteChar = document.getElementById("paste-char");
        let char_name_id = document.getElementById("id_char_name").innerHTML;
        console.log(char_name_id);
        blockPasteChar.innerHTML += `
    <div class="form__group-char">
      <label for="{{ product_char_form.char_name.id_for_label }}" class="form__controls-label">
        Название характеристики <span>:</span>
      </label>
      <select name="text_name" class="form__controls" placeholder="Название характеристики" id="id_name">${char_name_id}</select>
    
    <label for="id_char_value">Значение:</label>
    <input type="text" name="char_value" class="form__controls" placeholder="Значение" required="" id="id_char_value">
    <div class="form__remove">
      Удалить
    </div>
    </div>`;
    }
});

const menuSideBarButton = document.querySelectorAll(".menu-sidebar__dropdown-title");

if (menuSideBarButton) {
    menuSideBarButton.forEach(btn => {
        btn.addEventListener("click", function (e) {
            let parent = btn.closest(".menu-sidebar__dropdown");
            parent.classList.toggle("_active");
        });
    });
}

