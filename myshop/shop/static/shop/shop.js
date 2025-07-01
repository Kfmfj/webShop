document.addEventListener('DOMContentLoaded', () => {
  const buttons = document.querySelectorAll('.add-to-cart-btn');

  buttons.forEach(button => {
    button.addEventListener('click', event => {
      event.preventDefault();
      const productId = button.getAttribute('data-product-id');

      fetch(`/ajax/add-to-cart/${productId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/json',
        },
      })
      .then(response => response.json())
      .then(data => {
        if (data.cart_count !== undefined) {
          document.getElementById('cart-count').textContent = data.cart_count;
        }
      })
      .catch(error => console.error('Error:', error));
    });
  });
});

// Helper function to get CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
