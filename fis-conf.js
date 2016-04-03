// 只需要编译 html 文件，以及其用到的资源。
fis.set('project.files', ['*.html', 'map.json']);


fis.match('*.js', {
  isMod: true
});

/*这两个js不是模块*/
fis.match('/static/lib/sea.js', {
  isMod: false
});
fis.match('/static/lib/seajs-css.js', {
  isMod: false
});

/*压缩所有的js*/
fis.match('*.js', {
  // fis-optimizer-uglify-js 插件进行压缩，已内置
  optimizer: fis.plugin('uglify-js')
});

/*压缩所有的css*/
fis.match('*.css', {
  // fis-optimizer-clean-css 插件进行压缩，已内置
  optimizer: fis.plugin('clean-css')
});

fis.hook('cmd', {
  baseUrl: './sea-modules/',

  paths: {
    "jquery":"jquery/dist/jquery.min.js",
    "$":"jquery/dist/jquery.min.js"
  }
});

fis.match('::packager', {
  postpackager: fis.plugin('loader')
});


// 注意： fis 中的 sea.js 方案，不支持部分打包。
// 所以不要去配置 packTo 了，运行时会报错的。
fis
    .media('prod')
    .match('*.js', {
    // 通过 uglify 压缩 js
    // 记得先安装：
    // npm install [-g] fis-optimizer-uglify-js
    optimizer: fis.plugin('uglify-js')
  })
  .match('::packager', {
    postpackager: fis.plugin('loader', {
      allInOne: {
        includeAsyncs: true,
        ignore: ['/static/lib/sea.js',
          '/static/lib/seajs-css.js']
      }
    })
  })
