export default function({ store, redirect }) {
  // If the user is not authenticated
  console.log(store.state.accessToken)

  if (!store.state.accessToken) {
    return redirect('/signin')
  }
}
