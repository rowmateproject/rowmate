export default async function({
  store,
  redirect
}) {
  // If the user is not superuser
  if (store.state.isSuperuser !== 'true' && store.state.isSuperuser !== true) {
    return redirect('/dashboard')
  }
}
