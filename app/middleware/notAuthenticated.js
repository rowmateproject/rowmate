export default async function({
  store,
  redirect
}) {
  // If the user is not authenticated
  if (!store.state.accessToken) {
    return redirect('/signin')
  }
}
