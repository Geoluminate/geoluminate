import $ from 'jquery'


$.endlessPaginate({
  onCompleted: function (context, fragment) {
    console.log('Label:', $(this).text())
    console.log('URL:', context.url)
    console.log('Querystring key:', context.key)
    console.log('Fragment:', fragment)
  }
})
