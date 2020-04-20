const localhost = "http://127.0.0.1:8000";

const apiUrl = "/api/";

export const endpoint = `${localhost}${apiUrl}`;

export const productListUrl = `${endpoint}products/`;
export const productDetailUrl = id => `${endpoint}products/${id}/`;
export const addToCartUrl = id => `${endpoint}cart/${id}/`;
export const myCartUrl = `${endpoint}cart/`;
export const deleteCartItemUrl = id => `${endpoint}cart/delete/${id}/`;
export const updateCartItemUrl = id => `${endpoint}cart/update/${id}/`;
export const orderUrl = id => `${endpoint}order/success/${id}/`;