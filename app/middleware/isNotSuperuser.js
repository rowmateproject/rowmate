export default function({
  store,
  redirect
}) {
  // If the user is not authenticated
  if (store.state.isSuperuser !== 'true' && store.state.isSuperuser !== true) {
    return redirect('/settings')
  }
}
