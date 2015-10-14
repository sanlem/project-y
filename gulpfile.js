var gulp = require('gulp');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var react = require('gulp-react');
var htmlreplace = require('gulp-html-replace');
var exec = require('child_process').exec

var path = {
  FILES: ['ui/**/*.html', 'ui/**/*.css'],
  JSX: ['ui/js/*.jsx', 'ui/js/**/*.jsx'],
  MINIFIED_OUT: 'build.min.js',
  DEST_JS: 'ui-dist/js',
  DEST: 'ui-dist'
};

gulp.task('transform', function(){
  gulp.src(path.JSX)
    .pipe(react())
    .pipe(gulp.dest(path.DEST_JS));
});

gulp.task('copy', function(){
  gulp.src(path.FILES)
    .pipe(gulp.dest(path.DEST));
});

gulp.task('build', ['transform', 'copy']);

gulp.task('watch', ['build'], function () {
    gulp.watch(path.JSX, ['transform']);
    gulp.watch(path.FILES, ['copy']);
});

// Python tasks

gulp.task('migrate', function() {
  proc=exec('source venv/bin/activate; PYTHONUNBUFFERED=1 ./manage.py migrate');
  proc.stderr.on('data', function(data) {
    process.stdout.write(data);
  });
  proc.stdout.on('data', function(data) {
    process.stdout.write(data);
  });
});

gulp.task('serve', function() {
  proc = exec('source venv/bin/activate;' +
    'PYTHONUNBUFFERED=1 ./manage.py migrate;' +
    'PYTHONUNBUFFERED=1 ./manage.py runserver');
  proc.stderr.on('data', function(data) {
    process.stdout.write(data);
  });
  proc.stdout.on('data', function(data) {
    process.stdout.write(data);
  });
});

gulp.task('default', ['watch', 'serve']);
gulp.task('production', ['build']);

