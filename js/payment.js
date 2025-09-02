// scripts/payments.js
import { apiFetch, showToast } from './utils.js';
const supabase = window.supabase;

// Upgrade button navigation
document.getElementById('nav-upgrade')?.addEventListener('click', (e) => {
  e.preventDefault();
  // show modal with upgrade CTA
  const body = `<p>Upgrade to Pocket Tutor Basic ($10/month) and get unlimited course generation.</p>
    <div class="row"><button id="checkout" class="btn primary">Proceed to Checkout</button></div>`;
  openModal('Upgrade to Pro', body);
  document.getElementById('checkout').addEventListener('click', startCheckout);
});

// start checkout: call backend to create stripe session
async function startCheckout() {
  try {
    showToast('Redirecting to payment...', 'info');
    const res = await apiFetch('/api/payments/create-checkout-session', { method: 'POST', body: JSON.stringify({ priceId: 'pro_monthly' }) });
    // res should include sessionId
    const stripe = Stripe(res.publishableKey); // publishable key returned by backend (safe)
    stripe.redirectToCheckout({ sessionId: res.sessionId });
  } catch (err) {
    console.error(err);
    showToast(err.data?.error || 'Could not start checkout', 'error');
  }
}

// Listen for webhook-updated subscription status via server; alternatively poll /profile
window.checkSubscription = async function checkSubscription() {
  const user = (await supabase.auth.getUser()).data.user;
  if (!user) return;
  const { data: profile } = await supabase.from('profiles').select('subscription').eq('id', user.id).single();
  return profile?.subscription;
}
