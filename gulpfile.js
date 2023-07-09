const gulp = require('gulp');
const uglify = require('gulp-uglify');
const rename = require('gulp-rename');

const src_js = 'app/static/src/*.js';
const dest_js = 'app/static/build/';

const auth_src_js = 'app/blueprints/auth/static/js/src/*.js';
const auth_dest_js = 'app/blueprints/auth/static/js/build';

const offers_src_js = 'app/blueprints/offers/static/js/src/*.js';
const offers_dest_js = 'app/blueprints/offers/static/js/build';

const recharge_src_js = 'app/blueprints/recharge/static/src/*.js';
const recharge_dest_js = 'app/blueprints/recharge/static/build';

const product_src_js = 'app/blueprints/products/static/src/*.js';
const product_dest_js = 'app/blueprints/products/static/build';

const js = function() {
    return gulp.src(src_js)
        .pipe(uglify())
        .pipe(rename({extname: '.min.js'}))
        .pipe(gulp.dest(dest_js));
};

const auth_js = function () {
    return gulp.src(auth_src_js)
        .pipe(uglify())
        .pipe(rename({extname: '.min.js'}))
        .pipe(gulp.dest(auth_dest_js));
};

const offers_js = function () {
    return gulp.src(offers_src_js)
        .pipe(uglify())
        .pipe(rename({extname: '.min.js'}))
        .pipe(gulp.dest(offers_dest_js));
};

const recharge_js = function () {
    return gulp.src(recharge_src_js)
        .pipe(uglify())
        .pipe(rename({extname: '.min.js'}))
        .pipe(gulp.dest(recharge_dest_js));
};

const product_js = function () {
    return gulp.src(product_src_js)
        .pipe(uglify())
        .pipe(rename({extname: '.min.js'}))
        .pipe(gulp.dest(product_dest_js));
};

const watch = function () {
    gulp.watch(src_js, js);
    gulp.watch(auth_src_js, auth_js);
    gulp.watch(offers_src_js, offers_js);
    gulp.watch(recharge_src_js, recharge_js);
    gulp.watch(product_src_js, product_js);
};

const build = gulp.parallel(
    js,
    auth_js,
    offers_js,
    recharge_js,
    product_js
);

exports.build = build;
exports.watch = watch;
exports.default = gulp.series(build);
