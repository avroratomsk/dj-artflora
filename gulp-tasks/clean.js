"use strict";

import gulp from "gulp";
import del from "del";

gulp.task("clean", () => {
    return del([
        "./main/core/theme/mb/css",
        "./main/core/theme/mb/fonts",
        "./main/core/theme/mb/images",
        "./main/core/theme/mb/views",
        "./main/core/theme/mb/js",
    ]);
});

gulp.task("adminclean", () => {
    return del([
        "./main/core/admin/*",
        "./main/core/admin/css/**/*.css"
    ]);
});