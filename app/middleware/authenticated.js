export default async function({
  store,
  redirect
}) {
  // If the user is authenticated
  if (store.state.accessToken) {
    return redirect('/dashboard')
  }
}
