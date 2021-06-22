export function getUser(uuid,app) {
    app.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/users/${uuid}`,
      validateStatus: () => true
    }).then((res) => {
      if (res.status === 200) {
        this.user = res.data
      } else {
        this.user = false
      }
    })
  }
