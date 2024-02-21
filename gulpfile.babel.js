"use strict";

import gulp from "gulp";

const requireDir = require("require-dir"),
    paths = {
        views: {
            src: [
                "./#src/templates/theme/**/*.html",
                "./src/templates/theme/pages/*.html"
            ],
            dist: "./main/core/theme/mb/templates/",
            watch: [
                "./#src/templates/theme/**/*.html"
            ]
        },
        styles: {
            src: "./#src/scss/main.{scss,sass}",
            dist: "./main/core/theme/mb/css/",
            watch: [
                "./#src/scss/**/*.{scss,sass}"
            ]
        },
        scripts: {
            src: "./#src/js/index.js",
            dist: "./main/core/theme/mb/js/",
            watch: [
                "./#src/js/**/*.js"
            ]
        },
        images: {
            src: [
                "./#src/img/**/*.{jpg,jpeg,png,gif,tiff,svg}",
                "!./#src/img/favicon/*.{jpg,jpeg,png,gif,tiff}"
            ],
            dist: "./main/core/theme/mb/images/",
            watch: "./#src/img/**/*.{jpg,jpeg,png,gif,svg,tiff}"
        },
        sprites: {
            src: "./#src/img/sprites/*.svg",
            dist: "./main/core/theme/mb/images/sprites/",
            watch: "./#src/img/sprites/*.svg"
        },
        fonts: {
            src: "./#src/fonts/**/*.{woff,woff2}",
            dist: "./main/core/theme/mb/fonts/",
            watch: "./#src/fonts/**/*.{woff,woff2}"
        },
        favicons: {
            src: "./#src/img/favicon/*.{jpg,jpeg,png,gif}",
            dist: "./main/core/theme/mb/image/favicons/",
        },
        gzip: {
            src: "./#src/.htaccess",
            dist: "./main/core/"
        },

        // admin
        adminviews: {
            src: [
                "./#src/templates/admin/**/*.html",
                "./#src/templates/admin/pages/*.html"
            ],
            dist: "./main/core/admin/templates/",
            watch: [
                "./#src/templates/admin/**/*.html",
                "./#src/templates/admin/pages/*.html"
            ]
        },
        adminstyles: {
            src: "./#src/scss/admin/style.{scss,sass}",
            dist: "./main/core/admin/css/",
            watch: [
                "./#src/scss/admin/**/*.{scss,sass}",
                "./#src/scss/admin/**/*.{scss,sass}"
            ]
        },
        adminscripts: {
            src: "./#src/js/admin/app.js",
            dist: "./main/core/admin/js/",
            watch: [
                "./#src/js/admin/**/*.js",
                "./#src/js/admin/**/*.js"
            ]
        },
        adminimages: {
            src: [
                "./#src/img/admin/**/*.{jpg,jpeg,png,gif,tiff,svg}",
                "!./#src/img/admin/fav/*.{jpg,jpeg,png,gif,tiff}"
            ],
            dist: "./main/core/admin/images/",
            watch: "./#src/images/admin/**/*.{jpg,jpeg,png,gif,svg,tiff}"
        },
        adminsprites: {
            src: "./#src/img/admin/sprites/*.svg",
            dist: "./main/core/admin/images/sprites/",
            watch: "./#src/img/admin/sprites/*.svg"
        },
        adminfonts: {
            src: "./#src/fonts/admin/**/*.{woff,woff2,ttf}",
            dist: "./main/core/admin/fonts/",
            watch: "./#src/fonts/admin/**/*.{woff,woff2,ttf}"
        },
        adminfavicons: {
            src: "./#src/img/admin/fav/*.{jpg,jpeg,png,gif}",
            dist: "./main/core/img/fav/",
        }
    };

requireDir("./gulp-tasks/");

export { paths };

export const development = gulp.series("clean",
    gulp.parallel(["views", "styles", "scripts", "images", "webp", "sprites", "fonts", "favicons"]),
    gulp.parallel("serve"));

export const prod = gulp.series("clean",
    gulp.parallel(["views", "styles", "scripts", "images", "webp", "sprites", "fonts", "favicons", "gzip"]));

export default development;