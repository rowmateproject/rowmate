<template>
<button @click="authorize" type="button" class="flex items-center cursor-pointer bg-gray-200 hover:bg-gray-300 text-gray-900 rounded focus:outline-none px-4 py-2 mr-3">
  <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" class="w-5 h-5 mr-2">
    <g>
      <path fill="#ea4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"></path>
      <path fill="#4285f4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"></path>
      <path fill="#fbbc05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"></path>
      <path fill="#34a853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"></path>
      <path fill="none" d="M0 0h48v48H0z"></path>
    </g>
  </svg>
  <span>Signup with Google</span>
</button>
</template>

<script>
export default {
  data() {
    return {
      authorizationUrl: null
    }
  },
  methods: {
    popupWindow(url, title, w = '75%', h = '16:9', opts) {
      // sort options
      let options = [];

      if (typeof opts === 'object') {
        Object.keys(opts).forEach(function(value, key) {
          if (value === true) {
            value = 'yes';
          } else if (value === false) {
            value = 'no';
          }

          options.push(`${key}=${value}`);
        });

        if (options.length) {
          options = ',' + options.join(',');
        } else {
          options = '';
        }
      } else if (Array.isArray(opts)) {
        options = ',' + opts.join(',');
      } else if (typeof opts === 'string') {
        options = ',' + opts;
      } else {
        options = '';
      }

      // add most vars to local object (to shorten names)
      let size = {
        w: w,
        h: h
      };

      let win = {
        w: {
          i: window.top.innerWidth,
          o: window.top.outerWidth
        },
        h: {
          i: window.top.innerHeight,
          o: window.top.outerHeight
        },
        x: window.top.screenX || window.top.screenLeft,
        y: window.top.screenY || window.top.screenTop
      }

      // set window size if percent
      if (typeof size.w === 'string' && size.w.endsWith('%')) {
        size.w = Number(size.w.replace(/%$/, '')) * win.w.o / 100;
      }
      if (typeof size.h === 'string' && size.h.endsWith('%')) {
        size.h = Number(size.h.replace(/%$/, '')) * win.h.o / 100;
      }

      // set window size if ratio
      if (typeof size.w === 'string' && size.w.includes(':')) {
        size.w = size.w.split(':', 2);
        if (win.w.o < win.h.o) {
          // if height is bigger than width, reverse ratio
          size.w = Number(size.h) * Number(size.w[1]) / Number(size.w[0]);
        } else {
          size.w = Number(size.h) * Number(size.w[0]) / Number(size.w[1]);
        }
      }

      if (typeof size.h === 'string' && size.h.includes(':')) {
        size.h = size.h.split(':', 2);
        if (win.w.o < win.h.o) {
          // if height is bigger than width, reverse ratio
          size.h = Number(size.w) * Number(size.h[0]) / Number(size.h[1]);
        } else {
          size.h = Number(size.w) * Number(size.h[1]) / Number(size.h[0]);
        }
      }

      // force window size to type number
      if (typeof size.w === 'string') {
        size.w = Number(size.w);
      }
      if (typeof size.h === 'string') {
        size.h = Number(size.h);
      }

      // keep popup window within padding of window size
      if (size.w > win.w.i - 50) {
        size.w = win.w.i - 50;
      }
      if (size.h > win.h.i - 50) {
        size.h = win.h.i - 50;
      }

      // do math
      const x = win.w.o / 2 + win.x - (size.w / 2);
      const y = win.h.o / 2 + win.y - (size.h / 2);
      return window.open(url, title, `width=${size.w},height=${size.h},left=${x},top=${y}${options}`);
    },
    authorize() {
      this.$axios({
        method: 'GET',
        url: `${process.env.API_URL}/auth/google/authorize?authentication_backend=jwt&scopes=https://www.googleapis.com/auth/userinfo.email+profile`,
        validateStatus: () => true
      }).then((res) => {
        if (res.status === 200) {
          console.debug(res.data.authorization_url)
          this.authorizationUrl = res.data.authorization_url
          if (process.client) {
            this.popupWindow(this.authorizationUrl, '', '420', '520', {
              scrollbars: false,
              resizable: false
            })
          }
        }
      })
    }
  }
}
</script>
