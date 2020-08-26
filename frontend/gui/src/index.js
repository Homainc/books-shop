import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import * as serviceWorker from './serviceWorker';
import {createStore, compose, applyMiddleware, combineReducers} from 'redux';
import authReducer from './store/reducers/auth';
import locationReducer from './store/reducers/orderRoom';
import cartReducer from './store/reducers/cart';
import thunkMiddleware from 'redux-thunk';
import { Provider } from 'react-redux';
import 'leaflet/dist/leaflet.css';
import {jwt} from './store/middleware/jwt_middleware';


const composeEnhances = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const rootReducer = combineReducers({
    auth: authReducer,
    location: locationReducer,
    cart: cartReducer,
});


const store = createStore(rootReducer, composeEnhances(
    applyMiddleware
    (
        jwt,
        thunkMiddleware
    )
));


const app = (
    <Provider store={store}>
        <App />
    </Provider>
);

ReactDOM.render(app, document.getElementById('root'));
serviceWorker.unregister();