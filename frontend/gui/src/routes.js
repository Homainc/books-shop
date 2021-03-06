import React from 'react';
import {Route} from 'react-router-dom';
import ProductList from './ProductListPage/ProductList';
import connectedProductDetail from './_components/ProductDetail';
import NormalLoginForm from './LoginPage/Login';
import RegistrationForm from './SignUpPage/Signup';
import connectedCartList from './CartListPage/CartList';
import OrderForm from './OrderPage/Order';
import MapContainer from './MapPage/MapContainer';
import ProductType from './_components/ProductType';


const BaseRouter = () => (
    <div>
        <Route exact path='/login/' component={NormalLoginForm} />
        <Route exact path='/signup/' component={RegistrationForm} />
        <Route exact path='/' component={ProductList} />
        <Route exact path='/products/:productId/' component={connectedProductDetail} />
        <Route exact path='/products/type/:productType/' component={ProductType} />
        <Route exact path='/my-cart/' component={connectedCartList} />
        <Route exact path='/my-order/' component={OrderForm} />
        <Route exact path='/map/:roomID/' component={MapContainer} />
    </div>
);

export default BaseRouter;