import axios from 'axios'

export default () => {
  return new Promise((resolve) => {
    axios.get(`${process.env.API_URL}/lang/de`).then((res) => {
      resolve(Object.assign(res.data.textarea, res.data.input))
    })
  })
}
