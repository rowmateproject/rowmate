export default function({ store, redirect }) {
  // If the user is authenticated redirect to dashboard
  if (store.state.accessToken) {
    return redirect('/dashboard')
  }
}
