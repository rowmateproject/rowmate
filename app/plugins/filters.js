import  Vue  from  "vue"
import Cookies from 'js-cookie'

Vue.filter("formatDay", function(date)  {
  let format = new Intl.DateTimeFormat(Cookies.get('i18n_redirected'), { weekday: 'short', month: 'long', day: 'numeric' })
  return format.format(new Date(date))
});
